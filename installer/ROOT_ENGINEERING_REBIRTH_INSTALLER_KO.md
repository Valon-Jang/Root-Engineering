---
package_id: root-engineering-rebirth
package_version: 1.0.0-rc.1
codename: Rebirth
status: release-candidate
target_environment: 쓰기 가능한 /mnt/data와 Python 실행이 있는 일반 ChatGPT 채팅
primary_storage: chat-local-filesystem
project_required: false
google_drive_required: false
context_compaction: host-owned-observed-transaction
---

# Root Engineering 1.0 — Rebirth 설치기 RC.1

> **모델은 교체할 수 있다. Context도 교체할 수 있다. Root는 남고 같은 Chat은 계속된다.**

이 패키지는 하나의 일반 ChatGPT 채팅을 장기간 유지하기 위한 로컬 Root Runtime을 설치한다. ChatGPT의 비공개 압축 서비스를 구현하거나 흉내 내지 않는다. Host가 수행하는 압축 전후에 프로젝트 상태를 저장·검증·복구한다.

## 설치 실행 계약

이 문서와 `ROOT_ENGINEERING_REBIRTH_INSTALLER.py`가 현재 채팅에 있으면 설명만 하지 말고 가능한 절차를 실제 수행한다.

```bash
python /mnt/data/ROOT_ENGINEERING_REBIRTH_INSTALLER.py self-test
python /mnt/data/ROOT_ENGINEERING_REBIRTH_INSTALLER.py \
  --root /mnt/data/root-engineering \
  install --project-name "<프로젝트 이름>"
python /mnt/data/ROOT_ENGINEERING_REBIRTH_INSTALLER.py \
  --root /mnt/data/root-engineering verify
```

Self-test, 쓰기 Preflight, 전체 구조 생성, Identity 일치, Digest, Readback이 모두 통과한 뒤에만 ACTIVE로 판정한다.

## 설치 구조

```text
/mnt/data/root-engineering/
├── BOOT.md
├── PROTOCOL.md
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
├── sources/INDEX.md
├── tools/
│   ├── rebirth_runtime.py
│   └── noop_boundary.py
└── scratch/
```

## `압축해` 트랜잭션

명령 의미는 다음과 같다.

```text
Persist → Checkpoint → Verify → Compact → Rehydrate
```

사용자에게 보이는 진행 문구:

```text
현재 작업을 저장 중입니다…
저장 완료. 대화를 압축 중입니다…
압축 완료. 이어서 진행할게.
```

실행 순서:

1. `PROTOCOL.md`, `ROOT.md`, `runtime/CHECKPOINT.md`와 새 Durable State가 들어갈 정확한 Owner만 읽는다.
2. 사실·결정·검증된 방법·실패/Hot Path·History를 가장 작은 올바른 경로에 저장한다. 대화 전체를 넣지 않는다.
3. 압축 후 바로 재개할 정확한 다음 행동을 Checkpoint에 기록한다.

```bash
python /mnt/data/root-engineering/tools/rebirth_runtime.py \
  --root /mnt/data/root-engineering checkpoint \
  --goal "<현재 목표>" \
  --active-work "<진행 중 작업>" \
  --completed "<완료 내용>" \
  --promoted "<Root에 승격한 상태>" \
  --unresolved "<중요 미결>" \
  --next-action "<정확한 다음 행동>" \
  --resume "BOOT, ROOT, CHECKPOINT를 읽고 다음 행동에 필요한 Owner만 불러와 계속한다."
```

4. 저장 트랜잭션을 봉인한다.

```bash
python /mnt/data/root-engineering/tools/rebirth_runtime.py \
  --root /mnt/data/root-engineering prepare-compact --reason user-requested
```

5. 저장 또는 검증이 하나라도 실패하면 즉시 중단한다. **Save failure = no compact.**
6. Host가 공식 Native Compact Action을 실제 노출할 때만 우선 사용한다. 그렇지 않으면 같은 환경에서 이미 검증됐고 성공을 관찰할 수 있을 때에만 Zero-output Tool Boundary를 정확히 한 번 사용한다. 비공개 RPC를 지어내거나 대량 Pressure Text를 기본값으로 쓰지 않는다.
7. 압축 성공을 실제 관찰했을 때만 Epoch를 전진시킨다.

```bash
python /mnt/data/root-engineering/tools/rebirth_runtime.py \
  --root /mnt/data/root-engineering complete-compact \
  --observed \
  --method zero-output-boundary \
  --signal CONTEXT_REPLACEMENT_OBSERVED
```

8. 성공 여부를 확인할 수 없으면 Abort한다.

```bash
python /mnt/data/root-engineering/tools/rebirth_runtime.py \
  --root /mnt/data/root-engineering abort-compact \
  --reason "compaction not observed"
```

9. `BOOT.md`, `ROOT.md`, `runtime/CHECKPOINT.md`와 필요한 Owner만 읽고 동일 Chat에서 정확한 다음 행동부터 계속한다.

`complete-compact`는 Prepare 이후 Canonical Digest나 Checkpoint Hash가 달라졌으면 Epoch 전진을 거부한다.

## 백업

`/mnt/data`의 수명은 Host가 통제한다. 중요한 시점에는 Snapshot을 Export한다.

```bash
python /mnt/data/root-engineering/tools/rebirth_runtime.py \
  --root /mnt/data/root-engineering export
```

Google Drive와 GitHub는 선택적 Backup/Recovery Adapter이며 평상시 필수 의존성이 아니다.

## RC 경계

현재는 최종 `1.0.0`이 아니라 `1.0.0-rc.1`이다. 동일 Chat 반복 압축·복구·마이그레이션 Evidence가 Release Gate를 통과하기 전에는 안정 0.x 설치기를 대체하지 않는다.
