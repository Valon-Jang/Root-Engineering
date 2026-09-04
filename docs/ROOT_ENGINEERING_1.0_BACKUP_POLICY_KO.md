# Root Engineering 1.0 Rebirth — 외부 복구본 동기화 정책

상태: Root Engineering 1.0.0 Rebirth의 정식 운영 정책  
버전 영향: 없음. Package와 Schema는 모두 `1.0.0`을 유지한다.

## 1. 목적

Rebirth는 현재 Runtime에서 Chat 내부 Local Root를 Primary Authority로 사용한다. Google Drive, Git, Export Bundle은 복구본을 보관할 수 있지만 외부 동기화 때문에 평상시 Chat 작업이 느려지면 안 된다.

따라서 기본 정책은 명시적 Maintenance 경계를 사용한다.

> **사용자가 작업하는 동안에는 Local로만 일하고, `압축해` / `compact`라고 말했을 때 외부 복구본을 동기화한다.**

사용자가 명시적으로 `백업해` / `backup`을 요청하는 것은 허용한다. 예약, Idle, Timer, Background 동기화는 기본적으로 비활성화한다.

## 2. 왜 압축 시점인가

`압축해`는 이미 Rebirth가 다음을 수행해야 하는 순간이다.

1. Durable State를 정확한 Root Owner에 승격
2. 현재 작업 CHECKPOINT 갱신
3. Local Root 무결성 검증
4. Active Model Context 유지보수
5. Rehydrate 후 같은 Chat 계속

외부 복구본도 같은 시점에 처리하면:

- 평상시 작업 중 Connector Latency가 끼어들지 않고
- 이미 분류·검증된 상태만 백업하며
- 별도 예약 Runtime이 같은 Chat의 `/mnt/data`를 볼 수 있다고 가정하지 않아도 된다.

## 3. 기본 Trigger 계약

| Event | 외부 복구본 처리 |
|---|---|
| 일반 대화 | 없음 |
| 작업 중 Local Root Patch | Local 저장만 수행하고 변경 상태를 Local에 표시 |
| `압축해` / `compact` | 내용이 바뀌었고 Adapter가 연결된 경우 복구본 동기화 |
| `백업해` / `backup` | Compaction 없이 한 번 동기화 |
| `백업하고 압축해` | 외부 복구본 검증을 Compaction 전 필수조건으로 사용 |
| 예약 작업, Idle, Timer, Background Worker | 기본 비활성 |
| 의미/Hash 변경 없음 | 외부 Write 생략 |

Runtime State에 기록하는 기본 Trigger는 다음이다.

```text
EXPLICIT_COMPACT_ONLY
```

## 4. Transaction 순서

외부 Connector/Tool Boundary보다 먼저 Local Root와 CHECKPOINT를 안전하게 만들어야 한다.

```text
Durable Local Root 상태 저장
→ CHECKPOINT 갱신
→ Local Write 검증
→ Canonical Root Digest + Checkpoint Hash Seal
→ 결정적 Recovery Bundle Export
→ 연결된 외부 latest 복구본 동기화
→ 검증 또는 PENDING 기록
→ 아직 발생하지 않았다면 Active Context Compaction
→ 최소 상태 Rehydrate
→ 같은 Chat 계속
```

외부 백업 Tool 호출 자체가 Host Sampling Boundary가 되어 Compaction을 일으킬 수 있다. Compaction이 확인되면 그 Event를 현재 Transaction의 Compaction으로 사용한다. Rehydrate 후 Transaction을 완료하고 두 번째 Trigger를 실행하지 않는다.

## 5. Recovery Bundle과 Hash Gate

권장 외부 구조:

```text
Root Engineering Backups/
└── <PROJECT_ID>/
    ├── latest/
    │   ├── root-engineering-latest.zip
    │   └── BACKUP_MANIFEST.json
    └── snapshots/
        └── <ISO_DATE>_epoch-<N>_<REASON>.zip
```

일반 `압축해`에서는 `latest`만 갱신한다. 결정적 Bundle Hash가 마지막 검증 복구본과 같으면 외부 Write를 생략한다.

