# Root Engineering 1.0 Rebirth — Persistent Thread 융합 계약

상태: Root Engineering `1.0.0` Rebirth의 규범적 통합 계약  
버전 영향: 없음. Package와 Schema는 `1.0.0` 유지  
연구 출처: `Valon-Jang/persistent-project-thread`

## 1. 목적

이 문서는 검증된 Persistent Project Thread 연구 결과를 Root Engineering Rebirth에 융합한다. 단, **두 번째 Canonical System이나 서로 경쟁하는 `압축해` Skill을 만들지 않는다.**

통합 원칙:

> **연구는 동작을 발견하고, Rebirth가 Production 계약을 소유한다.**

Persistent Project Thread 저장소는 독립 연구·증거 저장소로 유지한다. 실제 설치된 Root의 운영 정본은 Root Engineering Rebirth다.

2026-09-05 장기 관찰에서는 성공적인 Active-context Compaction만으로 하나의 ChatGPT Thread를 무기한 유지할 수 있다는 더 강한 가설도 반증되었다. 따라서 Rebirth는 새로운 구조적 결론을 흡수한다.

> **Thread는 실행 Resource이지 Persistence Authority가 아니다.**

현재 Rebirth `1.0.0`은 해당 Chat이 유효한 동안에는 여전히 하나의 Chat 안에서 동작한다. 자동 Thread/Session Rollover가 이번 버전에 구현되었다고 주장하지 않는다. 다만 연구 구조에서는 Project Authority가 Thread가 아니라 Root/Checkpoint에 있으므로 Thread 교체 역시 Project Continuity와 양립 가능한 것으로 취급한다.

## 2. 문서 권한 지도

각 문서는 역할을 하나만 가진다.

| Resource | 권한 역할 |
|---|---|
| `installer/ROOT_ENGINEERING_REBIRTH_INSTALLER.md` | 영문 Canonical 설치·Runtime 계약 |
| `installer/ROOT_ENGINEERING_REBIRTH_INSTALLER_KO.md` | 영문 Installer의 한글 의미 동등본 |
| `docs/ROOT_ENGINEERING_1.0_REBIRTH.md` | 구조 설명. Installer를 덮어쓰지 않음 |
| `docs/ROOT_ENGINEERING_1.0_BACKUP_POLICY.md` | 위임된 외부 Backup 규범 정본 |
| `docs/ROOT_ENGINEERING_1.0_BACKUP_POLICY_KO.md` | Backup Policy 한글 의미 동등본 |
| 이 문서 | 문서 간 융합·권한 관계 정본 |
| `installer/rebirth/root-engineering/SKILL.md` | 실행 Hot Path. 요약·Routing은 하되 독립 정책을 만들지 않음 |
| `installer/rebirth/runtime/rebirth_transaction.py` | 결정적 Local Transaction Guard. ChatGPT 압축 또는 Google Drive Adapter 자체는 구현하지 않음 |
| `Valon-Jang/persistent-project-thread` | 연구·증거 출처. 설치된 Rebirth Root의 Runtime 정본이 아님 |

충돌 시 우선순위:

```text
현재 User/System/Project Instructions
→ Rebirth Canonical Installer
→ 위임된 규범 Policy/Fusion 문서
→ Rebirth Skill
→ 설명 문서
→ 연구 Evidence
```

최신 파일이라는 이유만으로 권한이 생기지 않는다.

## 3. `압축해` Trigger Owner는 하나

Rebirth 설치 범위에서는 `root-engineering-rebirth`만 다음 실행을 소유한다.

- `압축해`
- `컴팩션`
- `채팅 정리해`
- `백업하고 압축해`
- 현재 Chat이 유효한 동안의 Same-thread Rehydration

동일 Trigger Scope에 별도의 `persistent-project-thread` Skill을 함께 설치하지 않는다. 검증된 동작은 Rebirth Skill에 흡수하고, 연구 저장소는 Evidence Link로 유지한다.

이 규칙은 다음을 막는다.

- Save Gate 중복 실행
- Compaction Priority 충돌
- Backup 이중 실행
- No-op Boundary 반복 발사
- 성공 상태 모호화

자동 Provider Thread Rollover는 현재 `1.0.0` 실행 Trigger 계약 범위 밖이다. 향후 버전이 이를 구현하더라도 Rollover Policy와 Persistence Gate의 단일 Owner는 Root Engineering이어야 한다.

## 4. 융합된 상태 모델

Rebirth는 이제 Thread/Session Surface를 Memory 및 Persistence Layer와 분리한다.

