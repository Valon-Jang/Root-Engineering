---
package_id: root-engineering-rebirth-chat-installer
package_version: 1.1.0
codename: Rebirth
release_name: Sidecar Work Graph
schema_version: 1.1.0
release_date: 2026-09-04
status: staged-next-version
base_compatible_version: 1.0.0
primary_environment: 기존 Markdown 지식파일이 있는 프로젝트 작업공간
supported_topologies:
  - isolated-root
  - sidecar-workspace
preferred_existing_workspace_topology: sidecar-workspace
control_plane_path: .root
content_registry_path: .root/runtime/CONTENT_REGISTRY.json
existing_markdown_adoption: byte-exact-register-in-place
existing_markdown_move_during_adoption: forbidden
existing_markdown_rename_during_adoption: forbidden
existing_markdown_rewrite_during_adoption: forbidden
line_ending_normalization_during_adoption: forbidden
encoding_normalization_during_adoption: forbidden
adoption_verification: pre-and-post-sha256
routing_model: root-to-core-to-exact-work-node
specialized_project_content: excluded
---

# ROOT ENGINEERING 1.1.0 — REBIRTH: SIDECAR WORK GRAPH

> **모델은 교체 가능하다. Context도 교체 가능하다. 기존 지식은 보존한다. Root는 남는다.**

이 문서는 장기 프로젝트에서 실제로 검증된 구조만 일반화한 다음 버전 설치파일이다. 특정 프로젝트의 사실, 이름, 업무절차, 도메인 규칙은 포함하지 않는다.

핵심 변경은 다음 한 문장이다.

> **기존 Markdown을 Root Engineering 양식으로 다시 쓰지 않는다. 옆에 Root 제어층을 만들고, 기존 문서를 원문 그대로 등록한 뒤 정확한 수행업무 문서로 라우팅한다.**

Root Engineering 1.0.0의 Kernel은 그대로 유지한다. 1.1.0은 **Sidecar Work Graph** 구조와 비파괴 Adoption Transaction을 추가한다.

---

## 0. 적용범위

다음과 같은 Markdown이 이미 있는 프로젝트를 대상으로 한다.

- 프로젝트 판단방식이나 운영 Profile;
- 수행업무 Router / Core;
- 반복업무 Standard;
- 업무별 Living Context;
- Handoff / Resume 문서;
- Reference / 근거자료.

이 구조는 다음 문제를 해결한다.

1. 평면 폴더에서는 어떤 문서가 현재 사실의 Owner인지 찾기 어렵다.
2. 설치 과정에서 기존 문서를 재작성하면 사실, 용어, 이력, 개행이 바뀔 수 있다.
3. 모든 현재상태를 하나의 `CURRENT.md`에 넣으면 독립 업무가 늘수록 문서가 비대해진다.

따라서 1.1.0은 다음을 분리한다.

```text
CONTROL PLANE
= Root Identity / Routing / Registry / Checkpoint / Verification

CONTENT PLANE
= 기존 프로젝트 Markdown 원문
```

### 적용하지 않는 것

- 특정 프로젝트 내용을 설치파일에 포함;
- 기존 Markdown의 의미나 문구 수정;
- 모든 업무를 하나의 생성 Summary로 통합;
- Adoption 중 파일 이동, 이름변경, 삭제, 정규화;
- 파일명만으로 Authority 확정;
- Rebirth 1.0.0의 Compaction / Backup / Storage Safety 규칙 대체.

---

# PART A. Architecture

## 1. Sidecar Workspace 구조

기존 Markdown이 있는 Workspace에는 `.root/` 제어층만 추가하고 Content Plane은 그대로 둔다.

```text
<PROJECT_WORKSPACE>/
├── .root/
│   ├── BOOT.md
│   ├── ROOT.md
│   ├── MANIFEST.json
│   ├── knowledge/
│   │   ├── FOUNDATION.md
│   │   ├── CURRENT.md
│   │   ├── LEARNED.md
│   │   ├── OPERATIONAL.md
│   │   └── HISTORY.md
│   └── runtime/
│       ├── CHECKPOINT.md
│       ├── STATE.json
│       ├── CAPABILITIES.json
│       └── CONTENT_REGISTRY.json
│
├── <기존 Profile Markdown>          ← 원문 유지
├── <기존 Router/Core Markdown>      ← 원문 유지
├── <기존 Standard Markdown>         ← 원문 유지
├── <기존 Work Context Markdown>     ← 원문 유지
├── <기존 Handoff Markdown>          ← 원문 유지
└── <기존 Reference / Source>        ← 원문 유지
```