불변 Snapshot은 Release, 이름 있는 Milestone, Migration, Restore 경계, 중요 Authority/Schema 변경, 파괴적 작업, 사용자 명시 요청에만 같은 Maintenance Window 안에서 선택적으로 만든다. Compaction마다 새 Snapshot을 만들지 않는다.

## 6. Backup Manifest

최소 필드:

```json
{
  "project_id": "<PROJECT_ID>",
  "root_id": "<ROOT_ID>",
  "root_engineering_version": "1.0.0",
  "context_epoch": 0,
  "canonical_root_hash": "<HASH>",
  "backed_up_at": "<ISO-8601>",
  "backup_kind": "LATEST",
  "sync_trigger": "EXPLICIT_COMPACT_ONLY",
  "verification": "PASS"
}
```

노출된 Adapter를 통해 Identity, Artifact 존재, Content/Hash Evidence가 검증된 뒤에만 최신 복구본으로 인정한다.

## 7. 실패 처리

필수 Local 저장과 선택 외부 복구본 동기화는 서로 다른 계약이다.

```text
Local Root 또는 CHECKPOINT 저장/검증 실패
→ STOP
→ NO COMPACT
```

일반 `압축해`:

```text
선택 외부 복구본 동기화 실패
→ 검증된 Local Root Authority 유지
→ external_backup_pending = true
→ 실패 보고
→ Compaction은 계속 가능
```

엄격한 `백업하고 압축해`:

```text
Local 저장과 외부 복구본 모두 검증 필수
→ 하나라도 실패하면 NO COMPACT
```

PENDING 또는 미검증 Upload를 성공이라고 말하지 않는다. 한 번의 Maintenance 작업 안에서 같은 실패 경로를 계속 반복하지 않는다.

## 8. Authority 방향과 Restore

기존 Drive Root를 Rebirth로 Migration한 뒤 평상시 방향은 단방향이다.

```text
Local Root → 외부 복구본
```

정상 작업 중 외부 변경을 Local Root에 자동 병합하지 않는다. Restore는 별도 명시 작업이며 Project ID, Root ID, Version/Schema 호환성, Manifest, Content Hash, 복원 Scope를 검증한다.

## 9. Runtime State

`runtime/STATE.json` 권장 필드:

```json
{
  "external_backup_sync_trigger": "EXPLICIT_COMPACT_ONLY",
  "scheduled_backup_sync": false,
  "idle_backup_sync": false,
  "external_backup_pending": false,
  "last_external_backup": null
}
```

이 필드는 복구 상태와 정책을 나타내며 프로젝트 Truth를 바꾸지 않는다.

## 10. Complete Chat Runtime과의 관계

이 정책은 Rebirth의 **Complete Chat Runtime**, 즉 “완성형 Chat” 개념을 지원한다.

```text
일반 ChatGPT Chat
+ Local Root
+ Checkpoint
+ 명시적 압축 시점 외부 복구본 동기화
+ Active-context Compaction
= 작업 중 백업 지연 없이 오래 유지되는 하나의 프로젝트 Chat
```

“Complete Chat Runtime”은 Root Engineering의 용어이며 OpenAI의 공식 제품명이나 기능 주장으로 사용하지 않는다.

## 11. Acceptance 조건

다음을 모두 만족해야 PASS다.

1. Package/Schema Version이 `1.0.0` 그대로다.
2. 기본 복구본 동기화 Trigger가 `EXPLICIT_COMPACT_ONLY`다.
3. 예약, Idle, Timer, Background Sync가 비활성이다.
4. 외부 동기화 전에 Local Root와 CHECKPOINT를 검증한다.
5. 복구 내용이 동일하면 외부 Write를 생략한다.
6. 선택 Sync 실패를 숨기지 않고 PENDING으로 기록한다.
7. 엄격한 `백업하고 압축해` 실패는 Compaction을 차단한다.
8. 외부 Tool Boundary에서 확인된 Compaction을 재사용하고 이중 Trigger하지 않는다.
9. 평상시 Authority 방향은 Local → External이다.
10. 일반 작업 중 Routine External-backup Latency가 없다.