```text
THREAD / CHAT SURFACE
= 현재 Product-level 실행 Container. 유효한 동안 사용하지만 Project Identity 정본은 아님

CHAT TRANSCRIPT
= 사람이 보는 보존 History. Active Context와 독립적으로 계속 누적될 수 있음

ACTIVE MODEL CONTEXT
= 압축 가능한 모델 추론 작업 기억

LOCAL ROOT
= 프로젝트의 지속 가능한 Canonical 상태

CHECKPOINT
= Context 교체와 미래 Session 교체를 건너는 즉시 재개 Bridge

LOCAL CAPABILITY WORKSPACE
= 재사용 Skill, 검증된 Hot Path, Helper, Manifest, Runtime Asset
```

검증된 장기 ChatGPT Workflow에서는 Active-context Compaction을 반복해도 동일 Thread가 무기한 사용 가능해지지 않았다. 그 Product/Thread-level Boundary의 정확한 내부 원인은 알 수 없으며, 이 계약은 특정 OpenAI Retention Rule, Token Threshold, UI Threshold, Database Limit 또는 Private Implementation Detail을 주장하지 않는다.

구조 수준의 Invariant는 더 좁고 더 강하다.

```text
PROJECT / AGENT IDENTITY
    ≠ THREAD
    ≠ CHAT TRANSCRIPT
    ≠ ACTIVE MODEL CONTEXT
    ≠ TOOL / MODEL RUNTIME
```

`CHECKPOINT`는 장기 지식이 아니다. Local Capability Workspace도 두 번째 Root가 아니다. Thread 자체 역시 Root가 아니다.

Capability의 의미 정본은 다음이 소유한다.

- `knowledge/OPERATIONAL.md`: 검증된 절차, 실패 Fingerprint, Do-not-repeat
- `runtime/CAPABILITIES.json`: 가용성, Path, Hash, Scope, Verification State
- `ROOT.md`: 실제 Routing이 필요한 경우의 Pointer만

대형 Model, WAV, Cache, 생성 Artifact는 필요 시 Path/Hash로 연결한다. 기본적으로 Canonical MD에 복제하거나 Canonical Root Hash에 넣지 않는다.

## 5. Pre-Compaction Save Gate

의도적 Compaction은 Summary가 아니라 State Transaction이다.

고정 순서:

```text
1. 정확한 Local Root를 결정한다.
2. 필요한 만큼만 ROOT Routing과 현재 CHECKPOINT를 읽는다.
3. 마지막 Canonical Update 이후 새 Durable State를 찾는다.
4. 각 Durable Item을 가장 작은 Canonical Owner로 보낸다.
5. 실제 Root가 위치한 Filesystem을 검사한다.
6. 필요한 Owner를 Patch하고 CHECKPOINT를 갱신한다.
7. 모든 필수 Local Write를 Read-back 검증한다.
8. Canonical Digest + CHECKPOINT Hash를 Seal한다.
9. 설정된 Recovery를 이번 명시적 Compact Maintenance Window에서 동기화한다.
10. Capability Ladder에 따라 Active-context Compaction을 시도한다.
11. Compaction을 검증한다.
12. 검증 성공 후에만 Context Epoch를 증가시킨다.
13. BOOT → ROOT → CHECKPOINT → 필요한 Owner만 Rehydrate한다.
14. 해당 Thread가 유효한 동안 같은 Chat에서 계속한다.
```

따라서 Compaction은 **Context Maintenance 작업**이지 Thread의 영구성을 보장하는 기능이 아니다.

현재 Thread가 이후 사용 불가능해지더라도 `1.0.0` Package는 자동·투명 Rollover를 이미 구현했다고 주장하지 않는다. 명시적 Restore 또는 향후 Rollover Path를 시도하기 전에 Project State가 Root/Checkpoint와 설정된 Recovery Copy에 안전하게 저장되어 있어야 한다.

### 5.1 Root 결정 순서

1. 현재 지침이 지정한 명시적 Local Root Path
2. 이미 검증된 Active Root Binding
3. Project Local에 기록된 Root Entry Point
4. 실제 설치 경로로 검증된 경우에만 기본 `/mnt/data/root-engineering`

Local Root가 확정되면 Compaction 준비를 위해 File Library, Drive, GitHub, Web에서 경쟁 사본을 다시 찾지 않는다.

새 Durable State를 저장해야 하는데 신뢰 가능한 Root를 찾지 못하면 Compaction 전에 중단한다.

### 5.2 최소 Owner Routing

