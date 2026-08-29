---
package_id: root-engineering-chat-updater
target_package: root-engineering-chat-installer
target_version: 0.1.5
schema_version: 0.1.0
release_date: 2026-08-29
primary_entry_phrase: "업데이트 파일 읽고 기존 설치를 업데이트해."
direction: forward-only
patch_registry_url: https://raw.githubusercontent.com/Valon-Jang/Root-Engineering/main/installer/patches/README.md
fresh_installer_url: https://raw.githubusercontent.com/Valon-Jang/Root-Engineering/main/installer/ROOT_ENGINEERING_INSTALLER_KO.md
---

# ROOT ENGINEERING — 기존 설치 업데이트 v0.1.5

> **이 파일은 기존 설치를 업데이트한다. 새로 설치하지 않는다.**
>
> 공식 패치 파일은 영어 원본 하나만 사용한다: [patches/README.md](./patches/README.md)

## 실행 규칙

이 파일을 읽은 AI는 연결된 도구가 허용하는 범위에서 업데이트를 실제로 수행한다.

1. 기존 Project Binding, Global Manifest, Project Manifest를 찾는다.
2. 두 Manifest에서 Package ID, Package Version, Schema Version, 문서 ID, 설치 상태를 읽는다.
3. Package ID가 `root-engineering-chat-installer`인지, 두 Package Version이 같은지, 한 프로젝트가 명확한지 확인한다.
4. 공식 [패치 목록](./patches/README.md)을 읽는다. 필요하면 앞부분의 raw URL을 사용한다.
5. 확인한 현재 버전에서 `0.1.5`까지 빠짐없는 정방향 경로를 정한다.
6. 적용 직전에 해당 패치 파일 전체를 읽는다.
7. 패치의 `from_version`이 현재 확인된 버전과 정확히 같은지 확인한다.
8. 패치에 적힌 작업만 수행하고 `must_not_touch` 범위를 보존한다.
9. 패치 검증이 성공한 뒤에만 두 Manifest의 Package Version을 `to_version`으로 바꾼다.
10. 변경 범위와 두 Manifest 버전을 다시 읽고 다음 패치로 진행한다.
11. 두 Manifest가 모두 `0.1.5`이고 마지막 검증이 통과해야 완료한다.

## 경로 선택과 중단 조건

```text
기존 Binding 또는 Manifest가 없음
→ 중단: 기존 설치를 확인할 수 없음

두 Manifest가 이미 0.1.5
→ 쓰기 없이 마지막 검증만 수행

두 Manifest가 목록에 있는 낮은 버전
→ 공식 경로를 따라 패치를 하나씩 적용

두 Manifest 버전이 서로 다름
→ 중단: 두 값을 알리고 임의 선택 금지

설치 버전이 0.1.5보다 높음
→ 중단: 다운그레이드 금지

시작 버전 또는 다음 구간이 목록에 없음
→ 중단: "누락 패치: <from> → <to>"를 알리고 추측 금지
```

INSTALL을 실행하거나 대체 폴더를 만들거나 프로젝트 문서를 다시 생성하거나 문서 ID를 바꾸거나 패치 단계를 합치지 않는다. 이전 버전 기억을 패치 지시로 사용하지 않는다. Updater, 목록, 패치 파일을 Project Source에 영구 추가하지 않는다.

웹 연결을 사용할 수 없으면 사용자에게 이 업데이트 파일, `patches/README.md`, 결정된 경로에 필요한 정확한 패치 파일만 첨부해 달라고 요청한다.

## 마지막 검증

- Global/Project Manifest Package Version이 모두 `0.1.5`다.
- 정확한 패치가 달리 지시하지 않는 한 Schema Version은 `0.1.0`이다.
- 기존 문서 및 폴더 ID가 바뀌지 않았다.
- 기존 프로젝트 지식과 Source, Skill 내용이 보존됐다.
- 새 채팅에서도 같은 프로젝트 기록을 찾아간다.

확인한 시작 버전, 적용한 패치 파일명, 최종 버전, PASS/FAIL만 보고한다.
