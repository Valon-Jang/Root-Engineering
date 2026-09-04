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
backup_sync_policy: event-driven-dirty-only
backup_on_compaction: configured-and-hash-changed
backup_latest_policy: verified-replace
backup_snapshot_policy: milestone-explicit-migration
optional_backup_failure_blocks_compaction: false
strict_backup_compaction_command: true
backup_direction: local-to-external-one-way
---

# ROOT ENGINEERING 1.0.0 — REBIRTH

> **Model is replaceable. Context is replaceable. Root persists.**
>
> **상태를 저장하고 → Context를 압축하고 → 작업을 복구해 → 같은 Chat을 계속 사용한다.**

이 파일은 Root Engineering 1.0.0 **Rebirth**의 Chat-native 한글 설치본이다.
일반 ChatGPT Chat에서 사용하며 ChatGPT Project나 Google Drive를 필수로 요구하지 않는다.

## 0. Rebirth 구조

장기 Chat에서 다음 세 자원을 분리한다.

```text
CHAT TRANSCRIPT
= 사람이 보는 과거 대화

ACTIVE MODEL CONTEXT
= 모델의 압축 가능한 작업 기억

LOCAL ROOT
= 현재 Chat Runtime 내부의 Canonical 프로젝트 상태
```

기본 Runtime 경로:

```text
/mnt/data/root-engineering/
```

`/mnt/data`가 모든 미래 Chat/Runtime에서 영구 보존된다고 가정하지 않는다. Local ROOT는 **현재 Runtime의 Primary 저장소**이며 Google Drive, Git, Export Bundle은 선택적 Backup·Recovery Adapter다.

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

1. 최신 Drive ROOT와 필요한 Branch를 정확한 ID/Live Access로 읽는다.
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
- Private Chain-of-thought
- 일회성 Brainstorming
- 검증되지 않은 AI 추론을 사실로 승격
- 이미 다른 위치에 존재하는 Canonical Truth 복제

### 2.4 저장 위치

- `knowledge/FOUNDATION.md`: 목적, 장기 원칙, 경계, 핵심 Human Intent
- `knowledge/CURRENT.md`: 현재 유효한 사실, 상태, 결정, 제약, 중요 미결
- `knowledge/LEARNED.md`: 검증된 재사용 방법과 일반화된 교훈
- `knowledge/OPERATIONAL.md`: 정확한 Operation Key, 실패 Fingerprint, Do-not-repeat, 검증된 Hot Path, Required Evidence
- `knowledge/HISTORY.md`: 현재는 폐기됐지만 전환·Rollback·실패 방지 가치가 있는 과거 상태
- `runtime/CHECKPOINT.md`: 현재 작업을 Context 압축 후 바로 이어가기 위한 순간 상태
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

Durable Local State 변경은 다음 순서로 처리한다.

```text
정확한 Owner 결정
→ 현재 Owner Read
→ 최소 Semantic Patch 계산
→ 가능하면 Atomic Write
→ 영향 Scope Read-back
→ 검증 성공 후에만 Canonical 인정
```

Code/File Tool이 가능하면 같은 Directory의 Temporary File에 쓰고 `os.replace()`를 사용해 Torn Write를 줄인다.
일반 저위험 Patch는 영향 Scope의 정확한 Read-back이면 충분하다.
Identity/Routing 같은 고위험 변경은 연결 관계 전체를 검증한다.

Write를 검증할 수 없으면 기존 Canonical 상태를 유지하고 실패를 숨기지 않는다.

## 4. CHECKPOINT 규칙

`runtime/CHECKPOINT.md`는 장기 지식이 아니다. Active Context가 줄어든 뒤 작업을 즉시 이어가기 위한 Resume State다.

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

사용자가 `압축해`, `컴팩션`, `채팅 정리해`, `compact` 또는 동등한 요청을 하면 단순 요약이 아니라 **상태 저장 Transaction**으로 처리한다.

### 사용자에게 보이는 상태

시작:

```text
현재 작업을 저장 중입니다…
```

Local Save가 검증된 뒤:

- External Backup이 설정되지 않았거나 Local Root Hash가 동일하면:

```text
저장 완료. 대화를 압축 중입니다…
```

- External Backup Adapter가 설정되어 있고 Local Root가 변경됐으면:

```text
로컬 저장 완료. 복구본을 동기화 중입니다…
```

Backup 검증 성공 후:

```text
복구본 동기화 완료. 대화를 압축 중입니다…
```

일반 `압축해`에서 선택적 Backup이 실패하면 Local Save를 유지하고 Backup Pending 상태를 기록한 뒤 다음과 같이 알린다.

```text
로컬 저장은 완료됐지만 복구본 동기화는 보류됐습니다. 대화 압축은 계속합니다.
```

`백업하고 압축해` / `backup and compact`는 Strict Mode다. External Backup을 검증하지 못하면 Local Save는 안전하다고 알리되 Compaction 전에 중단한다.

압축·복구 성공 후:

```text
압축 완료. 이어서 진행합니다.
```

### 내부 순서 — 고정

```text
1. 마지막 Canonical Update 이후 새 Durable State 검사
2. 각 항목을 가장 작은 정확한 Root Owner에 최소 Patch
3. runtime/CHECKPOINT.md 갱신
4. 모든 필수 Local Write 검증
5. Local 검증 실패 → STOP, 압축 금지
6. 현재 Canonical Root Hash 계산 후 last_backup_root_hash와 비교
7. External Adapter가 설정되어 있고 Event가 Sync를 요구하면:
   - Hash 동일 → Upload Skip
   - Hash 변경 → 검증된 latest 갱신
   - Milestone/Explicit/Migration Event → Immutable Snapshot도 생성
8. 일반 `압축해`에서 선택적 Backup 실패:
   - external_backup_pending = true
   - 검증된 Local Root를 정본으로 유지
   - Warning 후 Compaction 계속 가능
9. `백업하고 압축해` Strict Backup 실패 → STOP, 압축 금지
10. 아래 Priority에 따라 Active Context Compaction 시도
11. Host-exposed Native Confirmation 또는 이전에 검증된 Reliable Signal로 Compaction 확인
12. 성공 후 runtime/STATE.json의 context_epoch 증가
13. BOOT + CHECKPOINT + 필요한 Root Owner만 Rehydrate
14. 같은 Chat 계속
```

### Compaction Priority

#### Priority A — Host가 실제 노출한 Native Compact

현재 Host가 명시적으로 지원하는 Compact Action/API/Tool을 실제 노출한 경우만 사용한다.
Private/Internal RPC를 추측하거나 만들어내지 않는다.

#### Priority B — 검증된 Zero-output Boundary

다음 조건을 모두 만족할 때만 사용한다.

1. 같은 Environment/Thread Class에서 Tool/Sampling Boundary의 Auto-compaction이 실제 검증됨
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

중요한 것은 Python 문장이 아니라 Tool/Sampling Boundary다.

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

`runtime/STATE.json`은 프로젝트 Truth가 아니라 Context Lifecycle과 Backup 상태를 기록한다.

```json
{
  "schema_version": "1.0.0",
  "context_epoch": 0,
  "compaction_count": 0,
  "checkpoint_revision": 0,
  "root_revision": 0,
  "last_compaction": null,
  "boundary_compaction_verified": false,
  "boundary_verification_scope": null,
  "external_backup_adapter": "NONE",
  "external_backup_pending": false,
  "current_root_hash": null,
  "last_backup_root_hash": null,
  "last_backup_at": null,
  "last_snapshot_at": null
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

Rebirth는 Kernel과 Storage를 분리한다.

```text
Root Engineering Kernel
    ↓
ChatGPT 기본 Adapter: /mnt/data
    ↓ 선택
