# claimcheck report: examples/python315-draft.md

- Claims checked: **28**
- Supported: **22** · Contradicted: **0** · Not found in sources: **6**
- Model: `gemma-4-31B-it` · 29 calls · 67,421 in / 4,008 out tokens · 303s
- Sources fetched: 4 (failed: 0)

## 1. [CHECK] The flag `-X warn_default_encoding` finds implicit-encoding calls.
> Draft: "on your current Python, run your test suite with `-X warn_default_encoding` to find every implicit-encoding call"

The passages mention EncodingWarning and default encoding, but not the -X warn_default_encoding flag.

## 2. [CHECK] On macOS 27.0, IDLE and tkinter applications may hang when a menu command opens a dialog.
> Draft: "on macOS 27.0, IDLE and other tkinter applications may hang when a menu command opens a dialog."

None of the provided passages mention macOS 27.0, IDLE, or tkinter application hangs.

## 3. [CHECK] In UTF-8 mode, `locale.getpreferredencoding(False)` returns UTF-8.
> Draft: "`locale.getpreferredencoding(False)` returns UTF-8 under UTF-8 mode"

Passages state UTF-8 mode affects the function, but not the specific return value.

## 4. [CHECK] The import system no longer calls `Loader.load_module()` in Python 3.15.
> Draft: "`Loader.load_module()` is no longer called by the import system"

The provided passages do not mention Loader.load_module() or its removal from the import system.

## 5. [CHECK] In Python 3.15, `EnumType.__members__` and `errno.errorcode` return `frozendict`.
> Draft: "The stdlib now returns `frozendict` from `EnumType.__members__` and `errno.errorcode` instead of `MappingProxyType` or `dict`"

EnumType.__members__ is mentioned, but errno.errorcode is not found in the provided passages.

## 6. [CHECK] The macOS installer for Python 3.15 supports macOS 10.15 and later.
> Draft: "The macOS installer supports macOS 10.15 and later"

None of the provided passages mention the macOS installer or its version support.

