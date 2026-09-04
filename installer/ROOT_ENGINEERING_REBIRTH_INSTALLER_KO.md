---
package_id: root-engineering-rebirth-chat-installer
package_version: 1.0.0
codename: Rebirth
schema_version: 1.0.0
release_date: 2026-09-04
target_environment: writable chat-local workspace를 가진 일반 ChatGPT Chat
primary_storage_adapter: chat-local-mnt
project_required: false
google_drive_required: false
single_file_package: true
supported_modes:
  - INSTALL
  - VERIFY
  - REPAIR
  - UPGRADE_FROM_DRIVE
  - EXPORT
  - COMPACT
three_layer_memory_model: transcript-active-context-local-root
checkpoint_owner: runtime/CHECKPOINT.md
context_epoch: true
compaction_transaction: persist-verify-compact-rehydrate
save_failure_blocks_compaction: true
native_compaction_policy: exposed-supported-only
boundary_fallback_policy: same-environment-verified-only
large_pressure_policy: diagnostic-only-bounded
external_storage_role: optional-backup-recovery-source
---

# ROOT ENGINEERING 1.0.0 — REBIRTH

> **Model is replaceable. Context is replaceable. Root persists.**
>
> **상태를 저장하고 → Context를 압축하고 → 작업을 복구해 → 같은 Chat을 계속 사용한다.**

이 파일은 Root Engineering 1.0.0 **Rebirth**의 Chat-native 한글 설치본이다.
일반 ChatGPT Chat에서 사용하며 ChatGPT Project나 Google Drive를 필수로 요구하지 않는다.

## 0. Rebirth 구조

장기 Chat에서 다음 세 계층을 분리한다.

```text
CHAT TRANSCRIPT
= 사람이 보는 과거 대화

ACTIVE MODEL CONTEXT
= 모델의 압축 가능한 작업 기억

LOCAL ROOT
= 현재 Chat Runtime 내부의 Canonical 프로젝트 상태
```

기본 경로:

```text
/mnt/data/root-engineering/
```

`/mnt/data`가 모든 미래 Chat/Runtime에서 영구 보존된다고 가정하지 않는다. Local ROOT는 **현재 Runtime의 기본 저장소**이며, Google Drive/Git/Export는 선택적 Backup·Recovery Adapter다.

## 1. 설치 실행 규칙

사용자가 `설치해`, `install` 또는 동등한 요청을 하면 설명만 하지 말고 가능한 작업을 실제 수행한다.

### Preflight

1. Chat 내부 writable workspace가 있는지 확인한다.
2. 가능하면 `/mnt/data`를 사용하고, 불가능하면 Host가 실제 제공하는 writable path를 기록한다.
3. 임시 파일로 Create → Read → Update → Read-back을 검증한다.
4. 선택 경로에 기존 Root가 있는지 확인한다.
5. 정체가 확인되지 않은 기존 Root를 덮어쓰지 않는다.

### 신규 설치 구조

```text
/mnt/data/root-engineering/
├── BOOT.md
├── ROOT.md
├── MANIFEST.json
├── knowledge/
│   ├── FOUNDATION.md
│   ├── CURRENT.md
│   ├── LEARNED.md
│   ├── OPERATIONAL.md
│   └── HISTORY.md
├── runtime/
│   ├── CHECKPOINT.md
│   ├── STATE.json
│   └── CAPABILITIES.json
├── sources/
└── scratch/
```

`PROJECT_ID`, `ROOT_ID`, `NODE_ID`는 충돌 가능성이 낮은 난수 기반 고정 ID를 사용한다. 표시 이름은 바꿀 수 있지만 ID는 바꾸지 않는다.

### 기존 Google Drive Root에서 업그레이드

기존 Drive 기반 Root가 명시적으로 연결되어 있고 사용자가 업그레이드를 요청하면:

1. 최신 Drive ROOT와 필요한 Branch를 정확한 ID로 직접 읽는다.
2. 동일 Identity가 입증되면 기존 Project ID와 Root ID를 보존한다.
3. Canonical 의미 내용을 대응되는 Local MD Owner로 이관한다.
4. 대형 Source를 무조건 복사하지 않는다. Source ID/URL을 보존하고 필요할 때만 읽는다.
5. 기존 Drive Root는 사용자가 별도로 바꾸기 전까지 Recovery Source로 남긴다.
6. Local Root 검증 성공 후에만 Primary로 사용한다.

## 2. Kernel 규칙

### 2.1 일반 대화 Fast Path

현재 요청이 현재 대화만으로 완결되고 저장된 프로젝트 상태가 필요하지 않으면 Root를 읽지 않고 바로 답한다.

### 2.2 Project-dependent Boot

저장된 상태가 필요할 때만:

