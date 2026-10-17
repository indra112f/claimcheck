# claimcheck report: examples/why-so-many-tokens.md

- Claims checked: **29**
- Supported: **23** · Contradicted: **0** · Not found in sources: **6**
- Model: `gemma-4-31B-it` · 30 calls · 69,121 in / 4,072 out tokens · 189s
- Sources fetched: 5 (failed: 0)

## 1. [CHECK] The cache lifetime for subscriptions is one hour as of October 16, 2026.
> Draft: "As of October 16, 2026, the costs page lists the lifetime as an hour on a subscription"

The passages mention the lifetime is an hour, but do not mention the date October 16, 2026.

## 2. [CHECK] Rules in .claude/rules/ without a paths field load unconditionally.
> Draft: "rules in .claude/rules/ without a paths field load unconditionally"

Passages discuss skill frontmatter and paths, but not rules in .claude/rules/ specifically.

## 3. [CHECK] Path-scoped rules load when Claude uses Read, Write, Edit, or a Bash command that counts as a read (like cat or head) on a matching file.
> Draft: "a path-scoped rule only loads when Claude uses Read, Write or Edit on a matching file, or views it with a Bash command that counts as a read, such as cat or head on a single file."

The passages mention that skills load automatically when working with matching paths, but not the specific tools.

## 4. [CHECK] Personal rules in ~/.claude/rules/ load before project rules.
> Draft: "Personal rules in ~/.claude/rules/ load before project rules"

The passages discuss settings and skills, but do not mention a ~/.claude/rules/ folder or rules loading order.

## 5. [CHECK] Claude reads AGENTS.md instead of CLAUDE.md if AGENTS.md is present and CLAUDE.md is not, starting in v2.1.277.
> Draft: "If your repository has an AGENTS.md and no CLAUDE.md, Claude reads the AGENTS.md instead, which takes v2.1.277 or later."

The passages mention CLAUDE.md and v2.1.277, but not AGENTS.md or this fallback behavior.

## 6. [CHECK] All four mentioned models have a 1M-token context window.
> Draft: "All four models have a 1M-token context window"

The passages mention 1M context for some models, but not specifically 'all four' mentioned models.

