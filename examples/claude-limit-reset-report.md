# claimcheck report: examples/claude-limit-reset.md

- Claims checked: **12**
- Supported: **0** · Contradicted: **0** · Not found in sources: **12**
- Model: `gemma-4-31B-it` · 13 calls · 28,035 in / 1,281 out tokens · 59s
- Sources fetched: 4 (failed: 1)

## 1. [CHECK] The Claude Max plan has a 5-hour session limit and a weekly limit.
> Draft: "On Max there are two limits: a 5-hour session limit and a weekly limit."

The provided passages do not mention a 'Max' plan or its session/weekly limits.

## 2. [CHECK] Claude Max limits are shared between the worker, the user's chat, and Claude Code use.
> Draft: "Both are shared with your own chat and Claude Code use."

The provided passages do not mention 'Claude Max limits' or sharing of limits between chat and Claude Code.

## 3. [CHECK] The session limit resets on a 5-hour basis.
> Draft: "The session limit resets on a 5-hour basis"

None of the passages mention a session limit or a 5-hour reset period.

## 4. [CHECK] The weekly limit resets weekly.
> Draft: "the weekly limit resets weekly."

None of the provided passages mention a 'weekly limit' or how such a limit resets.

## 5. [CHECK] The command `claude -p` can return a limit message instead of the requested work.
> Draft: "A worker that shells out to `claude -p` gets a limit message back instead of the work it asked for."

The passages mention the `claude -p` command but do not mention limit messages.

## 6. [CHECK] The `/usage` command in an interactive Claude Code session shows current usage standing.
> Draft: "To see where you stand by hand, open an interactive Claude Code session and use the `/usage` command."

The provided passages do not mention a /usage command.

## 7. [CHECK] The flag `--output-format json` provides tokens, cache reads, turns, and duration per call.
> Draft: "So I switched every call to `--output-format json` and log tokens, cache reads, turns and duration per call into SQLite."

The provided passages do not mention the `--output-format json` flag or its specific output data.

## 8. [CHECK] Observed build durations range from 35 seconds to 5 minutes.
> Draft: "a build took 35 seconds to 5 minutes"

The provided passages discuss systemd timers and SQLite3, not build durations.

## 9. [CHECK] Observed review durations range from 13 seconds to 1 minute.
> Draft: "a review took 13 seconds to 1 minute."

None of the provided passages mention review durations or timing for reviews.

## 10. [CHECK] The Claude Code Limit Saver Kit costs $15.
> Draft: "We packaged the tools we use for this into the [Claude Code Limit Saver Kit](https://coremesh.gumroad.com/l/claude-code-limit-saver) ($15, our own product)"

The provided passages are documentation for Claude Code and do not mention the 'Limit Saver Kit'.

## 11. [CHECK] The Claude Code Limit Saver Kit provides a local usage report, a status line for 5-hour and weekly limits, and a hook to stop reads of large files.
> Draft: "a local usage report built from your Claude Code transcripts, a status line with your 5-hour and weekly limits, and a hook that stops whole reads of huge files."

The passages mention Claude Code, hooks, and usage monitoring, but not this specific kit.

## 12. [CHECK] The Python sqlite3 module is sufficient for logging the JSON result fields.
> Draft: "Python's built-in [sqlite3 module](https://docs.python.org/3/library/sqlite3.html) is enough"

The provided passages describe the module's functionality but do not state it is 'enough' for this purpose.