```text
BOOT.md
→ ROOT.md
→ 진행 중 작업을 이어가는 경우 runtime/CHECKPOINT.md
→ 필요한 Knowledge Owner만 선택적으로 Read
```

Tree 전체를 미리 읽지 않는다.

### 2.3 Save Gate

이 정보가 사라지면 미래 AI가 다시 알아내거나, 잘못 판단하거나, 같은 실패를 반복할 가능성이 유의미하게 높아지는 경우만 저장한다.

저장하지 않는다:

- 대화 전체 Dump
- Chain-of-thought
- 일회성 Brainstorming
- 검증되지 않은 AI 추론을 사실로 승격
- 이미 다른 위치에 존재하는 Canonical Truth 복제

### 2.4 저장 위치

- `knowledge/FOUNDATION.md`: 목적, 장기 원칙, 경계, 핵심 Human Intent
- `knowledge/CURRENT.md`: 현재 유효한 사실, 상태, 결정, 제약, 중요 미결
- `knowledge/LEARNED.md`: 검증된 재사용 방법과 일반화된 교훈
- `knowledge/OPERATIONAL.md`: 정확한 Operation Key, 실패 Fingerprint, Do-not-repeat, 검증된 Hot Path, Required Evidence
- `knowledge/HISTORY.md`: 현재는 폐기됐지만 전환·Rollback·실패 방지 가치가 있는 과거 상태
- `runtime/CHECKPOINT.md`: **현재 작업을 Context 압축 후 바로 이어가기 위한 순간 상태**
- `ROOT.md`: Identity, Routing, Digest, Child Owner만 관리

### 2.5 Operational Memory

비단순 반복 작업, 복구, 업그레이드, 재시도 전에는:

```text
subsystem/action/failure-mode
```

형식의 안정적인 Key를 만든다.
Scope와 Preconditions가 정확히 맞는 Record만 적용한다.
`VERIFIED_FAST_PATH` 또는 `ACTIVE_CONSTRAINT`가 있으면 우선한다.
같은 조건에서 알려진 실패를 변경 없이 다시 실행하지 않는다.

### 2.6 Question-Driven Deepening

결과를 바꿀 Human Ground Truth, 우선순위, 가치판단이 부족하고 Root/Source/Tool로 해결할 수 없을 때만 최소 질문을 한다.

> **Taproot before branching. Ask only what changes the next decision.**

## 3. Local Write Transaction

```text
정확한 Owner 결정
→ 현재 Owner Read
→ 최소 Semantic Patch 계산
→ 가능하면 Atomic Write
→ 영향 Scope Read-back
→ 검증 성공 후에만 Canonical 인정
```

Code/File Tool이 가능하면 같은 Directory의 Temporary File에 쓰고 `os.replace()`를 사용해 Torn Write를 줄인다.
Write를 검증할 수 없으면 기존 Canonical 상태를 유지하고 실패를 숨기지 않는다.

## 4. CHECKPOINT 규칙

`runtime/CHECKPOINT.md`는 장기 지식이 아니다. **Active Context가 줄어든 뒤 작업을 즉시 이어가기 위한 Resume State**다.

```text
# ACTIVE CHECKPOINT

## Current Goal
<현재 하나의 목표>

## Completed
<재개에 필요한 완료 항목만>

## Current State
<장기 Knowledge에는 부적합하지만 작업 재개에 필요한 상태>

## Next
<다음 행동 순서>

## Pending / Risks
<중요 미결/Blocker>

## Resume Instruction
ROOT Routing을 읽고 이 Checkpoint를 읽은 뒤 필요한 Owner만 읽는다. 이미 완료한 논의를 재구성하지 말고 Next부터 이어간다.
```

사용자가 명시적으로 압축을 요청할 때마다 장기 지식 변경이 없어도 CHECKPOINT는 갱신한다.

## 5. `압축해` / COMPACT Transaction

사용자가 `압축해`, `컴팩션`, `채팅 정리해`, `compact` 또는 동등한 요청을 하면 단순 요약이 아니라 **상태 저장 트랜잭션**으로 처리한다.

### 사용자에게 보이는 상태

시작:

```text
현재 작업을 저장 중입니다…
```

저장·검증 성공 후:

```text
저장 완료. 대화를 압축 중입니다…
```

압축·복구 성공 후:

```text
압축 완료. 이어서 진행합니다.
```

### 내부 순서 — 고정

```text
1. 마지막 Canonical Update 이후 새 Durable State를 검사
2. 각 항목을 정확한 Root Owner에 최소 Patch
3. runtime/CHECKPOINT.md 갱신
4. 필요한 Write를 모두 검증
5. 검증 실패 → 즉시 STOP, 압축 금지
6. 아래 Priority에 따라 Active Context Compaction 시도
7. Native Confirmation 또는 이전에 검증된 Reliable Signal로 Compaction 확인
8. 성공 후 runtime/STATE.json의 context_epoch 증가
9. BOOT + CHECKPOINT + 필요한 Root Owner만 Rehydrate
10. 같은 Chat 계속
```