Google Drive / Git / Export Bundle / 기타 Filesystem
```

외부 Adapter는 Rebirth 일반 작동의 필수 조건이 아니다.
Runtime 손실 대비 Backup, Cross-runtime Recovery, Collaboration, Version History, Migration을 위해 사용할 수 있다.

### 9.1 Event-driven Cadence — Timer Loop 없음

Backup은 경과 시간이 아니라 의미 있는 Event에 따라 실행한다. 일반 Chat에서 보이지 않는 Background Timer를 주장하거나 의존하지 않는다.

| Event | External Backup Action |
|---|---|
| 일반 대화 | 외부 Write 없음 |
| 검증된 Local Root Patch | Canonical Hash가 바뀌면 Backup Pending 표시 |
| `압축해` / `compact` | Adapter가 설정되고 Hash가 바뀐 경우에만 `latest` 갱신 |
| Critical Authority/Routing/Structure 변경 | 설정된 경우 즉시 `latest` 갱신 |
| `백업해` / `backup` | 검증된 `latest` 즉시 강제 갱신 |
| `백업하고 압축해` | Compaction 전에 External Backup 검증 필수 |
| `마무리하자` / Explicit Closeout | 변경됐으면 `latest` 갱신 |
| Release, Major Milestone, Migration, Restore, Destructive Change | `latest` 갱신 + Immutable Snapshot 생성 |
| Semantic/Hash 변경 없음 | External Write Skip |

현재 Runtime에서는 Local Root가 정본이다.

### 9.2 Hash-gated Latest Backup

Disposable Scratch와 불안정한 Packaging Metadata를 제외한 Deterministic Canonical Export Set을 Hash한다.

```text
BOOT.md
ROOT.md
MANIFEST.json
knowledge/**
runtime/CHECKPOINT.md
runtime/STATE.json
runtime/CAPABILITIES.json
Policy가 명시적으로 포함한 작은 Linked Canonical Sources
```

`current_root_hash == last_backup_root_hash`이면 다시 Upload하지 않는다.

변경됐으면 하나의 Recoverable `latest`를 갱신한다.

```text
Root Engineering Backups/
└── <PROJECT_ID>/
    ├── latest/
    │   ├── root-engineering-latest.zip
    │   └── BACKUP_MANIFEST.json
    └── snapshots/
        └── <ISO_DATE>_epoch-<N>_<REASON>.zip
```

`BACKUP_MANIFEST.json` 최소 필드:

```json
{
  "project_id": "<PROJECT_ID>",
  "root_id": "<ROOT_ID>",
  "root_engineering_version": "1.0.0",
  "context_epoch": 0,
  "canonical_root_hash": "<HASH>",
  "backed_up_at": "<ISO-8601>",
  "backup_kind": "LATEST",
  "verification": "PASS"
}
```

Upload와 Read-back/Hash 검증이 성공한 뒤에만 `latest` 교체를 인정한다.
매 Compaction마다 Immutable Snapshot을 만들지 않는다.

### 9.3 Snapshot Gate

Immutable Snapshot은 다음 경우에만 만든다.

- Release 또는 Named Milestone
- Storage Adapter/Runtime Migration
- 다른 Canonical State를 수용하기 전 Restore
- Critical Authority/Routing/Schema 변경
- Potentially Destructive Operation
- Explicit User Request

Snapshot은 중요한 전환을 설명·복구하기 위한 것이며 Activity Log가 아니다.

### 9.4 실패 의미

```text
필수 Local Root / CHECKPOINT Save 실패
→ STOP
→ NO COMPACT

일반 `압축해`의 선택적 External Backup 실패
→ Local Root 정본 유지
→ external_backup_pending = true
→ Warning 후 Compaction 계속 가능
```

Strict Mode:

```text
`백업하고 압축해`
→ Local Save + External Backup 모두 검증 필수
→ 필수 실패 하나라도 있으면 NO COMPACT
```

Pending Backup은 다음 Qualifying Event 또는 Explicit `백업해`에서 재시도한다.
같은 실패 Operation을 같은 Turn에서 변경 없이 반복하지 않는다.

### 9.5 One-way Authority와 Restore

Drive 기반 Root를 Local Rebirth로 Migration한 뒤:

```text
Drive Latest Canonical Read
→ Local Root 변환
→ Local Identity/Content 검증
→ 최종 Drive Migration Snapshot
→ 과거 Drive Root는 Legacy/Read-only Recovery Source
→ 정상 흐름은 Local → External Backup
```

일반 운용에서 Drive 변경을 Local Root로 자동 Merge하지 않는다.
Restore는 명시적 Operation이다. Backup 하나를 선택하고 Project ID, Root ID, Version/Schema Compatibility, Manifest, Content Hash를 검증한 뒤 요청한 Scope만 복구한다.

Chat-local `/mnt/data`가 모든 미래 Session에서 영구적이라고 절대 과장하지 않는다.

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
Durable State 저장 → CHECKPOINT 갱신 → Local 검증 → 변경된 선택적 Backup 동기화 → Compact → Rehydrate → Same Chat Continue.

Backup Policy:
- Local Root가 정본이다.
- Qualifying Event에서 Canonical Hash가 바뀐 경우에만 External `latest`를 갱신한다.
- Immutable Snapshot은 Milestone, Explicit Request, Migration/Restore, Critical Change에만 만든다.
- `백업하고 압축해`는 External Backup 검증 필수다.
- 일반 `압축해`는 선택적 Backup 실패 시 external_backup_pending = true로 기록한 뒤 계속할 수 있다.

Hard Rule: 필수 Local Save 실패 = No Compact.
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

각 파일에는 최소한 동일한 `Project ID`, `Root ID`를 넣고 Section 2.4 Owner 규칙을 따른다. 전체 Transcript를 Dump하지 않는다.

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
  "boundary_verification_scope": null,
  "external_backup_adapter": "NONE",
  "external_backup_pending": false,
  "current_root_hash": null,
  "last_backup_root_hash": null,
  "last_backup_at": null,
  "last_snapshot_at": null
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
  "external_backup_adapter": "OPTIONAL",
  "external_backup_sync_policy": "EVENT_DRIVEN_HASH_GATED",
  "external_backup_strict_command": "백업하고 압축해"
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

다음 조건을 모두 확인한다.

1. 필수 파일 존재
2. 모든 Canonical Owner의 Project ID / Root ID 일치
3. BOOT 실제 Root/Checkpoint/State Path 일치
4. 일반 Self-contained 요청은 Root Read 없이 처리 가능
5. Project-dependent 요청은 필요한 Owner만 선택 Read
6. Durable Decision 최소 Patch + Read-back 성공
7. CHECKPOINT가 장기 Knowledge와 독립 갱신 가능
8. Save 실패 Simulation에서 Compaction Phase 실행 차단
9. Operational Memory가 동일 실패 재실행 차단
10. Google Drive / ChatGPT Project 필수 요구 없음
11. `/mnt/data` 영구성을 과장하지 않음
12. Compaction Capability가 Supported/Verified Fallback/Unavailable·Unknown 중 사실에 맞게 표시
13. External Backup Cadence는 Event-driven + Hash-gated
14. Canonical Hash가 같으면 External Upload Skip
15. 일반 `압축해`의 Optional Backup 실패는 external_backup_pending = true 후에만 계속 가능
16. `백업하고 압축해`에서 External Backup 미검증 시 Compaction 차단
17. Immutable Snapshot은 Milestone/Explicit/Migration/Critical Change에만 생성
18. 정상 Authority Flow는 Local → External이며 자동 양방향 Merge 없음

## 12. REPAIR

가장 작은 손상 Owner만 복구한다.
정상 Root 전체를 다시 생성하지 않는다.
Stable ID와 무관한 Content를 보존한다.
Identity를 입증할 수 없으면 다른 Root를 조용히 채택하지 말고 중단한다.

## 13. EXPORT / BACKUP

사용자가 Backup 또는 Cross-runtime Recovery를 요청하면:

1. Canonical Local Root의 Deterministic Export 생성
2. Canonical Root Hash 계산·기록
3. Hash가 같으면 Explicit Snapshot 요청이 없는 한 `latest` Upload Skip
4. 설정된 External Adapter로 Upload/Commit
5. Upload된 Bundle과 `BACKUP_MANIFEST.json` 검증
6. 검증 성공 후에만 `last_backup_root_hash`, `last_backup_at`, `external_backup_pending` 갱신

External Backup은 사용자가 명시적으로 Adapter Migration/Restore를 하지 않는 한 Local Root의 Authority를 바꾸지 않는다.

## 14. Rebirth Acceptance Gate

강한 Rebirth 검증은 다음 반복 Cycle을 시험해야 한다.

```text
work
→ durable-state promotion
→ CHECKPOINT
→ verified backup event when applicable
→ verified compaction
→ rehydrate
→ continue same Chat
```

최소 측정:

- Same-thread Continuation
- Compaction 후 State Accuracy
- Decision Retention
- Checkpoint Resume Accuracy
- No-repeat Operational Behavior
- External Backup State Accuracy
- Context/Latency Trend where observable
- 반복 Compaction Quality Loss

한 환경의 결과만으로 Universal One-chat-forever를 주장하지 않는다.

## 15. 완료 보고

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
- External backup: NOT CONFIGURED / READY / PENDING
- Backup cadence: EVENT-DRIVEN + HASH-GATED
- Backup authority direction: LOCAL → EXTERNAL
```

---

> **Rebirth principle**
>
> **Transcript는 남을 수 있다. Active Context는 죽을 수 있다. Checkpoint가 전환을 잇고 Root가 진실을 보존한다. 같은 프로젝트는 같은 Chat에서 계속된다.**
