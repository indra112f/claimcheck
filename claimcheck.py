#!/usr/bin/env python3
"""claimcheck: fact-check an AI-written draft against its own sources with an open-weight model.

    claimcheck draft.md                      # sources = the links inside the draft
    claimcheck draft.md --source URL ...     # add more sources
    claimcheck draft.md --report report.md --json result.json

Pipeline
  1. The model lists the checkable claims in the draft (numbers, versions, limits, dates,
     "X does Y" statements). Each claim must quote the draft; quotes that are not in the
     draft are dropped.
  2. Every source page is fetched and split into passages. For each claim the closest
     passages are picked with a small lexical scorer (numbers count extra).
  3. The model judges each claim against those passages only: supported, contradicted
     or not_found, and must copy the evidence sentence word for word.
  4. The evidence is checked against the fetched source text. If the quote is not really
     there, the verdict is downgraded to not_found. The model cannot invent its proof.

Any OpenAI-compatible chat endpoint works. Defaults: Gemma 4 on DigitalOcean serverless
inference. For fully local use point --base-url at Ollama (http://localhost:11434/v1).

Exit code: 0 when every claim is supported, 1 when something needs a human, 2 on errors.
Standard library only. MIT license.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

__version__ = "0.1.0"

DEFAULT_BASE = "https://inference.do-ai.run/v1"
DEFAULT_MODEL = "gemma-4-31B-it"
UA = f"claimcheck/{__version__} (+https://github.com/indra112f/claimcheck)"
VERDICTS = ("supported", "contradicted", "not_found")


# ---------------------------------------------------------------- text helpers
def norm(s: str) -> str:
    """Normalize for quote matching: unicode, quotes, dashes, whitespace, case."""
    s = unicodedata.normalize("NFKC", s or "")
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = re.sub(r"[‐-―−]", "-", s)
    s = re.sub(r"[`*_]", "", s)            # markdown emphasis / code ticks
    s = re.sub(r"\s+", " ", s)
    return s.strip().lower()


def quote_in(quote: str, text_norm: str, min_len: int = 12) -> bool:
    """True if the quote (or each '...'-separated piece of it) occurs in the normalized text."""
    q = norm(quote).strip(" .\"'")
    if len(q) < min_len:
        return False
    parts = [p.strip(" .\"'") for p in re.split(r"\.\.\.|…|\[\.\.\.\]", q)]
    parts = [p for p in parts if p]
    return bool(parts) and all(len(p) >= 6 and p in text_norm for p in parts)


def numbers(s: str) -> set[str]:
    """Numbers that carry meaning in a claim: 21, 3.15, 7-8, 10.15, 0.18 (single digits 0-9 and
    list numbering are ignored, they're too common to prove anything)."""
    out = set()
    for n in re.findall(r"(?<![\w.])\d+(?:[.,]\d+)*(?:-\d+)?(?![\w])", norm(s)):
        n = n.replace(",", "")
        if len(n) > 1:
            out.add(n)
    return out


def around(quote: str, text_norm: str, pad: int = 400) -> str:
    """The source text around a quote: the table row or heading a number lives in is usually
    a few hundred characters away from the sentence the model copied."""
    first = re.split(r"\.\.\.|…", norm(quote).strip(" .\"'"))[0].strip()
    i = text_norm.find(first) if first else -1
    return "" if i < 0 else text_norm[max(0, i - pad): i + len(first) + pad]


def strip_code(md: str) -> str:
    """Drop fenced code blocks; claims live in prose (code is tested, not fact-checked)."""
    return re.sub(r"^```.*?^```[ \t]*$", "", md, flags=re.S | re.M)


def md_links(md: str) -> list[str]:
    urls = re.findall(r"(?<!!)\[[^\]]*\]\((https?://[^)\s]+)\)", md)
    urls += re.findall(r"<(https?://[^>\s]+)>", md)
    seen, out = set(), []
    for u in urls:
        u = u.rstrip(".,;")
        if u not in seen:
            seen.add(u); out.append(u)
    return out


class _Text(HTMLParser):
    SKIP = {"script", "style", "noscript", "svg", "nav", "footer", "header", "form", "button"}
    BLOCK = {"p", "div", "li", "tr", "h1", "h2", "h3", "h4", "h5", "h6", "pre", "br", "section", "article", "td", "th", "dd", "dt"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self.skip = [], 0

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self.skip += 1
        elif tag in self.BLOCK:
            self.out.append("\n")

    def handle_endtag(self, tag):
        if tag in self.SKIP and self.skip:
            self.skip -= 1
        elif tag in self.BLOCK:
            self.out.append("\n")

    def handle_data(self, data):
        if not self.skip:
            self.out.append(data)


def html_to_text(raw: str) -> str:
    p = _Text()
    p.feed(raw)
    text = html.unescape("".join(p.out))
    lines = [re.sub(r"[ \t]+", " ", ln).strip() for ln in text.splitlines()]
    return "\n".join(ln for ln in lines if ln)


# ---------------------------------------------------------------- fetching
def fetch(url: str, cache_dir: Path | None, timeout: int = 25) -> str:
    key = hashlib.sha256(url.encode()).hexdigest()[:24]
    if cache_dir:
        f = cache_dir / f"{key}.txt"
        if f.exists() and time.time() - f.stat().st_mtime < 86400:
            return f.read_text(encoding="utf-8")
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,text/plain,*/*"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        ctype = r.headers.get("Content-Type", "")
        raw = r.read(4_000_000).decode(r.headers.get_content_charset() or "utf-8", "replace")
    text = raw if ("text/plain" in ctype or "markdown" in ctype or url.endswith((".md", ".txt"))) else html_to_text(raw)
    if cache_dir:
        cache_dir.mkdir(parents=True, exist_ok=True)
        (cache_dir / f"{key}.txt").write_text(text, encoding="utf-8")
    return text


# ---------------------------------------------------------------- retrieval
WORD = re.compile(r"[a-z0-9][a-z0-9._%-]*")
STOP = set("""a an the and or of to in on for with is are was were be been it its this that these those as at by from
not no can will would should may might do does did has have had you your we our they their there here than then
so if into about over under more most less very just also only any all each per via""".split())


def tokens(s: str) -> list[str]:
    return [w.strip(".-") for w in WORD.findall(norm(s)) if w.strip(".-") and w not in STOP]


def passages(text: str, size: int = 1200, step: int = 600) -> list[str]:
    if len(text) <= size:
        return [text]
    out, i = [], 0
    while i < len(text):
        out.append(text[i:i + size])
        i += step
    return out


class Index:
    """Tiny IDF-weighted lexical index over all source passages (rare words like
    'load_module' or '3.15' count much more than 'python')."""

    def __init__(self, sources: dict):
        import math
        self.items = []                      # (url, passage, token set)
        df = {}
        for url, text in sources.items():
            for p in passages(text):
                ts = set(tokens(p))
                self.items.append((url, p, ts))
                for t in ts:
                    df[t] = df.get(t, 0) + 1
        n = max(1, len(self.items))
        self.idf = {t: math.log(1 + n / c) for t, c in df.items()}

    def top(self, claim: str, k: int = 6) -> list[tuple[str, str]]:
        ct = set(tokens(claim))
        scored = []
        for url, p, ts in self.items:
            s = sum(self.idf.get(t, 0) * (2.0 if any(ch.isdigit() for ch in t) else 1.0) for t in ct & ts)
            if s > 0:
                scored.append((s, url, p))
        scored.sort(key=lambda x: -x[0])
        return [(u, p) for _, u, p in scored[:k]]


def top_passages(claim: str, sources: dict, k: int = 6) -> list[tuple[str, str]]:
    return Index(sources).top(claim, k)


# ---------------------------------------------------------------- model
class Model:
    def __init__(self, base: str, model: str, key: str | None, timeout: int = 120):
        self.base, self.model, self.key, self.timeout = base.rstrip("/"), model, key, timeout
        self.prompt_tokens = self.completion_tokens = self.calls = 0

    def chat(self, system: str, user: str, max_tokens: int = 1500) -> str:
        body = {"model": self.model, "temperature": 0, "max_tokens": max_tokens,
                "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}]}
        headers = {"Content-Type": "application/json", "User-Agent": UA}
        if self.key:
            headers["Authorization"] = f"Bearer {self.key}"
        last = None
        for attempt in range(3):
            try:
                req = urllib.request.Request(f"{self.base}/chat/completions", data=json.dumps(body).encode(), headers=headers)
                with urllib.request.urlopen(req, timeout=self.timeout) as r:
                    data = json.loads(r.read().decode())
                u = data.get("usage") or {}
                self.prompt_tokens += int(u.get("prompt_tokens") or 0)
                self.completion_tokens += int(u.get("completion_tokens") or 0)
                self.calls += 1
                return data["choices"][0]["message"]["content"] or ""
            except urllib.error.HTTPError as e:
                last = f"HTTP {e.code}: {e.read()[:300].decode('utf-8', 'replace')}"
                if e.code not in (429, 500, 502, 503, 504):
                    break
            except (urllib.error.URLError, TimeoutError, KeyError, ValueError) as e:
                last = str(e)
            time.sleep(2 * (attempt + 1))
        raise RuntimeError(f"model call failed: {last}")


def parse_json(s: str):
    s = s.strip()
    s = re.sub(r"^```(?:json)?\s*|\s*```$", "", s)
    for opener, closer in (("[", "]"), ("{", "}")):
        i, j = s.find(opener), s.rfind(closer)
        if i != -1 and j > i:
            try:
                return json.loads(s[i:j + 1])
            except ValueError:
                continue
    raise ValueError("no JSON in model output")


EXTRACT_SYS = """You list the factual claims in a technical article draft that a reader could check against documentation.
Include: numbers, prices, limits, versions, dates, defaults, names of settings/flags/commands and what they do,
"X supports/requires/returns Y" statements. Skip opinions, advice, and the author's own experience.
Return ONLY a JSON array, at most {n} items, each: {{"claim": "<one self-contained sentence>", "quote": "<exact words copied from the draft that state it>"}}."""

VERIFY_SYS = """You check ONE claim from an article draft against the source passages given. Use only the passages, not your own knowledge.
Judge what the DRAFT TEXT actually says (the summary line is only a hint and may be imprecise).
verdict:
- "supported": a passage states the same thing (same numbers, names, conditions).
- "contradicted": a passage states something incompatible (different number, version, default, or the opposite).
- "not_found": the passages do not settle it.
For supported/contradicted, copy ONE sentence from the passage word for word as evidence (no paraphrase, no ellipsis if avoidable).
Return ONLY JSON: {"verdict": "...", "source": "S1", "evidence": "...", "note": "<max 20 words>"}"""


# ---------------------------------------------------------------- pipeline
def extract_claims(m: Model, draft: str, n: int) -> list[dict]:
    prose = strip_code(draft)
    raw = m.chat(EXTRACT_SYS.format(n=n), prose[:60000], max_tokens=4000)
    items = parse_json(raw)
    if not isinstance(items, list):
        raise ValueError("claim list is not a JSON array")
    dn = norm(prose)
    out, seen = [], set()
    for it in items:
        if not isinstance(it, dict):
            continue
        c, q = str(it.get("claim") or "").strip(), str(it.get("quote") or "").strip()
        if not c or not quote_in(q, dn, min_len=8):
            continue                     # the model must point at real text in the draft
        if norm(c) in seen:
            continue
        seen.add(norm(c))
        out.append({"claim": c, "quote": q})
    return out[:n]


def verify(m: Model, claim: str, sources: dict, src_norm: dict, index: "Index | None" = None, quote: str = "") -> dict:
    ps = (index or Index(sources)).top(claim + " " + quote)
    if not ps:
        return {"verdict": "not_found", "source": None, "evidence": "", "note": "no source passage mentions it"}
    labels = {}
    blocks = []
    for i, (url, p) in enumerate(ps, 1):
        labels[f"S{i}"] = url
        blocks.append(f"[S{i}] {url}\n{p}")
    head = f"DRAFT TEXT: {quote}\nSUMMARY: {claim}" if quote else f"CLAIM: {claim}"
    raw = m.chat(VERIFY_SYS, head + "\n\nPASSAGES:\n\n" + "\n\n".join(blocks), max_tokens=600)
    try:
        r = parse_json(raw)
    except ValueError:
        return {"verdict": "not_found", "source": None, "evidence": "", "note": "model answer was not JSON"}
    v = str(r.get("verdict") or "").lower()
    v = v if v in VERDICTS else "not_found"
    url = labels.get(str(r.get("source") or "").strip("[] "))
    ev = str(r.get("evidence") or "").strip()
    note = str(r.get("note") or "")[:200]
    if v != "not_found":
        # the evidence must really be in a fetched source, otherwise it doesn't count
        hit = url if url and quote_in(ev, src_norm[url]) else next((u for u, t in src_norm.items() if quote_in(ev, t)), None)
        if not hit:
            return {"verdict": "not_found", "source": url, "evidence": ev,
                    "note": f"model said {v}, but its quote is not in the source (discarded)", "quote_checked": False}
        url = hit
        if v == "supported":
            # numbers in the draft text must appear in the evidence (or the page's own title/URL,
            # e.g. "3.15" on the 3.15 release notes); otherwise the quote doesn't prove the number
            near = numbers(url + " " + sources[url][:300]) | numbers(ev) | numbers(around(ev, src_norm[url]))
            missing = [n for n in numbers(quote or claim) if n not in near]
            if missing:
                return {"verdict": "not_found", "source": url, "evidence": ev, "quote_checked": False,
                        "note": f"model said supported, but its quote doesn't contain {', '.join(missing)}"}
    return {"verdict": v, "source": url, "evidence": ev, "note": note, "quote_checked": v != "not_found"}


def report_md(path: str, results: list[dict], stats: dict) -> str:
    icon = {"supported": "OK", "contradicted": "WRONG", "not_found": "CHECK"}
    c = {v: sum(r["verdict"] == v for r in results) for v in VERDICTS}
    lines = [f"# claimcheck report: {path}", "",
             f"- Claims checked: **{len(results)}**",
             f"- Supported: **{c['supported']}** · Contradicted: **{c['contradicted']}** · Not found in sources: **{c['not_found']}**",
             f"- Model: `{stats['model']}` · {stats['calls']} calls · {stats['prompt_tokens']:,} in / {stats['completion_tokens']:,} out tokens · {stats['seconds']:.0f}s",
             f"- Sources fetched: {stats['sources_ok']} (failed: {stats['sources_failed']})", ""]
    order = {"contradicted": 0, "not_found": 1, "supported": 2}
    for i, r in enumerate(sorted(results, key=lambda r: order[r["verdict"]]), 1):
        lines.append(f"## {i}. [{icon[r['verdict']]}] {r['claim']}")
        lines.append(f"> Draft: \"{r['quote']}\"")
        if r.get("evidence") and r.get("quote_checked"):
            lines.append(f"> Source ({r['source']}): \"{r['evidence']}\"")
        if r.get("note"):
            lines.append(f"\n{r['note']}")
        lines.append("")
    return "\n".join(lines)


def run(args) -> int:
    draft = Path(args.draft).read_text(encoding="utf-8")
    urls = list(dict.fromkeys((md_links(draft) if not args.no_links else []) + (args.source or [])))
    if args.exclude:
        urls = [u for u in urls if not any(x in u for x in args.exclude)]
    if not urls:
        print("No sources: add links to the draft or pass --source URL.", file=sys.stderr)
        return 2
    cache = None if args.no_cache else Path(args.cache)
    sources, failed = {}, []
    for u in urls:
        try:
            t = fetch(u, cache)
            if len(t) > 200:
                sources[u] = t
            else:
                failed.append((u, "page has almost no text"))
        except Exception as e:  # noqa: BLE001
            failed.append((u, str(e)[:120]))
    for u, why in failed:
        print(f"  ! source skipped: {u} ({why})", file=sys.stderr)
    if not sources:
        print("None of the sources could be fetched.", file=sys.stderr)
        return 2
    src_norm = {u: norm(t) for u, t in sources.items()}
    key = os.environ.get(args.key_env)
    m = Model(args.base_url, args.model, key)
    t0 = time.time()
    claims = extract_claims(m, draft, args.max_claims)
    print(f"{len(claims)} claims, {len(sources)} sources", file=sys.stderr)
    index = Index(sources)
    results = []
    for i, c in enumerate(claims, 1):
        r = verify(m, c["claim"], sources, src_norm, index, c["quote"])
        results.append({**c, **r})
        print(f"  [{i}/{len(claims)}] {r['verdict']:<12} {c['claim'][:90]}", file=sys.stderr)
    stats = {"model": args.model, "calls": m.calls, "prompt_tokens": m.prompt_tokens,
             "completion_tokens": m.completion_tokens, "seconds": time.time() - t0,
             "sources_ok": len(sources), "sources_failed": len(failed)}
    md = report_md(args.draft, results, stats)
    if args.report:
        Path(args.report).write_text(md, encoding="utf-8")
    else:
        print(md)
    if args.json:
        Path(args.json).write_text(json.dumps({"stats": stats, "results": results, "failed_sources": failed}, indent=2), encoding="utf-8")
    bad = [r for r in results if r["verdict"] in args.fail_on]
    return 1 if bad else 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="claimcheck", description="Fact-check an AI-written draft against its sources with an open-weight model.")
    ap.add_argument("draft", help="markdown file")
    ap.add_argument("--source", action="append", help="extra source URL (repeatable)")
    ap.add_argument("--exclude", action="append", help="skip draft links containing this text (repeatable), e.g. your own domain")
    ap.add_argument("--no-links", action="store_true", help="ignore links inside the draft; use only --source")
    ap.add_argument("--base-url", default=os.environ.get("CLAIMCHECK_BASE_URL", DEFAULT_BASE))
    ap.add_argument("--model", default=os.environ.get("CLAIMCHECK_MODEL", DEFAULT_MODEL))
    ap.add_argument("--key-env", default="CLAIMCHECK_API_KEY", help="env var that holds the API key (none needed for Ollama)")
    ap.add_argument("--max-claims", type=int, default=40)
    ap.add_argument("--fail-on", nargs="+", default=["contradicted", "not_found"], choices=VERDICTS)
    ap.add_argument("--report", help="write the markdown report here instead of stdout")
    ap.add_argument("--json", help="also write machine-readable results")
    ap.add_argument("--cache", default=".claimcheck-cache")
    ap.add_argument("--no-cache", action="store_true")
    ap.add_argument("--version", action="version", version=__version__)
    args = ap.parse_args(argv)
    try:
        return run(args)
    except (RuntimeError, ValueError, OSError) as e:
        print(f"claimcheck: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