Canonical Project Boundary는 `<PROJECT_WORKSPACE>`다. `.root/`는 이 경계 안의 Root Engineering 제어층이며, 등록된 기존 문서는 현재 경로에서 Canonical Content Owner로 유지된다.

### 1.1 Sidecar를 쓰는 이유

- 정확한 Boot / Routing;
- 사실과 판단의 단일 Owner;
- 현재 업무 Resume;
- 구조 검증;
- Hash 기반 변경 감지;

를 제공하면서 성숙한 기존 문서를 다시 쓰지 않기 위해서다.

### 1.2 Isolated Root 호환

신규 프로젝트에는 기존 1.0.0 구조를 계속 사용할 수 있다.

```text
/mnt/data/root-engineering/
```

기존 지식 Corpus가 있으면 Sidecar, 없는 신규 프로젝트면 Isolated Root를 사용한다.

---

## 2. 제어층 역할

### `BOOT.md`

Workspace, Root ID, Checkpoint 경로, 프로젝트 의존 Boot 순서를 가진 최소 진입점.

### `ROOT.md`

다음만 가진 작은 Identity / Routing 문서.

- Project ID / Root ID;
- 제어층 경로;
- Compact Digest;
- `CURRENT.md` Route;
- `CONTENT_REGISTRY.json` Route;
- Direct Child Ownership.

상세 업무내용을 복제하지 않는다.

### `knowledge/FOUNDATION.md`

Root Engineering 자체가 소유해야 하는 안정적 목적, 경계, Human Intent. 기존 Profile 문서는 복사하지 않고 Content Node로 등록한다.

### `knowledge/CURRENT.md`

현재 Routing Digest, Active Work Node, 업무 간 핵심 Risk, Routing Core Pointer를 관리한다. 상세 업무문서를 대체하지 않는다.

### `knowledge/LEARNED.md`

검증된 범용 학습. 기존 Standard는 복사하지 않고 원위치 등록한다.

### `knowledge/OPERATIONAL.md`

반복작업 Key, 검증된 Fast Path, 실패 Fingerprint, 필요한 Evidence.

### `knowledge/HISTORY.md`

Root 수준에서 폐기된 Routing / Topology 이력. 기존 문서에 이미 있는 상세이력을 흡수하지 않는다.

### `runtime/CHECKPOINT.md`

현재 한 개 실행경로의 목표, 완료, 상태, 다음 Action, Risk, Resume Instruction.

### `runtime/CONTENT_REGISTRY.json`

보존된 Content Node의 기계판독용 Authoritative Map.

---

# PART B. Content Registry / Role

## 3. Registry 최소구조

```json
{
  "schema_version": "1.1.0",
  "project_id": "REP-...",
  "root_id": "RR-...",
  "workspace": ".",
  "preservation_mode": "BYTE_EXACT_REGISTER_IN_PLACE",
  "generated_at": "2026-09-04T00:00:00Z",
  "nodes": [
    {
      "node_id": "RN-...",
      "relative_path": "WORK_EXAMPLE.md",
      "role": "WORK_CONTEXT",
      "authority": "CANONICAL_CONTENT_OWNER",
      "status": "ACTIVE",
      "sha256": "...",
      "size_bytes": 12345,
      "parent_route": "ROUTING_CORE",
      "direct_children": []
    }
  ]
}
```

Registry에는 문서본문을 복사하지 않고 Metadata와 Hash만 저장한다.

## 4. 범용 Role

### `OPERATING_PROFILE`

**어떻게 판단·검토·우선순위화·보고할지** 정의한다. 업무사실이 아니다.

파일명 Hint:

```text
*PROFILE*.md
*OPERATING*.md
```

### `ROUTING_CORE`

**어떤 수행업무 Context를 읽을지**, 등록업무 Map과 Boundary를 정의한다.

파일명 Hint:

