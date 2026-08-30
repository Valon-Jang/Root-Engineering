# Codex Child-Agent Capability Check — 2026-08-30

Status: Experimental research checkpoint

## Question

Can the Child / subagent mechanism observed around Human Codex be used deliberately, and is the previously observed five-worker count a hard child-agent limit?

## Result

Yes for the Codex / Human Codex engine path, but not as a directly exposed tool in the current ordinary ChatGPT conversation surface.

The previously used five Interceptors were deterministic Python/OS workers and do not establish a five-child LLM limit.

## Important distinction: two different Child mechanisms

Earlier Human Codex evidence confirms that a **separate ephemeral provider Thread actually executed** after a background completion path. The old flow marked every completed tracked test/build command `followup_state=pending`; Core then started a separate ephemeral provider Thread with a generic completion prompt. Because that prompt carried no useful exit-code/output details, the model sometimes returned a useless message equivalent to “no result details were provided.” This was a real provider/model Turn, not a Python worker.

That automatic background-completion trigger was later deliberately removed for routine completion, test PASS, and build success. Those cases now remain Tool Cards and do not launch a provider follow-up. Failure/result-unavailable/generated-result cases were also changed to deterministic notices rather than provider Turns. Therefore:

- the **ephemeral provider Thread capability was proven to work**;
- the old **routine background-completion auto-trigger is intentionally suppressed now**;
- suppressing that trigger does not prove the underlying provider Thread capability disappeared.

Independent Candidate E2E after these repairs still created a fresh ephemeral Thread using `gpt-5.6-sol` with `low` reasoning, completed one shell tool call and Turn, received assistant output, and exited without completion error. This confirms the underlying ephemeral Thread/provider execution path remained operational after the notification repair, even though the noisy routine-completion trigger was removed.

Do not conflate this historical ephemeral follow-up mechanism with Codex native multi-agent `spawn_agent`; whether they share an internal implementation path is not established.

## Codex 0.147.0 source evidence

The exact `rust-v0.147.0` source contains native multi-agent instructions and explicitly names these collaboration tools:

- `spawn_agent`
- `followup_task`
- `send_message`
- `wait_agent`
- `interrupt_agent`
- `list_agents`

The same version defines:

- `DEFAULT_AGENT_MAX_THREADS = Some(6)` for the V1/legacy child-thread limit when no override is supplied.
- `DEFAULT_MULTI_AGENT_V2_MAX_CONCURRENT_THREADS_PER_SESSION = 4` for V2 total active-agent slots.
- V2 effective child capacity is `max_concurrent_threads_per_session - 1` because the primary/root agent occupies one slot.

The config schema accepts `max_concurrent_threads_per_session` as an unsigned integer with minimum 1 and does not declare a schema-level maximum. Therefore 5 is not a source-level hard ceiling.

## Automated 1..12 source/config probe

A GitHub Actions probe was executed against the exact public `rust-v0.147.0` source rather than only reasoning from copied snippets.

Workflow run: `33292022259`  
Commit: `84c41467cd3de3c45f141db659e2f032ee2c47de`  
Conclusion: **success**

The probe downloaded the exact 0.147.0 config source, schema, and agent registry; verified the default constants, verified the absence of a schema-level maximum, verified the registry uses the configured `max_threads` value, and evaluated requested concurrency values 1 through 12.

| Requested setting | V1 child slots | V2 total slots | V2 child slots | Schema accepted |
|---:|---:|---:|---:|:---:|
| 1 | 1 | 1 | 0 | yes |
| 2 | 2 | 2 | 1 | yes |
| 3 | 3 | 3 | 2 | yes |
| 4 | 4 | 4 | 3 | yes |
| 5 | 5 | 5 | 4 | yes |
| 6 | 6 | 6 | 5 | yes |
| 7 | 7 | 7 | 6 | yes |
| 8 | 8 | 8 | 7 | yes |
| 9 | 9 | 9 | 8 | yes |
| 10 | 10 | 10 | 9 | yes |
| 11 | 11 | 11 | 10 | yes |
| 12 | 12 | 12 | 11 | yes |