## 7. [OK] The cache lifetime for usage credits, API keys, or cloud providers is five minutes by default.
> Draft: "dropping to five minutes once you're drawing on usage credits. On an API key or a cloud provider it's five minutes by default."
> Source (https://code.claude.com/docs/en/costs): "The lifetime is an hour on a subscription and drops to five minutes once you’re drawing on usage credits; on an API key or cloud provider, it’s five minutes by default."

The passage explicitly confirms the five-minute lifetime for all three mentioned scenarios.

## 8. [OK] The minimum cacheable length for Claude Fable 5.1, Opus 5.5, Sonnet 5.5, and Haiku 5.5 is 512 tokens.
> Draft: "The minimum cacheable length is 512 tokens for Claude Fable 5.1, Opus 5.5, Sonnet 5.5 and Haiku 5.5."
> Source (https://docs.claude.com/en/docs/build-with-claude/prompt-caching): "512 tokens for Claude Fable 5.1, Claude Mythos 5.1, Claude Opus 5.5, Claude Opus 5, Claude Sonnet 5.5, Claude Fable 5, Claude Mythos 5, and Claude Haiku 5.5"

The passage lists all four models mentioned in the draft as having a 512 token minimum.

## 9. [OK] On the API, total input is the sum of cache_read_input_tokens, cache_creation_input_tokens, and input_tokens.
> Draft: "If you're on the API, the usage object tells you what happened: cache_read_input_tokens, cache_creation_input_tokens and input_tokens add up to total input."
> Source (https://docs.claude.com/en/docs/build-with-claude/prompt-caching): "total_input_tokens = cache_read_input_tokens + cache_creation_input_tokens + input_tokens"

## 10. [OK] The /usage command on Pro, Max, Team, or Enterprise plans flags behaviors accounting for 10% or more of recent usage.
> Draft: "On a Pro, Max, Team or Enterprise plan, the /usage breakdown flags any behavior that accounts for 10% or more of your recent usage"
> Source (https://code.claude.com/docs/en/costs): "On a Pro, Max, Team, or Enterprise plan, the /usage breakdown flags behaviors that account for 10% or more of your recent usage, such as long context or cache misses, each with a tip to reduce it."

The draft text is directly supported by the passage.

## 11. [OK] CLAUDE.md is loaded into the conversation at the start of every session.
> Draft: "CLAUDE.md is loaded into the conversation at the start of every session"
> Source (https://code.claude.com/docs/en/costs): "Your CLAUDE.md file is loaded into context at session start."

## 12. [OK] Invoking a skill adds the rendered SKILL.md as a single message to the conversation.
> Draft: "when you or Claude invoke a skill, the rendered SKILL.md enters the conversation as a single message and stays there across later turns."
> Source (https://code.claude.com/docs/en/skills): "When you or Claude invoke a skill, the rendered SKILL.md content enters the conversation as a single message and stays there across later turns."

The draft text matches the source passage exactly.

## 13. [OK] The 'disable-model-invocation: true' frontmatter or 'user-invocable-only' in skillOverrides prevents Claude from invoking a skill on its own.
> Draft: "Stop Claude from invoking a skill on its own with `disable-model-invocation: true` in its frontmatter, or "user-invocable-only" in skillOverrides."
> Source (https://code.claude.com/docs/en/skills): "To keep a personal or project skill but stop Claude from invoking it on its own, set disable-model-invocation: true in its frontmatter, or "user-invocable-only" in skillOverrides when you don’t want to edit the file."

The passage explicitly confirms both methods for stopping Claude from invoking a skill on its own.

## 14. [OK] Setting disableBundledSkills to true turns off bundled skills.
> Draft: "Turn off bundled skills you never use by setting disableBundledSkills to true"
> Source (https://code.claude.com/docs/en/skills): "Bundled skill: set disableBundledSkills to true to turn off bundled skills, or set one skill to "off" in skillOverrides to hide it."

## 15. [OK] Setting "off" in skillOverrides hides a single bundled skill.
> Draft: "hide a single one with "off" in skillOverrides."
> Source (https://code.claude.com/docs/en/skills): "Bundled skill: set disableBundledSkills to true to turn off bundled skills, or set one skill to "off" in skillOverrides to hide it."

## 16. [OK] Compaction keeps the first 5,000 tokens of the most recent invocation of each skill, up to a combined 25,000-token budget.
> Draft: "After a summary, Claude Code re-attaches the most recent invocation of each skill, keeping the first 5,000 tokens of each, within a combined 25,000-token budget"
> Source (https://code.claude.com/docs/en/skills): "When the conversation is summarized to free context, Claude Code re-attaches the most recent invocation of each skill after the summary, keeping the first 5,000 tokens of each. Re-attached skills share a combined budget of 25,000 tokens."

The draft text accurately reflects the process and token limits described in the passage.

## 17. [OK] The tool-use system prompt costs 286 tokens on Claude Opus 5.5, Sonnet 5.5, and Haiku 5.5 with default tool choice.
> Draft: "a tool-use system prompt that costs 286 tokens on Claude Opus 5.5, Sonnet 5.5 and Haiku 5.5 with the default tool choice."
> Source (https://docs.claude.com/en/docs/about-claude/pricing): "Claude Haiku 5.5For high-volume, latency-sensitive tasks such as classification, extraction, and routing
auto, none
286 tokens"

S2 lists 286 tokens for auto/none (default) for Opus 5.5, Sonnet 5.5, and Haiku 5.5.

## 18. [OK] Setting crossSessionInbound to 'hold' prevents cross-session messages from being delivered as new turns.
> Draft: "Set crossSessionInbound to hold"
> Source (https://code.claude.com/docs/en/costs): "To hold inbound messages instead of delivering them, set crossSessionInbound to hold"

## 19. [OK] Goal check-ins are limited to at most three idle check-ins per goal since v2.1.246.
> Draft: "Claude is asked to check on it even when idle, at most three idle check-ins per goal since v2.1.246"
> Source (https://code.claude.com/docs/en/costs): "Claude Code starts at most three idle check-ins per goal between your prompts. Before v2.1.246, idle check-ins were uncapped."

The passage confirms the limit and the version change.

## 20. [OK] Setting CLAUDE_CODE_GOAL_CHECKIN_MINUTES to 0 disables idle goal check-ins.
> Draft: "Set CLAUDE_CODE_GOAL_CHECKIN_MINUTES to 0"
> Source (https://code.claude.com/docs/en/costs): "To turn check-ins off, set CLAUDE_CODE_GOAL_CHECKIN_MINUTES to 0."

The draft text matches the instruction for turning off check-ins found in the passage.

## 21. [OK] Idle goal check-ins require v2.1.236 or later.
> Draft: "Idle goal check-ins require v2.1.236 or later"
> Source (https://code.claude.com/docs/en/costs): "Idle check-ins require Claude Code v2.1.236 or later"

## 22. [OK] As of October 16, 2026, the input rate for Claude Fable 5.1 is $10 per million tokens and the output rate is $50.
> Draft: "Claude Fable 5.1 | $10 | $50"
> Source (https://docs.claude.com/en/docs/build-with-claude/prompt-caching): "Claude Fable 5.1For demanding reasoning and long-horizon agentic work $10 / MTok $50 / MTok"

Passage S1 lists Claude Fable 5.1 with input $10/MTok and output $50/MTok.

## 23. [OK] As of October 16, 2026, the input rate for Claude Opus 5.5 is $4 per million tokens and the output rate is $20.
> Draft: "Claude Opus 5.5 | $4 | $20"
> Source (https://docs.claude.com/en/docs/about-claude/pricing): "Claude Opus 5.5For long-running agentic coding and knowledge work $4 / MTok $20 / MTok"

The rates match $4 input and $20 output per million tokens.

## 24. [OK] As of October 16, 2026, the input rate for Claude Sonnet 5.5 is $2 per million tokens and the output rate is $10.
> Draft: "Claude Sonnet 5.5 | $2 | $10"
> Source (https://docs.claude.com/en/docs/about-claude/pricing): "Claude Sonnet 5.5The best combination of speed and intelligence $2 / MTok $10 / MTok"

The draft text aligns with the pricing table in S1 for Claude Sonnet 5.5.

## 25. [OK] As of October 16, 2026, the input rate for Claude Haiku 5.5 starts from $0.10 per million tokens and the output rate from $0.50.
> Draft: "Claude Haiku 5.5 | From $0.10 | From $0.50"
> Source (https://docs.claude.com/en/docs/about-claude/pricing): "Claude Haiku 5.5For high-volume, latency-sensitive tasks such as classification, extraction, and routing $0.10 / MTokfor prompts up to 100,000 tokens $0.50 / MTok"

Input starts at $0.10 and output is $0.50 for prompts up to 100k tokens.

## 26. [OK] Claude Opus 5.5 cache reads are priced at the input rate times 0.05.
> Draft: "the pricing page's worked example for a one-hour Claude Opus 5.5 session prices cache reads at the input rate times 0.05."
> Source (https://docs.claude.com/en/docs/about-claude/pricing): "Cache read tokens
40,000 × $4 × 0.05 / 1,000,000"

The calculation in the worked example uses the input rate ($4) multiplied by 0.05.

## 27. [OK] Claude 4.7 and later models produce approximately 30 percent more tokens for the same text than earlier models.
> Draft: "Claude 4.7 and later models use a newer tokenizer that produces approximately 30 percent more tokens for the same text than earlier models."
> Source (https://docs.claude.com/en/docs/about-claude/pricing): "Claude 4.7 and later models and Claude Mythos Preview use a newer tokenizer that produces approximately 30 percent more tokens for the same text than earlier models."

The draft text is directly supported by the passage.

## 28. [OK] The /clear command removes context between tasks.
> Draft: "Running /clear between unrelated tasks costs nothing."
> Source (https://code.claude.com/docs/en/costs): "When you want a fresh start instead of continuity, /clear costs nothing"

## 29. [OK] The /compact command reads the whole conversation to summarize it.
> Draft: "/compact reads the whole conversation it summarizes"
> Source (https://code.claude.com/docs/en/costs): "Compaction: /compact reads the conversation it summarizes, so compacting a large context is itself a large request."

The text explicitly confirms that /compact reads the conversation it summarizes.