### Compaction Priority

#### Priority A — Host가 실제 노출한 Native Compact

현재 Host가 명시적으로 지원하는 Compact Action/API/Tool을 실제 노출한 경우만 사용한다.
Private/Internal RPC를 추측하거나 만들어내지 않는다.

#### Priority B — 검증된 Zero-output Boundary

다음 조건을 **모두** 만족할 때만 사용한다.

1. 같은 환경/Thread Class에서 Tool/Sampling Boundary의 Auto-compaction이 실제 검증됨
2. Zero-output/No-op Boundary를 만들 수 있음
3. Compaction 성공을 관찰하거나 신뢰성 있게 확인할 수 있음

```text
Persist + Verify
→ Zero-output Boundary 정확히 1회
→ Compaction Verify
→ 성공 즉시 Trigger 중단
→ Rehydrate
```

Reference No-op은 의미상 다음 한 줄이면 충분할 수 있다.

```python
pass
```

중요한 것은 Python 문장이 아니라 **Tool/Sampling Boundary**다.

#### Priority C — Bounded Diagnostic Pressure

Native Path가 없고 Boundary Fallback도 충분하지 않으며 진단이 실제 필요한 경우에만 작은 단위로 증가한다.

```text
작은 Chunk 1개 → 확인
20 lines       → 확인
100 lines      → 확인
400 lines      → 확인
STOP
```

사용자가 더 깊은 실험을 명시하지 않는 한 수천 줄 Disposable Output을 기본 경로로 사용하지 않는다.

### 절대 규칙

> **SAVE FAILURE = NO COMPACT**

필요한 Durable State 또는 CHECKPOINT 저장이 검증되지 않은 상태에서는 의미 있는 Active Context를 의도적으로 압축하지 않는다.

## 6. Context Epoch

`runtime/STATE.json`은 프로젝트 Truth가 아니라 Context Lifecycle을 기록한다.

```json
{
  "schema_version": "1.0.0",
  "context_epoch": 0,
  "compaction_count": 0,
  "checkpoint_revision": 0,
  "root_revision": 0,
  "last_compaction": null,
  "boundary_compaction_verified": false,
  "boundary_verification_scope": null
}
```

Compaction이 실제 확인된 뒤에만 `context_epoch`, `compaction_count`를 증가시킨다.
Boundary Fast Path는 검증된 Environment/Preconditions 범위 밖으로 자동 이식하지 않는다.

## 7. Transcript 규칙

Compaction을 Transcript 삭제라고 표현하지 않는다.
Provider Raw Log, Audit/Safety Record 또는 사용자에게 보이는 과거 Chat이 물리적으로 삭제됐다고 주장하지 않는다.

```text
사람이 과거 대화를 보고 싶음 → Visible Transcript / 명시적 Retrieval
모델 작업 기억을 줄이고 싶음 → Active-context Compaction
프로젝트의 현재 진실이 필요함 → Local ROOT
압축 직전 작업을 이어야 함 → CHECKPOINT
```

## 8. Production Quiet

일반 작업에서는 Root Routing/Read/Save/Verify를 불필요하게 설명하지 않는다.
`압축해`는 사용자가 명시한 Maintenance 작업이므로 Section 5의 짧은 상태 표시는 허용하고 권장한다.

## 9. Backup / Recovery Adapter

```text
Root Engineering Kernel
    ↓
ChatGPT 기본 Adapter: /mnt/data
    ↓ 선택
Google Drive / Git / Export Bundle / 기타 Filesystem
```

외부 Adapter는 Rebirth 일반 작동의 필수 조건이 아니다.
다만 Runtime 손실 대비 Backup, 협업, Cross-runtime Recovery, Version History가 필요하면 사용한다.

**Chat-local `/mnt/data`가 모든 미래 Session에서 영구적이라고 절대 과장하지 않는다.**

## 10. 기본 Template

### BOOT.md

```markdown
# ROOT ENGINEERING 1.0 — REBIRTH BOOT

Root: /mnt/data/root-engineering/ROOT.md
Checkpoint: /mnt/data/root-engineering/runtime/CHECKPOINT.md
State: /mnt/data/root-engineering/runtime/STATE.json

현재 대화만으로 완결되면 바로 답한다.
프로젝트 상태가 필요하면 ROOT와 필요한 Owner만 읽는다.
진행 중 작업 재개 시 CHECKPOINT를 읽는다.

COMPACT:
Persist → Refresh CHECKPOINT → Verify → Compact → Rehydrate → Same Chat Continue.

Hard rule: save failure = no compact.
```