Probe result: **CONFIG/SOURCE GATE PASS 1..12**.

Important boundary: this proves configuration acceptance and source-level slot accounting only. It does **not** yet prove that 12 simultaneous authenticated provider Child turns can complete successfully in Human Codex.

## Live provider probe attempt

A second GitHub Actions workflow attempted to proceed beyond source/config inspection and run an actual authenticated Codex provider test configured for **12 simultaneous V2 Children** (`max_concurrent_threads_per_session = 13`, including the root agent).

Workflow run: `33292209451`  
Commit: `5dee1565ac9232f38d5b304bd5a9b2250575c427`

The runner checked for an available Codex/OpenAI authentication route without printing any secret values. Results:

- `OPENAI_API_KEY`: absent
- `CODEX_AUTH_JSON`: absent
- `CHATGPT_AUTH_JSON`: absent
- current ChatGPT container: no `codex` binary and no `~/.codex` authenticated session

Therefore the provider step was correctly skipped with:

`PROVIDER_CHILD_LIVE_PROBE=BLOCKED_NO_CODEX_AUTH`

This is an **environment/auth boundary**, not a concurrency failure. No provider Child was actually spawned, so it must not be counted as a failed 12-Child runtime test.

The live-probe workflow remains at `.github/workflows/codex-child-provider-live-probe.yml`; if an authenticated Codex execution route is later attached to that runner, it is already configured to attempt 12 Child agents with minimal child tasks.

## Runtime evidence / boundary

Human Codex captured sessions currently show `multi_agent_version: disabled`, so the current Human Codex configuration does not expose the native `spawn_agent` lane even though its 0.147.0 engine contains the capability.

This does **not** contradict the earlier ephemeral provider-Thread evidence: the old background follow-up mechanism operated even with native multi-agent disabled, which is another reason to treat the two mechanisms separately until proven otherwise.

## Practical interpretation for Carrier research

There are now potentially four distinct execution layers/mechanisms:

1. **Python Interceptors** — cheap deterministic work, existing five-worker implementation.
2. **Ephemeral provider Thread** — historically proven real provider Turn, previously triggered by background follow-up; routine trigger now suppressed.
3. **Codex native Child agents** — `spawn_agent` multi-agent lane available when enabled.
4. **Carrier** — primary reasoning and final decision authority.

The most promising next experiment is to determine whether the proven ephemeral provider Thread can be invoked deliberately with a bounded prompt/result contract before introducing a wider native multi-agent pool.

## Next experiments

1. Reproduce one deliberately invoked ephemeral provider Thread in the authenticated Human Codex runtime and return a unique marker to the parent path.
2. Determine whether that path can accept an explicit prompt/context/model/effort and whether its result can be consumed programmatically rather than merely displayed.
3. Only then compare it with native `spawn_agent` and decide which mechanism is better suited to Shadow Carrier ambiguity resolution.
4. Separately, when native multi-agent is enabled, benchmark authenticated provider Children at `1 -> ... -> 12` and measure spawn success, simultaneous active threads, completion, wall-clock, tokens, quality, resources, and slot reclamation.

## Sources

- Human Codex self-repair/session evidence from 2026-08-28 through 2026-08-30
- OpenAI Codex source tag `rust-v0.147.0`, `codex-rs/core/src/config/mod.rs`
- OpenAI Codex source tag `rust-v0.147.0`, `codex-rs/core/config.schema.json`
- OpenAI Codex source tag/current `codex-rs/core/src/agent/registry.rs`
- GitHub Actions run `33292022259` in `Valon-Jang/Root-Engineering`
- GitHub Actions run `33292209451` in `Valon-Jang/Root-Engineering`

## Current conclusion

**The historical ephemeral Child/provider Thread definitely worked, and an independent ephemeral provider Thread still worked after the background-notification repair. What was disabled was the noisy automatic routine-completion trigger, not provider-Thread execution itself. Native `spawn_agent` remains a separate, not-yet-live-tested mechanism in this project.**