```text
ROOT.md                   → Identity, Authority, Routing, Compact Digest
knowledge/FOUNDATION.md   → 목적, 장기 원칙, 경계, Human Intent
knowledge/CURRENT.md      → 현재 사실, 결정, 상태, 제약, 중요 미결
knowledge/LEARNED.md      → 검증된 일반화 학습
knowledge/OPERATIONAL.md  → Hot Path, Capability 절차, 알려진 실패, Evidence Gate
knowledge/HISTORY.md      → 전환·Rollback·예방 가치가 남은 과거 상태
runtime/CHECKPOINT.md     → 즉시 작업 재개 상태만
runtime/CAPABILITIES.json → 실행 Capability의 Availability/Path/Hash/Scope
```

Transcript를 Dump하지 않는다. 기존 Owner가 있으면 두 번째 Canonical Owner를 만들지 않는다. 현재 Provider Thread를 Canonical Owner로 취급하지 않는다.

## 6. Local Storage Gate

Pre-compaction Save를 승인하기 전에 **결정된 Root Path가 실제 올라간 Filesystem**을 검사한다.

최소 검증:

- Filesystem과 Target Directory 존재
- Target Writable
- Patch/Checkpoint/Export에 필요한 Free Bytes
- Inode Accounting이 있으면 Free Inodes
- 실제 Write 후 Read-back 성공
- Candidate Write 실패 시 이전 Canonical 상태 보존

한 Chat Runtime에서 측정한 용량을 고정값으로 사용하지 않는다. Storage Size, Quota, Mount, Lifetime은 환경 속성이다.

> **필수 Local Save 실패 = No Compact.**

여유 공간과 영구성은 다른 문제다. `/mnt/data`가 크고 Writable이어도 모든 미래 Runtime에서 살아남는다는 뜻은 아니다.

## 7. External Backup 융합

외부 Backup 세부 정책은 `ROOT_ENGINEERING_1.0_BACKUP_POLICY.md`가 소유한다.

### 일반 `압축해`

```text
Local Root Save 검증
→ Canonical Root Hash 계산
→ External Adapter와 Target Binding이 실제 설정됐는가?
   ├── 아니오 → 외부 Write 없이 Compaction 계속
   └── 예
       ├── Hash 동일 → Upload Skip
       └── Hash 변경 → 검증된 `latest` 갱신
```

정책 문구가 있다는 것과 실행 가능한 Adapter가 있다는 것은 다르다. Google Drive 동기화는 다음을 모두 만족할 때만 성공으로 인정한다.

1. Google Drive Connector/Tool 또는 유효한 Adapter가 실제 가용
2. Project Backup Target이 모호하지 않게 Binding됨
3. Upload가 실제 실행됨
4. Upload된 Manifest/Bundle을 Read-back 또는 동등 방식으로 검증함

일반 `압축해`에서 선택적 External Backup이 실패하면 `external_backup_pending = true`로 기록한다. 검증된 Local Root는 계속 정본이며 경고 후 Compaction은 진행할 수 있다.

### 엄격한 `백업하고 압축해`

Local Save와 External Backup이 모두 검증돼야 한다. Adapter 부재, Drive Target 모호성, Upload 실패, Read-back 실패 중 하나라도 있으면 **No Compact**다.

### Authority 방향

정상 흐름은 단방향이다.

```text
Local Root → External latest/snapshot
```

Drive 변경을 Local Root로 자동 Merge하지 않는다. Restore는 명시적이며 Identity/Hash를 검증한다.

## 8. Compaction Capability Ladder

```text
A. Host가 실제 노출한 Supported Native Compact
↓ 불가
B. 동일 Scope에서 이미 검증된 Zero-output Boundary 정확히 1회
↓ 실패/검증 불가
C. 작은 단위의 Bounded Diagnostic Pressure
↓ 실패
STOP 후 진단
```

Private RPC를 만들어내지 않는다. No-op을 모든 Chat의 Universal Force-compact 명령으로 취급하지 않는다. 성공이 검증되면 즉시 Trigger를 중단한다.

Minefield 및 Trigger Reduction 실험은 Research Provenance이며 Production Assumption이 아니다.

Compaction 성공은 Active-context Maintenance가 성공했다는 것만 증명한다. 사람이 보는 Transcript가 줄었거나 Product Thread의 수명이 무한해졌음을 증명하지 않는다.

## 9. Transcript와 Thread 규칙

Compaction은 Active Model Context 유지보수다. 사람이 보는 Transcript 삭제 또는 압축 요청이 아니다.

검증된 Persistent Project Thread에서는 Active Context가 반복 압축된 뒤에도 과거 Message를 Scroll해 볼 수 있었다. 이후 장기 관찰에서는 성공적인 Context Compaction에도 불구하고 누적된 Thread가 결국 계속 작업할 수 없는 상태에 도달했다.