```text
*WORK_CORE*.md
*ROUTER*.md
*CORE*.md — 실제 Routing 의미가 확인되는 경우
```

### `EXECUTION_STANDARD`

반복되는 업무종류를 **어떻게 수행할지** 정의한다.

파일명 Hint:

```text
*STANDARD*.md
*PROTOCOL*.md
*GUIDE*.md
```

### `WORK_CONTEXT`

한 수행업무의 실제 사실, 판단, 완료 Action, 회신대기, 일정, 다음 Action, Gate, Resume Point를 소유한다.

파일명 Hint:

```text
WORK_*.md
```

### `HANDOFF`

Stage / Chat / 담당 / 구현경계를 넘길 때 필요한 임시 연결문서.

파일명 Hint:

```text
*HANDOFF*.md
*CHAT_SUMMARY*.md
*STAGE_PLAN*.md — Authority Owner가 아니라 전환계획인 경우
```

### `REFERENCE`

현재 의사결정 Owner가 아닌 근거, 배경, Data Note, Report.

### `UNCLASSIFIED`

근거가 부족하면 강제분류하지 않는다. 잘못된 분류보다 보존이 우선이다.

## 5. Authority 분리

```text
OPERATING_PROFILE
= 어떻게 판단할 것인가

ROUTING_CORE
= 어떤 Context를 읽을 것인가

EXECUTION_STANDARD
= 반복업무를 어떻게 수행할 것인가

WORK_CONTEXT
= 실제로 무엇이 있었고 현재 어디까지인가

REFERENCE
= 판단을 뒷받침하는 근거
```

Profile이 업무사실을 만들지 않는다. Standard가 업무별 최신결정을 덮지 않는다. Router가 모든 상세사실의 Owner가 되지 않는다.

---

# PART C. 비파괴 Adoption Transaction

## 6. 기존 Markdown 보호계약

Adoption 중 모든 기존 Markdown은 보호대상이다.

금지:

- 본문 수정;
- Metadata 앞붙이기;
- Routing Block 뒤붙이기;
- Heading 정리;
- 공백 / 개행 정규화;
- Encoding 변경;
- 이름변경;
- 이동;
- 삭제;
- 생성문서로 교체.

허용되는 Write는 `.root/` 아래의 신규 또는 기존 Root-owned 제어파일뿐이다.

## 7. 실행순서

```text
1. 정확한 Project Workspace 결정
2. Writable 확인
3. 기존 유효 `.root/` 탐지
4. `.root/` 밖 기존 Markdown 전체 Inventory
5. Relative Path / Byte Size / SHA-256 기록
6. 보수적으로 Role 분류
7. 임시 sibling 경로에 후보 `.root/` 생성
8. ROOT / Routing Digest / Checkpoint / Manifest / State / Capabilities / Registry 작성
9. 생성된 제어파일 Read-back 검증
10. 기존 Markdown 전체 재Hash
11. Path / Size / Hash 중 하나라도 변경되면 후보 제어층만 삭제하고 FAIL CLOSED
12. 가능하면 후보 `.root/`를 Atomic Activate
13. Active Registry 재확인 / 등록경로 Sample Read
14. 보존 파일수와 Hash 동일결과 보고
```

### 7.1 기존 `.root/`가 있는 경우

- 두 번째 Root 생성 금지;
- Schema / Topology 비교 후 VERIFY 또는 UPGRADE;
- 등록된 Content 보존;
- Version Delta에 필요한 Root-owned 파일만 Patch.

Identity가 증명되지 않으면 이름만 보고 덮어쓰지 말고 중단한다.

### 7.2 실패처리

> **보호대상 Markdown 불일치 1건이라도 있으면 Adoption 실패다.**

부분 활성화하지 않는다. 원문을 추정 복구하지 않는다. 기존 Workspace를 Authoritative 상태로 유지하고 변경경로를 정확히 보고한다.

---

# PART D. Boot / Routing

## 8. 프로젝트 의존 Boot

자기완결 요청은 Fast Path로 답하고 Root를 읽지 않는다.

프로젝트 상태가 필요하면:

