# claimcheck

Fact-check an AI-written draft against **its own sources** with an open-weight model, before you publish it.

```
$ claimcheck examples/python315-draft.md --exclude coremesh.online
28 claims, 4 sources
  [1/28] supported    Python 3.15 uses UTF-8 as the default text encoding for files, stdio and pipes.
  ...
  [18/28] not_found    In Python 3.15, `EnumType.__members__` and `errno.errorcode` return `frozendict`.
```

That last line is a real mistake our blog's AI writer made: PEP 814 lists those two as *possible candidates*, not as shipped changes. claimcheck flagged it.

## How it works

1. **Claims.** The model lists the checkable claims in the draft: numbers, versions, limits, defaults, dates, "X supports Y". Every claim must quote the draft. A claim whose quote isn't in the draft is dropped.
2. **Retrieval.** Every source page linked in the draft (plus any `--source`) is fetched and split into passages. A small IDF-weighted lexical index picks the closest passages for each claim, with no embeddings and no vector DB.
3. **Verdict.** The model sees one claim and those passages only, and answers `supported`, `contradicted` or `not_found`, copying the evidence sentence.
4. **Quote check.** The evidence must appear **word for word** in the fetched source (after normalizing quotes, dashes and whitespace). If it doesn't, the verdict is thrown away and becomes `not_found`. The model can't invent its proof.
5. **Number check.** For `supported`, every number in the draft's sentence (versions, limits, prices) must appear in the evidence or the text around it. This was added after a run accepted "you'll need LLVM 21" with a quote that never mentions 21.

The report lists problems first. The exit code is `1` when anything needs a human, so it works as a CI or pre-publish gate.

## Install and run

Python 3.9+. Standard library only.

```bash
git clone https://github.com/indra112f/claimcheck && cd claimcheck
export CLAIMCHECK_API_KEY=...            # DigitalOcean model access key
python3 claimcheck.py draft.md --report report.md --json result.json
```

The default is **Gemma 4 (`gemma-4-31B-it`) on DigitalOcean serverless inference**. Any OpenAI-compatible endpoint works:

```bash
# fully local with Ollama (no key; the draft never leaves your machine)
python3 claimcheck.py draft.md --base-url http://localhost:11434/v1 --model gemma3:12b
```

The Ollama route uses the same OpenAI-compatible API, but the numbers below were measured on DigitalOcean only.

| Option | What it does |
|---|---|
| `--source URL` | add a source (repeatable) |
| `--exclude TEXT` | skip draft links containing TEXT, e.g. your own domain |
| `--no-links` | ignore links in the draft, use only `--source` |
| `--max-claims N` | default 40 |
| `--fail-on ...` | which verdicts fail the run (default: `contradicted not_found`) |

## Real runs (October 2026)

Three articles from [CoreMesh](https://coremesh.online), whose drafts are written by an AI pipeline:

| Draft | Claims | Supported | Flagged | Time | Tokens in / out |
|---|---|---|---|---|---|
| Python 3.15 upgrade (with the frozendict mistake put back) | 28 | 22 | 6, incl. the planted mistake | 303 s | 67.4k / 4.0k |
| Why Claude Code uses so many tokens | 29 | 23 | 6 | 189 s | 69.1k / 4.1k |
| Claude Code usage limit reset, its own links (docs home pages) | 12 | 0 | 12 | 59 s | 28.0k / 1.3k |
| Same article, right sources via `--source` | 10 | 3 | 7, mostly first-hand measurements | 47 s | 22.0k / 1.2k |

At DigitalOcean's listed Gemma 4 serverless rate ($0.18 per 1M input tokens and $0.50 per 1M output tokens, as of October 2026), a full article costs about **1.4 cents**.

The third row is a useful failure: that article links only to documentation **home pages**, so none of its claims could be backed by what it links to. The fix is better links, not a better model. Most flags left in the fourth row are the author's own measurements (build and review times), which no documentation can confirm.

Full reports are in [`examples/`](examples/).

## What "flagged" means

`not_found` means **your sources don't settle this**. It doesn't mean the claim is wrong. In the Python run, some flags are true statements from docs the draft never linked (for example `-X warn_default_encoding` lives in PEP 597). Either way a human should look: link the right source, or cut the sentence.

## Limits

- Retrieval is lexical. A claim worded very differently from its source can be missed, which shows up as `not_found`.
- Pages that need JavaScript to render, or that block scripts, come back empty and are skipped with a warning.
- Code blocks are ignored; test code by running it.
- The model can still be wrong about *meaning* even when its quote is real. The report shows the draft text and the source sentence side by side so you can judge in seconds.

## Tests

```bash
python3 -m unittest test_claimcheck.py
```

The tests run offline with a fake model. They cover quote matching, the fabricated-evidence downgrade, claim filtering, retrieval and report order.

## License

MIT