두 결과를 함께 유지해야 한다.

```text
사람의 과거 확인        → Transcript
모델 Working Memory 감소 → Compaction
현재 실행 Container     → Thread / Chat Surface
프로젝트 정본           → Local Root
즉시 작업 재개          → CHECKPOINT
재사용 행동 능력        → Capability Workspace
```

따라서:

> **Active-context Lifetime과 Thread Lifetime은 서로 다른 문제다.**

현재 ChatGPT-hosted 한계는 실험으로 발견된 Product/Thread Boundary로 취급하며, Root Engineering 연구의 종료로 취급하지 않는다.

연구 Evidence:

- `Valon-Jang/persistent-project-thread/evidence/LONG_HORIZON_THREAD_LIMIT_2026-09-05.md`

## 10. 연구 계속 — Thread-replaceable Continuity

반증된 질문은 다음이었다.

> **하나의 ChatGPT Thread를 어떻게 영구적으로 만들 것인가?**

Root Engineering은 더 일반적인 질문으로 연구를 계속한다.

> **Model, Context, Runtime, Thread가 교체되어도 Project는 어떻게 살아남는가?**

구조 수준의 연구 방향:

- 하나의 Stable Project Identity 뒤에서 Provider Session/Thread Rollover
- Fresh Execution Surface로 Root + Checkpoint Rehydration
- Raw History와 기본 표시 화면을 분리하는 Human-view Compression
- 전체 History를 Active Context에 넣지 않는 Transcript/Event Retrieval
- Model, Session, Runtime 교체를 견디는 Agent Identity
- Context를 Compact할 시점과 Session을 교체할 시점을 구분하는 Lifecycle Health Signal

이 항목들은 연구 방향이다. 현재 ChatGPT Rebirth `1.0.0`이 이미 투명한 Thread Rollover 또는 Human-visible Transcript Compression을 수행한다는 주장이 아니다.

일반화된 원칙:

> **Model은 교체 가능하다. Context는 교체 가능하다. Thread는 교체 가능하다. Root는 지속된다.**

## 11. MD 동기화 규칙

1. 영문 Installer가 Canonical이며 한글 Installer는 의미 동등본이다.
2. Backup 세부 내용은 Backup Policy 문서가 소유하고 다른 파일은 요약·Link만 한다.
3. Persistent-thread 실험 세부는 연구 저장소에 두고 Rebirth에는 검증된 운영 결론만 가져온다.
4. Skill은 Installer보다 짧게 유지하고 Canonical Owner로 Routing한다.
5. Production Rule 변경 시 영향받는 의미 동등본과 Validator를 같은 Patch에서 갱신한다.
6. 두 번째 `압축해` Canonical Owner를 추가하지 않는다.
7. 기존 Layout과 Identity Contract가 호환되므로 이번 융합에서 Package/Schema는 `1.0.0`을 유지한다.
8. Thread Replaceability 연구 결론을 이미 구현된 Transparent Rollover 기능처럼 표현하지 않는다.

## 12. Acceptance Gate

다음을 모두 만족해야 PASS다.

- Document Authority 명시
- Trigger Owner 하나
- Root 결정 후 Persistence 수행
- 실제 Root Filesystem Storage Health 검사
- Smallest-owner Save 및 CHECKPOINT Read-back 검증
- External Backup은 `EXPLICIT_COMPACT_ONLY` 기본, Hash-gated, Adapter-gated, One-way 유지
- 일반/엄격 Backup 실패 의미 분리
- Compaction 성공 확인 후 Epoch 증가
- 현재 `1.0.0` Scope에서 Same-thread Rehydration 정의
- 현재 Thread를 Canonical Project Identity나 영구 Resource로 취급하지 않음
- 별도 구현·검증 없이 Automatic Thread Rollover를 주장하지 않음
- Capability Asset이 두 번째 Root가 되지 않도록 Index됨
- 변경 Scope의 영문/한글 의미 불일치 없음
- 연구 저장소는 Provenance이며 Production Authority가 아님

---

> **Transcript는 남을 수 있다. Active Context는 압축할 수 있다. Thread는 그래도 끝날 수 있다. Checkpoint가 전환을 잇고 Root가 진실을 보존한다. Skill은 재사용 능력을 보존한다. 같은 Project는 교체 가능한 실행 Resource를 넘어 계속될 수 있다.**

> **Model은 교체 가능하다. Context는 교체 가능하다. Thread는 교체 가능하다. Root는 지속된다.**

Default external recovery trigger: `EXPLICIT_COMPACT_ONLY`; scheduled/idle/timer/background sync is disabled.
