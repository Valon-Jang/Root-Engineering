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

## Initial concurrency recommendation

Do not start by maximizing the configurable limit. Benchmark 1, 2, 3, 5, and 6 simultaneous children first, with quality, wall-clock, provider-token cost, resource use, and thread reclamation measured separately. V2 should be tested with explicit awareness that the configured concurrency includes the root agent.

## Sources

- OpenAI Codex source tag `rust-v0.147.0`, `codex-rs/core/src/config/mod.rs`
- OpenAI Codex source tag `rust-v0.147.0`, `codex-rs/core/config.schema.json`
- OpenAI Codex current `codex-rs/core/src/agent/registry.rs`
- Public Codex issue reproductions for 0.147.0 multi-agent configurations and thread-lifecycle behavior

## Next experiment

Enable the native multi-agent lane in an isolated Human Codex candidate configuration, then verify:

1. one bounded Child can be spawned and returns to the parent;
2. model / reasoning effort can be constrained;
3. inherited context can be minimized (`fork_turns` behavior);
4. 1/2/3/5/6 concurrent Child runs complete correctly;
5. completed threads release capacity;
6. the Child lane beats Carrier-direct handling on a narrow ambiguity task after counting all model-visible/provider tokens.