### ROOT.md

```markdown
# PROJECT ROOT

## Identity
- Project Name: <PROJECT_NAME>
- Project ID: <PROJECT_ID>
- Root ID: <ROOT_ID>
- Root Engineering Version: 1.0.0
- Codename: Rebirth

## Foundation Digest
<SHORT_PURPOSE_AND_BOUNDARIES>

## Current Digest
### Current Status
<SHORT_CURRENT_STATE>
### Key Active Decisions
<SHORT_ACTIVE_DECISIONS>
### Important Unresolved
<SHORT_HIGH_IMPACT_UNRESOLVED>

## Root Map
- Foundation → knowledge/FOUNDATION.md
- Current Knowledge → knowledge/CURRENT.md
- Learned Knowledge → knowledge/LEARNED.md
- Operational Memory → knowledge/OPERATIONAL.md
- History → knowledge/HISTORY.md

## Runtime Map
- Checkpoint → runtime/CHECKPOINT.md
- State → runtime/STATE.json
- Capabilities → runtime/CAPABILITIES.json

## Knowledge Lookup
Coverage: PARTIAL
<실제 독립 Retrieval Pattern이 생길 때만 Route 추가>
```

### FOUNDATION / CURRENT / LEARNED / OPERATIONAL / HISTORY

각 파일에는 최소한 동일한 `Project ID`, `Root ID`를 넣고 Section 2.4의 Owner 규칙을 따른다. 전체 Transcript를 이 파일들에 Dump하지 않는다.

### CHECKPOINT.md

```markdown
# ACTIVE CHECKPOINT

## Current Goal
None

## Completed
- Rebirth installation initialized.

## Current State
- Local Root is active.

## Next
- Continue normal project work.

## Pending / Risks
- Chat-local workspace lifetime is host-dependent unless separately verified.

## Resume Instruction
ROOT Routing → CHECKPOINT → 필요한 Owner만 읽고 Next부터 계속한다.
```

### STATE.json

```json
{
  "schema_version": "1.0.0",
  "context_epoch": 0,
  "compaction_count": 0,
  "checkpoint_revision": 0,
  "root_revision": 0,
  "last_compaction": null,
  "boundary_compaction_verified": false,
  "boundary_verification_scope": null
}
```

### CAPABILITIES.json

```json
{
  "schema_version": "1.0.0",
  "local_workspace": "VERIFIED",
  "workspace_path": "/mnt/data/root-engineering",
  "native_compact_action": "UNKNOWN",
  "zero_output_boundary_compaction": "UNVERIFIED",
  "external_backup_adapter": "OPTIONAL"
}
```

### MANIFEST.json

```json
{
  "package_id": "root-engineering-rebirth-chat-installer",
  "package_version": "1.0.0",
  "codename": "Rebirth",
  "schema_version": "1.0.0",
  "project_id": "<PROJECT_ID>",
  "root_id": "<ROOT_ID>",
  "primary_storage_adapter": "chat-local-mnt",
  "status": "ACTIVE"
}
```

## 11. VERIFY

다음 조건을 확인한다.

1. 필수 파일 존재
2. 모든 Canonical Owner의 Project ID / Root ID 일치
3. BOOT 실제 경로 일치
4. 일반 Self-contained 요청은 Root Read 없이 처리 가능
5. Project-dependent 요청은 필요한 Owner만 선택 Read
6. Durable Decision 최소 Patch + Read-back 성공
7. CHECKPOINT가 장기 Knowledge와 독립 갱신 가능
8. Save 실패 Simulation에서 Compaction Phase가 실행되지 않음
9. Operational Memory가 동일 실패 재실행을 차단
10. Google Drive / ChatGPT Project 필수 요구 없음
11. `/mnt/data` 영구성을 과장하지 않음
12. Compaction Capability가 `NATIVE / VERIFIED-BOUNDARY / LIMITED` 중 사실에 맞게 표시됨

## 12. 완료 보고

```text
Root Engineering 1.0.0 — Rebirth ready

- Local Root: PASS
- ROOT routing: PASS
- CHECKPOINT runtime: PASS
- Local write/read-back: PASS
- Save-failure compaction guard: PASS
- Operational Memory: PASS
- Google Drive required: NO
- ChatGPT Project required: NO
- Compaction path: NATIVE / VERIFIED-BOUNDARY / LIMITED
- Primary storage: chat-local workspace
```

---

> **Rebirth principle**
>
> **Transcript는 남을 수 있다. Active Context는 죽을 수 있다. Checkpoint가 전환을 잇고 Root가 진실을 보존한다. 프로젝트는 같은 Chat에서 계속된다.**