```text
.root/BOOT.md
→ .root/ROOT.md
→ .root/knowledge/CURRENT.md
→ Routing이 필요할 때 등록된 ROUTING_CORE
→ 정확한 WORK_CONTEXT
→ 현재 업무에 필요한 Profile / Standard / Handoff / Reference만 선택 Read
```

모든 업무파일을 미리 읽지 않는다.

## 9. 충돌 시 우선순위

```text
1. 현재 대화의 사용자 직접 지시 / 수정
2. 해당 사실의 정확한 Authoritative WORK_CONTEXT 또는 Content Owner
3. 판단방법에 적용되는 OPERATING_PROFILE / EXECUTION_STANDARD
4. Root 수준 Digest / Routing Metadata
5. 일반 관행 / 모델 추론
```

현재 대화의 수정은 즉시 우선한다. 저장은 정확한 Owner와 Save Gate를 통해서만 한다.

## 10. 수행업무 식별

### 기존 업무

정확한 `WORK_CONTEXT`에서 필요한 것만 읽는다.

- 현재 상태;
- 확정 사실;
- 과거 판단;
- 완료 Action;
- 회신 / 결과 대기;
- 일정;
- 다음 Action;
- Gate;
- Resume Point.

### 신규 업무

모든 대화에 Work Node를 만들지 않는다. 다음처럼 Context 손실 Risk가 커질 때 생성한다.

- 여러 날 지속;
- 다수 담당 / 부서 / 업체 연관;
- 일정 / 승인 / Test / Gate 존재;
- 사실과 판단 누적;
- 다른 Chat / 담당자가 이어갈 필요.

신규 Node는 아래 권장구조를 사용할 수 있지만 기존문서는 이 구조로 재작성하지 않는다.

## 11. 신규 Work Node 권장구조

```text
# WORK_<NAME>

## 0. Use Rules / Boundary
## 1. Purpose / Problem
## 2. Confirmed Facts
## 3. Current Judgment / Evidence
## 4. Completed Actions
## 5. Pending Responses / Results
## 6. Schedule
## 7. Risks
## 8. Next Actions
## 9. Gates / Completion Conditions
## 10. Resume Point
```

---

# PART E. Write / Update 규칙

## 12. Single Owner Write

- 사실은 정확한 Work Node에 Update;
- Routing 변화만 Routing Core에 Update;
- 판단정책 변화만 Profile에 Update;
- 반복방법 변화만 Standard에 Update;
- Identity / Topology / Direct Route 변화만 ROOT에 Update;
- 편의를 위해 동일 상세내용을 여러 Node에 복제하지 않는다.

## 13. Adoption 이후 기존 Content 수정

Byte-exact 보장은 Adoption Transaction에 적용된다.

활성화 이후 사용자가 Living Work 파일의 의도적 Update를 요청하면 다음 조건에서 가능하다.

1. 정확한 Owner 결정;
2. Semantic Delta 명확화;
3. 무관한 내용 보존;
4. Write 검증;
5. Registry Hash / Size를 같은 성공 Transaction에서 Update;
6. 실패 시 기존 파일과 Registry 유지.

구조 Upgrade만으로 Content Plane Markdown을 수정하지 않는다.

## 14. 현재상태 / History

Authoritative Work Node에서 최신 유효상태가 명확해야 한다. 과거상태는 전환이유, Rollback, 실패방지 가치가 있을 때 보존한다.

Work Owner와 경쟁하는 별도 최신 Summary를 만들지 않는다.

## 15. Checkpoint

`CHECKPOINT.md`는 현재 한 개 실행경로를 가리키며 즉시 재개에 필요한 내용만 가진다. Work Node를 대체하지 않는다.

```text
# ACTIVE CHECKPOINT

## Current Goal
## Active Work Node
## Completed
## Current State
## Next
## Pending / Risks
## Resume Instruction
```

---

# PART F. Rebirth 1.0.0에서 Upgrade

## 16. Upgrade Mode

### Mode A — 기존 Isolated 1.0.0 Root

사용자가 별도 Workspace Binding을 요청하지 않으면 기존 구조 유지. 1.1 Registry / Role 의미만 추가하고 기존 Knowledge 파일은 이동하지 않는다.

### Mode B — 기존 Markdown Workspace

`.root/` Sidecar를 생성하고 원위치 등록한 뒤 Pre/Post Hash 검증 후 활성화한다.

