#!/usr/bin/env python3
import json
import re
import urllib.request

TAG = "rust-v0.147.0"
BASE = f"https://raw.githubusercontent.com/openai/codex/{TAG}/"
URLS = {
    "config": BASE + "codex-rs/core/src/config/mod.rs",
    "schema": BASE + "codex-rs/core/config.schema.json",
    "registry": BASE + "codex-rs/core/src/agent/registry.rs",
}

def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "root-engineering-child-probe/0.1"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8")

config = fetch(URLS["config"])
schema_text = fetch(URLS["schema"])
registry = fetch(URLS["registry"])
schema = json.loads(schema_text)

m_v1 = re.search(r"DEFAULT_AGENT_MAX_THREADS:\s*Option<usize>\s*=\s*Some\((\d+)\)", config)
m_v2 = re.search(r"DEFAULT_MULTI_AGENT_V2_MAX_CONCURRENT_THREADS_PER_SESSION:\s*usize\s*=\s*(\d+)", config)
assert m_v1 and m_v2, "Could not locate concurrency defaults in exact 0.147.0 source"
v1_default = int(m_v1.group(1))
v2_total_default = int(m_v2.group(1))

agents = schema["definitions"]["AgentsToml"]["properties"]["max_concurrent_threads_per_session"]
assert agents.get("minimum") == 1.0
assert "maximum" not in agents, "Unexpected schema-level maximum found"

assert "fn try_increment_spawned(&self, max_threads: usize) -> bool" in registry
assert "if current >= max_threads" in registry

print(f"Codex tag: {TAG}")
print(f"V1 default child-thread cap: {v1_default}")
print(f"V2 default total active-agent slots: {v2_total_default} -> child slots {max(v2_total_default-1,0)}")
print("Schema maximum: NONE")
print()
print("requested,v1_child_slots,v2_total_slots,v2_child_slots,schema_accepts")
for n in range(1, 13):
    schema_accepts = n >= int(agents["minimum"]) and ("maximum" not in agents or n <= int(agents["maximum"]))
    print(f"{n},{n},{n},{max(n-1,0)},{str(schema_accepts).lower()}")

print("\nRESULT: CONFIG/SOURCE GATE PASS 1..12")
print("NOTE: This proves source/config acceptance and slot accounting only. It does NOT prove 12 simultaneous authenticated provider child turns complete successfully in Human Codex.")
