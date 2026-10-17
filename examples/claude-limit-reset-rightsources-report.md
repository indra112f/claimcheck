# claimcheck report: examples/claude-limit-reset.md

- Claims checked: **10**
- Supported: **3** · Contradicted: **0** · Not found in sources: **7**
- Model: `gemma-4-31B-it` · 11 calls · 21,988 in / 1,215 out tokens · 47s
- Sources fetched: 5 (failed: 0)

## 1. [CHECK] The command `claude -p` is used by the worker to execute tasks.
> Draft: "A worker that shells out to `claude -p` gets a limit message back instead of the work it asked for."

The passages mention -p and spend limits, but not that -p specifically triggers a limit message.

## 2. [CHECK] The flag `--output-format json` causes the CLI to return JSON containing tokens, cache reads, turns, and duration.
> Draft: "So I switched every call to `--output-format json` and log tokens, cache reads, turns and duration per call into SQLite."

S2 mentions total_cost_usd for --output-format json, but not tokens, cache reads, turns, or duration.

## 3. [CHECK] Observed build times ranged from 35 seconds to 5 minutes.
> Draft: "a build took 35 seconds to 5 minutes"

None of the provided passages mention build times ranging from 35 seconds to 5 minutes.

## 4. [CHECK] Observed review times ranged from 13 seconds to 1 minute.
> Draft: "a review took 13 seconds to 1 minute."

The provided passages contain no information about the duration of reviews.

## 5. [CHECK] The Claude Code Limit Saver Kit provides a local usage report, a status line for 5-hour and weekly limits, and a hook to stop reads of large files.
> Draft: "a local usage report built from your Claude Code transcripts, a status line with your 5-hour and weekly limits, and a hook that stops whole reads of huge files."

The passages do not mention a 'Limit Saver Kit' or a hook to stop reading huge files.

## 6. [CHECK] The Claude Code Limit Saver Kit runs locally and does not upload data.
> Draft: "It runs on your machine and uploads nothing."

The passages discuss Claude Code costs and commands, but not a 'Limit Saver Kit'.

## 7. [CHECK] The suggested job states are PENDING, RUNNING, DONE, FAILED, and QUOTA_WAIT.
> Draft: "I'd define the states first: PENDING, RUNNING, DONE, FAILED and QUOTA_WAIT."

None of the passages mention these specific job states (PENDING, RUNNING, DONE, FAILED, QUOTA_WAIT).

## 8. [OK] The Claude Max plan has a 5-hour session limit and a weekly limit.
> Draft: "On Max there are two limits: a 5-hour session limit and a weekly limit."
> Source (https://support.claude.com/en/articles/11145838-use-claude-code-with-your-pro-or-max-plan): "Both Pro and Max plans have a five-hour session limit and a weekly limit."

The passage explicitly confirms both limits for Max plans.

## 9. [OK] Claude Max plan limits are shared between chat, Claude Code, and worker usage.
> Draft: "Both are shared with your own chat and Claude Code use."
> Source (https://support.claude.com/en/articles/11145838-use-claude-code-with-your-pro-or-max-plan): "These limits are shared across Claude and Claude Code, meaning all activity in both tools counts against the same limits."

Confirms usage limits are shared between Claude (chat) and Claude Code.

## 10. [OK] The `/usage` command in an interactive Claude Code session shows current usage status.
> Draft: "To see where you stand by hand, open an interactive Claude Code session and use the `/usage` command."
> Source (https://code.claude.com/docs/en/commands): "/stats
Alias for /usage. Opens on the Stats tab"

The text confirms /usage exists and relates to stats/usage via the /stats alias.
