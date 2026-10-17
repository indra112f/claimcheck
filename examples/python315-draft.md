Upgrading to Python 3.15 is mostly painless, with one exception. Python now uses UTF-8 as the default text encoding for files, stdio and pipes ([PEP 686](https://peps.python.org/pep-0686/)). If you run on Windows, or you read data written in a legacy encoding, any `open()` call without an explicit `encoding=` can start raising errors or producing garbled text. Test for that first, then upgrade.

The short version: on your current Python, run your test suite with `-X warn_default_encoding` to find every implicit-encoding call and fix them, check that your dependencies support 3.15, create a fresh virtual environment on 3.15, and run the suite again. Below are the details for each step, the removed APIs that now raise instead of warn, and the new features (frozendict, lazy imports, unpacking in comprehensions) worth using once you're there.

## Should you upgrade to Python 3.15 right now

Python 3.15.0 shipped on October 9, 2026 as a stable release. For a new project, I'd start on 3.15 without hesitation. For an existing codebase, the answer depends on two things: whether your code relies on the platform default encoding, and whether your dependencies have caught up.

Two packaging changes are easy to miss. The official Windows 64-bit binaries now use the tail-calling interpreter, and the official macOS binaries now install free-threading support by default. Both are worth knowing if you file bug reports or compare performance.

One platform warning from the release notes: on macOS 27.0, IDLE and other tkinter applications may hang when a menu command opens a dialog. This is an operating system behavior change that affects all current Tk versions, not something specific to 3.15. If you depend on Tk apps on a Mac, hold off on macOS 27.0 or test your workflow first.

## The UTF-8 default is the change most likely to bite

Before 3.15, the default text encoding depended on the locale. Most Unix systems already use a UTF-8 locale, and Python already switched on UTF-8 mode when the locale was C or POSIX, so Linux and macOS users rarely noticed. Windows was different: the default was the legacy code page, so a bare `open("report.txt")` read the system's ANSI code page (cp1252 on most English-language Windows installs).

In 3.15, UTF-8 mode is on everywhere. The same bare `open()` now reads UTF-8. That's the right default, and it matches Node.js, Go, Rust and Java, but if the file was written by an older tool in the legacy code page, you get one of three outcomes: a `UnicodeDecodeError`, mojibake, or silent data corruption on round trips.

Here's what the mojibake case looks like. The bytes are the same; only the decoder's assumption changes:

```python run
text = "café costs 5€"
legacy_bytes = text.encode("cp1252")   # written by an old Windows tool

print("decoded as utf-8: ", legacy_bytes.decode("utf-8", errors="replace"))
print("decoded as cp1252:", legacy_bytes.decode("cp1252"))
```

The fix is to stop relying on the default at all. Three patterns cover almost every case:

```python
# 1. You know the file is UTF-8 (JSON, TOML, Markdown, source code). Say so.
with open("config.json", encoding="utf-8") as f:
    config = f.read()

# 2. The file was written by a local tool in the system's locale encoding.
with open("legacy_export.csv", encoding="locale") as f:
    rows = f.read()

# 3. You were calling locale.getpreferredencoding() to pick an encoding.
import locale
enc = locale.getencoding()   # locale encoding, ignores UTF-8 mode
```

The `encoding="locale"` option is honored even in UTF-8 mode (that was fixed in 3.11 specifically so this upgrade could happen). And `locale.getencoding()` exists since 3.11 for the same reason: `locale.getpreferredencoding(False)` returns UTF-8 under UTF-8 mode, so it can no longer tell you what the system locale is.

The same rule applies to subprocesses. If you call `subprocess.run(..., text=True)` and parse the output of a Windows command-line tool, the pipe is now decoded as UTF-8. Pass `encoding="utf-8"` or `encoding="locale"` explicitly. PEP 686 considered using `PYTHONIOENCODING` as the pipe default and rejected it, so there's no shortcut. If you already wrap commands with timeouts, see the [subprocess timeout examples](/python-subprocess-timeout/) for the surrounding pattern.

If you need time, you can turn the old behavior back on with `PYTHONUTF8=0` in the environment or `-X utf8=0` on the command line. Treat that as a migration aid, not a fix.

## How to test for encoding problems before you upgrade

PEP 686 spells out a procedure, and it works on the Python you're running today. The idea is to make every implicit-encoding call visible, fix it, then run under UTF-8 mode to confirm nothing changed.

```bash
# Step 1: find every place the default encoding is used.
# EncodingWarning is raised by open() and locale.getpreferredencoding().
python -X warn_default_encoding -W error::EncodingWarning -m pytest

# Step 2: fix each call site with encoding="utf-8" or encoding="locale".

# Step 3: run the suite with UTF-8 mode forced on, still on your current Python.
PYTHONUTF8=1 python -m pytest
```

Turning the warning into an error is deliberate. A warning scrolls past; an error gives you a traceback at the exact `open()` call. Run it once with `-W error` to get the list, then fix them in bulk.

Step 3 is the real preview. If the suite passes with `PYTHONUTF8=1` on 3.14, the encoding change in 3.15 is a non-event for you. If it fails, the failures point at files or pipes that carry legacy-encoded data, and those need `encoding="locale"` or a conversion step.

On Windows, run this on a real Windows machine or CI runner. Testing only on Linux proves nothing, because Linux was already UTF-8.

## Removed APIs that now raise errors

Everything in this table was deprecated earlier and is gone in 3.15. The full list is in the [What's new in Python 3.15](https://docs.python.org/3.15/whatsnew/3.15.html) page.

| Removed or changed | What to use instead |
|---|---|
| AST node constructors raise `TypeError` for missing required args or unknown keyword args | Pass every required field; drop keywords that aren't fields (was a `DeprecationWarning` since 3.13) |
| `datetime.strptime()` with `%d` but no year directive raises `ValueError` | Add a year directive to the format string |
| `glob.glob0()` and `glob.glob1()` | `glob.glob()` with the `root_dir` argument |
| `http.server.CGIHTTPRequestHandler` and the `--cgi` flag | Removed; What's new lists no direct replacement |
| `Loader.load_module()` is no longer called by the import system | Implement `exec_module()` on custom loaders |
| `importlib.resources.files(package=...)` keyword | Pass the package positionally: `files("mypkg")` |
| `pathlib.PurePath.is_reserved()` | `os.path.isreserved()` on Windows |
| `ctypes.SetPointerType()` | Removed, undocumented |
| `collections.abc.ByteString` dropped from `__all__` | Still importable until its removal in 3.17; stop using it now |

The `strptime` one catches people who parse log lines like `"%m/%d %H:%M"`. That worked with a warning on 3.13 and 3.14. On 3.15 it's a `ValueError`.

The custom-loader change is easy to miss because it lives in code you rarely touch: the import system no longer calls `load_module()`, so any custom loader that only implements the old method needs an `exec_module()` before you upgrade.

## New syntax and built-ins you can start using

Once the suite is green, these four features are the ones most likely to change how you write day-to-day code.

**frozendict** is a new built-in immutable mapping ([PEP 814](https://peps.python.org/pep-0814/)). It's not a `dict` subclass; it inherits from `object` and implements the `Mapping` protocol. It preserves insertion order, pickles, and is hashable when its values are hashable, which makes it usable as a dict key, a set member, a safe function default, and an argument to `functools.lru_cache()`-decorated functions.

```python
DEFAULTS = frozendict(retries=3, timeout=30)

def fetch(url, options=DEFAULTS):      # safe default, no mutable-default bug
    opts = {**DEFAULTS, **options}       # merge into a new dict
    ...

frozendict({"a": 1})                     # from a dict
frozendict([("a", 1), ("b", 2)])         # from key/value pairs
frozendict({"a": 1}, b=2)                # both
```

Construction from a dict is a shallow O(n) copy. `frozendict.copy()` returns the same object in CPython, and mutable values stay mutable, so use `copy.deepcopy()` if you need isolation. The stdlib now returns `frozendict` from `EnumType.__members__` and `errno.errorcode` instead of `MappingProxyType` or `dict`, and `eval()` and `exec()` accept a `frozendict` for `globals`.

**sentinel** is also a new built-in type (PEP 661), listed in the release highlights. The release notes don't spell out the API in the summary, so check the What's new page before using it.

**Explicit lazy imports** add a `lazy` soft keyword ([PEP 810](https://peps.python.org/pep-0810/)). The module is loaded on first use instead of at the import statement, which cuts startup time for CLIs and tools that import heavy libraries they only sometimes need.

```python
lazy import json
lazy from decimal import Decimal

def main(args):
    if args.pretty:
        print(json.dumps(data, indent=2))   # json is loaded here, not above
```

Two things to know. First, `lazy from module import Class` still executes the whole module on first access; there's no way to run part of a file. Second, for code that must also run on older versions, use the `__lazy_modules__` global, which 3.15 honors and older versions ignore:

```python
# Lazy on 3.15+, eager on older Python
__lazy_modules__ = ["json", "decimal"]
import json
from decimal import Decimal
```

**Unpacking in comprehensions** (PEP 798) lets you write `[*xs for xs in items]` where before you needed a double loop or `itertools.chain.from_iterable`. It works in list, set and dict comprehensions and in generator expressions, with `*` for iterables and `**` for mappings. Unpacking is restricted to the top level of the expression. This example runs on any Python 3 and uses the new syntax when it's available:

```python run
import sys

nested = [[1, 2, 3], [], [4, 5]]
try:
    flat = eval("[*xs for xs in nested]", {"nested": nested})
    how = "PEP 798 syntax"
except SyntaxError:
    flat = [x for xs in nested for x in xs]
    how = "double loop (Python %d.%d has no PEP 798)" % sys.version_info[:2]

print(flat, "via", how)
```

One readability trap: `f(*x for x in y)` means `f((*x for x in y))`, a single generator argument, not unpacked arguments. Add the parentheses yourself so the next reader doesn't have to think about it.

## What the experimental JIT does and doesn't give you

The JIT is still experimental and is not on in a default build. Per the What's new page, the pyperformance suite reports a 7-8% geometric mean improvement for the JIT over the standard interpreter on x86-64 Linux, and an 11-12% speedup over the tail-calling interpreter on AArch64 macOS. The spread across individual benchmarks goes from roughly a 15% slowdown to over 100% speedup, so your workload may land anywhere in that range.

The practical upshot: don't upgrade for the JIT. If you build CPython yourself with the JIT enabled, you'll need LLVM 21 at build time (end users running the resulting binary don't need LLVM). The new tracing frontend records real execution paths and handles object creation, overloaded operations and generators partially, which is why more code speeds up than in 3.14. GDB and GNU `backtrace()` can now unwind through JIT frames on supported Linux ELF platforms, so crash reports from JIT builds are no longer dead ends.

## How to install Python 3.15 on Windows, macOS and Linux

Installers come from the python.org download page for the 3.15.0 release.

**Windows.** The download page points to the Python install manager, and the Windows release manifest is installed with:

```powershell
py install 3.15
```

Traditional installers also exist: 64-bit (recommended), 32-bit and ARM64, plus embeddable packages for each if you're bundling Python into an application.

**macOS.** The macOS installer supports macOS 10.15 and later and, new in 3.15, installs free-threading support by default.

**Linux (including Ubuntu).** The download page lists source tarballs (gzipped and XZ compressed) but no Linux binaries. Your options are your distribution's packages once they ship 3.15, a tool that fetches prebuilt interpreters, or building from the tarball. The release announcement itself shows uv in action:

```bash
uvx --python 3.15 whatsnewt   # a TUI tour of the new features, run on 3.15
```

Whichever route you take on Linux, don't `pip install` into the system interpreter. If you hit the externally-managed-environment error, the [safe fix for that pip error](/externally-managed-environment-pip/) is a virtual environment, which is where the upgrade should live anyway.

After installing, create a clean environment with the new interpreter rather than pointing an old one at it:

```bash
python3.15 -m venv .venv
source .venv/bin/activate
python -m pip install -e . && python -m pytest
```

If you need a refresher on activation across shells, see [how to create and activate a Python virtual environment](/python-virtual-environment/).

## Common mistakes when upgrading

- **Setting `PYTHONUTF8=0` and forgetting it.** It silences the problem on one machine and moves the crash to CI or a colleague's laptop. Use it only while you fix call sites.
- **Assuming `encoding="locale"` means UTF-8.** It means the system locale encoding, which on Windows is the legacy code page. Use it only for files that really were written that way.
- **Testing only on Linux.** Linux was already UTF-8, so a green Linux run tells you nothing about Windows behavior.
- **Expecting `frozendict.copy()` to isolate mutable values.** It returns the same object. Reach for `copy.deepcopy()`.
- **Making a module lazy when its import has side effects.** Registration, logging setup or monkeypatching that used to happen at startup now happens on first use, or never. Keep those imports eager.
- **Parsing dates with `%d` and no year.** This is the removal most likely to appear in a production traceback, because it was only a warning before.
- **Reusing the old virtual environment.** Compiled extensions built for 3.14 won't load. Build a new one and reinstall.
- **Expecting a JIT speedup from the stock installer.** The JIT is experimental and the reported gains are for JIT-enabled builds.

If your code is async-heavy, the same rules apply inside coroutines; nothing in the UTF-8 change is specific to asyncio, but file and pipe reads in [async code](/python-async-await/) are just as affected.

## Upgrade checklist

1. On your current Python, run the suite with `-X warn_default_encoding -W error::EncodingWarning` and fix every reported call with an explicit `encoding=`.
2. Run the suite again with `PYTHONUTF8=1` set. Do this on Windows if you ship to Windows.
3. Grep for `strptime`, `glob0`, `glob1`, `load_module`, `is_reserved`, `CGIHTTPRequestHandler` and `ByteString` and replace them using the table above.
4. Check that each dependency with compiled extensions publishes a 3.15 build.
5. Install 3.15 and create a fresh virtual environment with `python3.15 -m venv`.
6. Install your project into it and run the full suite.
7. Only then adopt new features: `frozendict` for constants and defaults, `lazy import` for slow optional imports, `[*xs for xs in items]` for flattening.
8. Leave `PYTHONUTF8=0` out of your production configuration.