## 7. [OK] Python 3.15 uses UTF-8 as the default text encoding for files, stdio and pipes.
> Draft: "Python now uses UTF-8 as the default text encoding for files, stdio and pipes ([PEP 686](https://peps.python.org/pep-0686/))."
> Source (https://peps.python.org/pep-0686/): "With this change, Python consistently uses UTF-8 for default encoding of files, stdio, and pipes."

S1 and S2 confirm the scope of PEP 686 and its implementation in Python 3.15.

## 8. [OK] Python 3.15.0 was released as a stable release on October 9, 2026.
> Draft: "Python 3.15.0 shipped on October 9, 2026 as a stable release."
> Source (https://docs.python.org/3.15/whatsnew/3.15.html): "Python 3.15 was released on 9 October 2026."

S1 confirms both the date and that Python 3.15 is the latest stable release.

## 9. [OK] Official Windows 64-bit binaries for Python 3.15 use the tail-calling interpreter.
> Draft: "The official Windows 64-bit binaries now use the tail-calling interpreter"
> Source (https://docs.python.org/3.15/whatsnew/3.15.html): "The official Windows 64-bit binaries now use the tail-calling interpreter"

Directly stated in the Release changes section.

## 10. [OK] Official macOS binaries for Python 3.15 install free-threading support by default.
> Draft: "the official macOS binaries now install free-threading support by default."
> Source (https://docs.python.org/3.15/whatsnew/3.15.html): "The official macOS binaries now install free-threading support by default"

## 11. [OK] The `encoding="locale"` option was fixed in Python 3.11 to be honored in UTF-8 mode.
> Draft: "The `encoding="locale"` option is honored even in UTF-8 mode (that was fixed in 3.11 specifically so this upgrade could happen)."
> Source (https://peps.python.org/pep-0686/): "This issue was fixed in Python 3.11."

S1 explicitly states that TextIOWrapper should use locale encoding in UTF-8 mode and this was fixed in 3.11.

## 12. [OK] The function `locale.getencoding()` was introduced in Python 3.11.
> Draft: "`locale.getencoding()` exists since 3.11"
> Source (https://peps.python.org/pep-0686/): "This API was added in Python 3.11."

The text explicitly links the addition of locale.getencoding() to Python 3.11.

## 13. [OK] Calling `subprocess.run(..., text=True)` in Python 3.15 decodes pipes as UTF-8.
> Draft: "If you call `subprocess.run(..., text=True)` and parse the output of a Windows command-line tool, the pipe is now decoded as UTF-8."
> Source (https://peps.python.org/pep-0686/): "With this change, Python consistently uses UTF-8 for default encoding of files, stdio, and pipes."

PEP 686 makes UTF-8 the default for pipes starting in Python 3.15.

## 14. [OK] The environment variable `PYTHONUTF8=0` or the command line flag `-X utf8=0` disables the new UTF-8 default behavior.
> Draft: "you can turn the old behavior back on with `PYTHONUTF8=0` in the environment or `-X utf8=0` on the command line."
> Source (https://docs.python.org/3.15/whatsnew/3.15.html): "To retain the previous behaviour, Python’s UTF-8 mode may be disabled with the PYTHONUTF8=0 environment variable or the -X utf8=0 command-line option."

The passage confirms both the environment variable and command-line flag used to retain previous behavior.

## 15. [OK] AST node constructors in Python 3.15 raise `TypeError` for missing required args or unknown keyword args.
> Draft: "AST node constructors raise `TypeError` for missing required args or unknown keyword args"
> Source (https://docs.python.org/3.15/whatsnew/3.15.html): "The constructors of AST nodes now raise a TypeError when a required argument is omitted or when a keyword argument that does not map to a field on the AST node is passed."

## 16. [OK] In Python 3.15, `datetime.strptime()` raises `ValueError` if `%d` is used without a year directive.
> Draft: "`datetime.strptime()` with `%d` but no year directive raises `ValueError`"
> Source (https://docs.python.org/3.15/whatsnew/3.15.html): "strptime() now raises ValueError when the format string contains %d (day of month) without a year directive."

Directly supports the claim.

## 17. [OK] frozendict is a new built-in immutable mapping in Python 3.15 that inherits from `object` and implements the `Mapping` protocol.
> Draft: "**frozendict** is a new built-in immutable mapping ([PEP 814](https://peps.python.org/pep-0814/)). It's not a `dict` subclass; it inherits from `object` and implements the `Mapping` protocol."
> Source (https://peps.python.org/pep-0814/): "The proposed frozendict type: implements the collections.abc.Mapping protocol, supports pickling."

S4 confirms it implements the Mapping protocol; S1/S3/S4 confirm it inherits from object and is not a dict subclass.

## 18. [OK] frozendict is hashable when its values are hashable.
> Draft: "it preserves insertion order, pickles, and is hashable when its values are hashable"
> Source (https://peps.python.org/pep-0814/): "Using hashable values creates a hashable frozendict."

Passages S1, S2, S5 and S6 all confirm hashability depends on values being hashable.

## 19. [OK] CPython's `frozendict.copy()` returns the same object.
> Draft: "`frozendict.copy()` returns the same object in CPython"
> Source (https://peps.python.org/pep-0814/): "In CPython, it simply returns the same frozendict (new reference)."

## 20. [OK] The `eval()` and `exec()` functions accept `frozendict` for `globals` in Python 3.15.
> Draft: "`eval()` and `exec()` accept a `frozendict` for `globals`."
> Source (https://docs.python.org/3.15/whatsnew/3.15.html): "eval() and exec() accept frozendict for globals, and type() and str.maketrans() accept frozendict for dict."

## 21. [OK] sentinel is a new built-in type introduced in Python 3.15 (PEP 661).
> Draft: "**sentinel** is also a new built-in type (PEP 661)"
> Source (https://docs.python.org/3.15/whatsnew/3.15.html): "PEP 661: Add sentinel built-in type"

The text matches the PEP number and the addition of the sentinel built-in type.

## 22. [OK] Python 3.15 introduces the `lazy` soft keyword for explicit lazy imports.
> Draft: "**Explicit lazy imports** add a `lazy` soft keyword ([PEP 810](https://peps.python.org/pep-0810/))."
> Source (https://docs.python.org/3.15/whatsnew/3.15.html): "Neither star imports nor future imports can be lazy (lazy from module import * and lazy from __future__ import ... both raise SyntaxError)."

Passage S6 explicitly mentions the use of the 'lazy' keyword for imports.

## 23. [OK] Python 3.15 honors the `__lazy_modules__` global for lazy imports.
> Draft: "use the `__lazy_modules__` global, which 3.15 honors and older versions ignore"
> Source (https://peps.python.org/pep-0810/): "On Python versions before 3.15 that don’t support lazy imports, the __lazy_modules__ attribute is simply ignored and imports proceed eagerly as normal."

The text confirms 3.15+ honors it and older versions ignore it.

## 24. [OK] Python 3.15 supports unpacking in comprehensions using `*` for iterables and `**` for mappings.
> Draft: "**Unpacking in comprehensions** (PEP 798) lets you write `[*xs for xs in items]` ... with `*` for iterables and `**` for mappings."
> Source (https://docs.python.org/3.15/whatsnew/3.15.html): "List, set, and dictionary comprehensions, as well as generator expressions, now support unpacking with * and **."

The draft text's claims about PEP 798 and the use of * and ** are confirmed.

## 25. [OK] The experimental JIT reports a 7-8% geometric mean improvement over the standard interpreter on x86-64 Linux.
> Draft: "the pyperformance suite reports a 7-8% geometric mean improvement for the JIT over the standard interpreter on x86-64 Linux"
> Source (https://docs.python.org/3.15/whatsnew/3.15.html): "Results from the pyperformance benchmark suite report a 7-8% geometric mean performance improvement for the JIT over the standard CPython interpreter built with all optimizations enabled on x86-64 Linux."

## 26. [OK] The experimental JIT reports an 11-12% speedup over the tail-calling interpreter on AArch64 macOS.
> Draft: "an 11-12% speedup over the tail-calling interpreter on AArch64 macOS."
> Source (https://docs.python.org/3.15/whatsnew/3.15.html): "On AArch64 macOS, the JIT has an 11-12% speedup over the tail calling interpreter with all optimizations enabled."

## 27. [OK] Building CPython with the JIT enabled requires LLVM 21 at build time.
> Draft: "If you build CPython yourself with the JIT enabled, you'll need LLVM 21 at build time"
> Source (https://docs.python.org/3.15/whatsnew/3.15.html): "As always, LLVM is only needed when building CPython with the JIT enabled;"

S1 explicitly links LLVM 21 as a build-time dependency for CPython JIT builds.

## 28. [OK] GDB and GNU `backtrace()` can unwind through JIT frames on supported Linux ELF platforms.
> Draft: "GDB and GNU `backtrace()` can now unwind through JIT frames on supported Linux ELF platforms"
> Source (https://docs.python.org/3.15/whatsnew/3.15.html): "This allows native debuggers, crash handlers, and diagnostic tools using these mechanisms to unwind through JIT frames instead of stopping at generated code."

The passage confirms support for both GDB and GNU backtrace() on supported Linux ELF platforms.