### Mode C — 이미 Router/Core/Work 구조가 있는 프로젝트

그 구조를 Content Plane으로 인정한다. 이름과 내용을 번역·재작성하지 않는다. 근거가 충분할 때 기존 Router는 `ROUTING_CORE`, 업무별 문서는 `WORK_CONTEXT`, 판단방식은 `OPERATING_PROFILE`, 반복절차는 `EXECUTION_STANDARD`로 등록한다.

### Mode D — 혼합 / 불명확 Workspace

불확실한 문서는 `UNCLASSIFIED`로 등록한다. 추후 검증된 근거로 Metadata만 재분류하고 본문은 바꾸지 않는다.

## 17. Upgrade Write Scope

허용:

- `.root/` 제어층 생성 / Patch;
- Registry Metadata 추가;
- 검증된 근거에 따른 Role Metadata 변경;
- Root Routing / Checkpoint Pointer Update.

금지:

- 기존 Markdown 편집;
- Heading 정리;
- 기존파일 자동 Merge;
- Duplicate 자동삭제;
- 프로젝트 고유용어 변경;
- 프로젝트 전문내용을 전역 Root Engineering 정책으로 승격.

---

# PART G. 검증 / 완료

## 18. Acceptance Test

완료조건:

1. `.root/` Identity 유효.
2. 보호대상 Markdown의 Path / Size / SHA-256이 전후 동일.
3. Registry의 모든 Path가 실제로 Resolve.
4. Workspace에 ACTIVE Root 1개.
5. 프로젝트 질문이 `Root → Current → Routing Core → 정확한 Work Context`로 Routing.
6. 무관한 Work 파일을 읽지 않음.
7. Profile / Standard를 방법으로 사용하고 업무사실로 오인하지 않음.
8. Checkpoint만으로 현재 업무를 Resume 가능.
9. 설치파일에 프로젝트 전문내용이 없음.

## 19. 완료보고

```text
Mode: SIDECAR_WORKSPACE / ISOLATED_ROOT
Root: <verified path>
Protected Markdown files: <count>
Preservation check: <count>/<count> path-size-hash unchanged
Registered roles: <compact counts>
Active work node: <path or NONE>
Acceptance routing: PASS / FAIL
Unclassified files: <count>
```

진단에 필요하지 않으면 내부 ID를 나열하지 않는다.

## 20. Reference 구현

Repository에 다음 도구를 포함한다.

```text
tools/root_sidecar_adopt.py
```

기존 Markdown을 수정·이동·이름변경·삭제하지 않고 Inventory, Role 분류, 제어층 생성, 전후 SHA-256 검증을 수행하는 보수적 Reference다.

이 도구는 Root Engineering Authority / Save Gate를 대체하지 않는다. 구조 Transaction을 실행 가능한 형태로 증명한다.

---

# PART H. 핵심 불변조건

## 21. Non-Negotiable Invariants

> **기존 지식은 재작성하지 않고 Adoption한다.**

> **Routing Metadata는 변할 수 있지만 Adoption 중 보호대상 Content Byte는 변하지 않는다.**

> **Router는 어디를 읽을지 결정하며 모든 사실의 Owner가 되지 않는다.**

> **Profile은 판단방식, Work Node는 실제 이력과 현재상태, Standard는 수행방법을 소유한다.**

> **하나의 현재 사실에는 하나의 Authoritative Owner만 둔다.**

> **현재 대화의 사용자 직접 지시가 프로젝트 수준 최우선이다.**

> **보존검증 불일치는 활성화 전에 Fail Closed한다.**

---

## 22. Version Position

Root Engineering 1.1.0은 Rebirth 1.0.0의 추가형 구조 진화다.

추가내용:

- 기존 Workspace용 Sidecar 설치;
- 기존 Markdown Byte-exact Adoption;
- Role-aware Content Registry;
- Root → Core → 정확한 Work Context Routing;
- Profile / Routing / Standard / Work / Handoff / Reference 역할분리;
- Hash Gate 기반 구조 활성화.

기존 1.0.0 설치파일과 모든 기존 Markdown은 이 Staged Version이 명시적으로 승격되기 전까지 변경하지 않는다.
