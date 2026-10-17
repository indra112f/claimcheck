# Examples

Real runs from October 17, 2026 with `gemma-4-31B-it` on DigitalOcean serverless inference.

| File | What it is |
|---|---|
| `python315-draft.md` | A CoreMesh draft about upgrading to Python 3.15. The false `frozendict` sentence the AI writer produced was put back in on purpose. |
| `python315-draft-report.md` | claimcheck's report for it. The planted sentence is flagged. |
| `why-so-many-tokens-report.md` | Report for the published article "Why Claude Code Uses So Many Tokens". |
| `claude-limit-reset-report.md` | Report for "Claude Code Usage Limit Reached?" using only the links in the article. They point at documentation home pages, so nothing could be backed. |
| `claude-limit-reset-rightsources-report.md` | The same article checked with `--no-links` and the right support and docs pages passed as `--source`. |

Model output varies a little between runs even at temperature 0, so a re-run can list a slightly different set of claims.
