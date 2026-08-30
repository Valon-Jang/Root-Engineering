# Codex Child-Agent Capability Check — 2026-08-30

Status: Experimental research checkpoint

## Question

Can the Child / subagent mechanism observed around Human Codex be used deliberately, and is the previously observed five-worker count a hard child-agent limit?

## Result

Yes for the Codex / Human Codex engine path, but not as a directly exposed tool in the current ordinary ChatGPT conversation surface.

The previously used five Interceptors were deterministic Python/OS workers and do not establish a five-child LLM limit.

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

## Runtime evidence / boundary

Recent public 0.147.0 reports show working `spawn_agent` usage with explicit concurrency settings above five, including `max_concurrent_threads_per_session = 6`, and a V2 reproduction configured at 30. Other reports show much higher values such as 128 can create severe resource and lifecycle pressure; a large accepted configuration value should not be confused with a safe operating value.

Human Codex captured sessions currently show `multi_agent_version: disabled`, so the current Human Codex configuration does not expose the native child-agent lane yet even though its 0.147.0 engine contains the capability.

## Practical interpretation for Carrier research

There are now three distinct execution layers:

1. **Python Interceptors** — cheap deterministic work, existing five-worker implementation.
2. **Codex Child agents** — real model/provider threads available when multi-agent is enabled.
3. **Carrier** — primary reasoning and final decision authority.

A Child should not replace all Interceptors. The most promising first experiment is an exception/ambiguity lane:

`deterministic Interceptor -> ambiguous case -> one Child -> unresolved/high-impact case -> Carrier`

This preserves the Shadow Carrier efficiency target while allowing a small amount of real model judgment below the Carrier.

## Next concurrency experiment

The next runtime benchmark should now test actual authenticated provider Children at:

`1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 7 -> 8 -> 9 -> 10 -> 11 -> 12`

Measure separately:

- spawn success / AgentLimitReached or other error,
- number of simultaneously active provider threads,
- completion success,
- wall-clock time,
- provider/model token usage,
- quality,
- resource use,
- thread-slot reclamation after completion.

V2 tests must remember that the configured total includes the root agent; to obtain 12 V2 Children, total concurrency must be configured as 13.

## Sources

- OpenAI Codex source tag `rust-v0.147.0`, `codex-rs/core/src/config/mod.rs`
- OpenAI Codex source tag `rust-v0.147.0`, `codex-rs/core/config.schema.json`
- OpenAI Codex source tag/current `codex-rs/core/src/agent/registry.rs`
- GitHub Actions run `33292022259` in `Valon-Jang/Root-Engineering`

## Current conclusion

**Twelve is permitted by the 0.147.0 configuration/source gate. The real safe/effective provider concurrency limit is still unmeasured.**
