# Root Engineering 1.0 Rebirth — 외부 백업 정책

상태: Root Engineering 1.0.0 Rebirth의 정식 운영 정책  
버전 영향: 없음. Package와 Schema는 모두 `1.0.0`을 유지한다.

## 1. 목적

Rebirth는 Chat 내부 Local Root를 현재 Runtime의 Primary Authority로 사용한다. Google Drive, Git, Export Bundle 같은 외부 저장소는 Backup·Recovery·협업·Migration Adapter다.

백업은 복구 가능성을 지키되, 일반 대화 Turn마다 외부 Write를 발생시키면 안 된다.

## 2. 핵심 규칙

> **Local 상태는 의미가 생길 때 저장하고, 외부 백업은 사건이 생길 때 동기화한다.**

일반 Chat에서 보이지 않는 Background Timer가 계속 작동한다고 가정하지 않는다.

```text
Local Root 변경
→ Local Write 검증
→ Canonical Root Hash 계산
→ 백업 Trigger까지 대기
→ Hash 동일: Skip
→ Hash 변경: 검증된 latest 백업 갱신
```

## 3. 기본 동기화 주기

| Event | 처리 |
|---|---|
| 일반 대화 | 외부 Write 없음 |
| 검증된 Local Root Patch | Canonical Hash가 바뀌면 Backup Pending 표시 |
| `압축해` / `compact` | Adapter가 연결되고 Hash가 바뀐 경우에만 `latest` 갱신 |
| 중요한 Authority·Routing·구조 변경 | Adapter가 있으면 즉시 `latest` 갱신 |
| `백업해` / `backup` | 즉시 검증된 `latest` 백업 |
| `백업하고 압축해` | 외부 백업 검증 성공을 압축 전 필수조건으로 사용 |
| `마무리하자` / 명시적 종료 | 변경이 있으면 `latest` 갱신 |
| Release·중요 Milestone·Migration·Restore·파괴적 변경 | `latest` 갱신 + 불변 Snapshot 생성 |
| Hash 변경 없음 | Upload 생략 |

현재 Runtime에서는 Local Root가 Authority다.

## 4. Latest와 Snapshot

권장 구조:

```text
Root Engineering Backups/
└── <PROJECT_ID>/
    ├── latest/
    │   ├── root-engineering-latest.zip
    │   └── BACKUP_MANIFEST.json
    └── snapshots/
        └── <ISO_DATE>_epoch-<N>_<REASON>.zip
```

`latest`는 복구용 교체 가능 백업이다. Upload와 Read-back/Hash 검증이 모두 성공한 뒤에만 새 백업으로 인정한다.

Snapshot은 다음과 같은 의미 있는 전환에만 만든다.

- Release 또는 이름 있는 Milestone
- Adapter/Runtime Migration
- 다른 Canonical 상태를 수용하기 전 Restore
- 중요한 Authority·Routing·Schema 변경
- 파괴 가능성이 있는 작업
- 사용자의 명시적 요청

Compaction마다 Snapshot을 새로 만들지 않는다.

## 5. Canonical Hash

다음과 같은 결정적 Export Set을 Hash한다.

```text
BOOT.md
ROOT.md
MANIFEST.json
knowledge/**
runtime/CHECKPOINT.md
runtime/STATE.json
runtime/CAPABILITIES.json
정책상 명시적으로 포함한 소형 Canonical Source
```

Scratch, Cache, Packaging 과정에서만 생기는 Timestamp 등 불안정한 비의미 데이터를 제외한다.

현재 Hash와 마지막 검증 백업 Hash가 같으면 외부 Upload를 생략한다.

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
  "verification": "PASS"
}
```

Manifest와 Bundle의 Identity·Hash가 일치해야 한다.

## 7. 실패 처리

필수 Local 저장과 선택 외부 백업은 다른 계약이다.

```text
Local Root 또는 CHECKPOINT 저장 실패
→ STOP
→ NO COMPACT
```

일반 `압축해`:

```text
선택 외부 백업 실패
→ 검증된 Local Root Authority 유지
→ external_backup_pending = true
→ 사용자에게 경고
→ Compaction은 계속 가능
```

엄격한 `백업하고 압축해`:

```text
Local 저장과 외부 백업 모두 검증 필수
→ 하나라도 실패하면 NO COMPACT
```

보류된 선택 백업은 다음 적격 Event나 `백업해`에서 다시 시도한다. 같은 실패 경로를 한 작업 안에서 반복하지 않는다.

## 8. Authority 방향

기존 Drive Root를 Rebirth로 옮긴 뒤에는:

```text
Drive Canonical 최신 Read
→ Local 변환
→ Local Identity/Content 검증
→ 최종 Migration Snapshot
→ 기존 Drive Root는 Legacy Read-only Recovery Source로 보존
→ 평상시 흐름은 Local → 외부 백업
```

정상 운영 중 External 변경을 Local Root에 자동 병합하지 않는다.

Restore는 명시적 작업이다. 복원 전에 다음을 검증한다.

- Project ID
- Root ID
- Version/Schema 호환성
- Backup Manifest
- Content Hash
- 복원 Scope

## 9. Runtime State

`runtime/STATE.json`의 권장 선택 필드:

```json
{
  "external_backup_adapter": "NONE",
  "external_backup_pending": false,
  "current_root_hash": null,
  "last_backup_root_hash": null,
  "last_backup_at": null,
  "last_snapshot_at": null
}
```

이 필드는 백업 상태를 추적하며 프로젝트 Truth를 변경하지 않는다.

## 10. 사용자에게 보이는 동작

일반 `압축해`:

```text
현재 작업을 저장 중입니다…
로컬 저장 완료. 복구본을 동기화 중입니다…
복구본 동기화 완료. 대화를 압축 중입니다…
압축 완료. 이어서 진행합니다.
```

선택 백업 실패:

```text
로컬 저장은 완료됐지만 복구본 동기화는 보류됐습니다. 대화 압축은 계속합니다.
```

엄격 백업 실패:

```text
로컬 저장은 완료됐지만 요청한 복구본을 검증하지 못해 대화 압축을 중단했습니다.
```

## 11. Acceptance 조건

다음을 모두 만족해야 PASS다.

1. Package/Schema Version이 `1.0.0` 그대로다.
2. 백업은 Timer가 아니라 Event 기반이다.
3. Canonical Hash가 같으면 Upload를 생략한다.
4. `latest`는 교체 인정 전에 검증한다.
5. Snapshot은 Milestone·명시 요청·Migration·중요 변경에만 만든다.
6. 일반 선택 백업 실패는 Pending 처리 후 Compaction을 계속할 수 있다.
7. `백업하고 압축해`의 백업 실패는 Compaction을 차단한다.
8. 평상시 Authority 방향은 Local → External이다.
9. Restore는 명시적이며 Identity/Hash를 검증한다.