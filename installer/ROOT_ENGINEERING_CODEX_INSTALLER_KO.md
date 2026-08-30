# Root Engineering — Codex 설치기

이 패키지는 Root Engineering을 재사용 가능한 Codex Skill로 설치한 뒤, 프로젝트 로컬 `.root/` 파일과 작은 `AGENTS.md` 연결 블록으로 하나의 저장소 또는 작업공간에 연결합니다.

Google Drive가 필요하지 않고, 기존 프로젝트 지침을 덮어쓰지 않으며, 전역 통합 지식 데이터베이스를 만들지 않습니다.

## 1. Skill 설치

Codex에서 다음 프롬프트를 전송합니다.

```text
$skill-installer install the skill from https://github.com/Valon-Jang/Root-Engineering/tree/main/installer/codex/root-engineering
```

내장 설치기가 `SKILL.md`가 있는 폴더를 내려받아 현재 Codex 프로필의 Skill 디렉터리에 설치합니다. 다음 Turn부터 사용할 수 있으며, 보이지 않으면 새 Codex 세션을 시작합니다.

사용자 전역 설치 없이 특정 저장소에서만 쓰려면 `installer/codex/root-engineering` 폴더를 다음 위치에 복사합니다.

```text
<저장소>/.agents/skills/root-engineering
```

## 2. 프로젝트 하나에 Root 초기화

대상 저장소나 작업공간을 Codex에서 연 뒤 다음 프롬프트를 전송합니다.

```text
Use $root-engineering to initialize Root Engineering in this project and run the bundled validation. Preserve all existing AGENTS.md content.
```

Skill은 구조가 없을 때만 다음 프로젝트 로컬 파일을 만듭니다.

```text
<프로젝트>/
├── AGENTS.md
└── .root/
    ├── ROOT.md
    ├── FOUNDATION.md
    ├── CURRENT.md
    ├── LEARNED.md
    ├── HISTORY.md
    └── nodes/
        └── OPERATIONAL_MEMORY.md
```

초기화 도구는 완전한 Root를 임시 경로에 먼저 만든 뒤 공개합니다. 일부만 존재하거나 유효하지 않은 기존 Root와 심볼릭 링크 대상은 거부하며, 기존 바이트를 보존한 채 표시된 Root Engineering 블록 하나만 `AGENTS.md`에 추가합니다.

## 3. 새 Codex 세션에서 검증

초기화한 프로젝트에서 새 Codex 세션을 열고 다음 프롬프트를 전송합니다.

```text
Use $root-engineering to identify this project's Root, read only the route needed for the current state, and report any unresolved fresh-session acceptance item without changing it.
```

다음 조건을 모두 확인하면 인수 검증을 통과합니다.

- `root-engineering` Skill이 발견됨
- 해당 프로젝트의 `AGENTS.md`가 로드됨
- 현재 checkout의 `.root/ROOT.md`가 선택됨
- `.root/CURRENT.md`로 가는 정확한 경로만 따라감
- 관계없는 Root 노드를 읽지 않음
- 새 세션 결과를 성공으로 추정하지 않고 관찰 증거로 보고함

검증이 통과한 뒤 Codex에 `.root/CURRENT.md`의 해당 미해결 항목을 실제 관찰 결과로 교체하도록 요청합니다.

## 4. 도구 직접 실행

Skill에는 외부 모듈이 필요 없는 PowerShell 도구가 포함되어 있습니다. 일반적으로 Codex가 대신 실행합니다.

```text
pwsh -File <skill-directory>/scripts/root_engineering.ps1 init -ProjectRoot <project-root>
pwsh -File <skill-directory>/scripts/root_engineering.ps1 validate -ProjectRoot <project-root>
pwsh -File <skill-directory>/scripts/root_engineering.ps1 validate-package
pwsh -File <skill-directory>/scripts/root_engineering.ps1 self-test
```

Windows에서 직접 스크립트 파일 실행이 차단되면 canonical 스크립트를 검토한 뒤 `powershell.exe -NoProfile -ExecutionPolicy Bypass -File`을 사용합니다. Bypass는 해당 프로세스에만 적용하며 컴퓨터나 사용자 실행 정책을 영구 변경하지 않습니다. PowerShell을 사용할 수 없으면 Codex가 포함된 템플릿을 작은 guarded patch로 생성할 수 있습니다. 기존 Root나 기존 `AGENTS.md` 내용을 덮어쓰면 안 됩니다.

## 5. 안전 및 범위

- 위에 표시된 canonical 저장소 경로에서만 Skill을 설치합니다.
- 패키지를 수정하기 전에 `SKILL.md`와 `references/PROTOCOL.md`를 검토합니다.
- Root 경로는 파일 접근, 승인, 신뢰, 권한을 부여하지 않습니다.
- 자격 증명, Secret, Token, 개인 키, `.env` 내용, 원시 인증 자료를 Root에 저장하지 않습니다.
- Git worktree에서는 `.root/`를 checkout 로컬로 취급합니다.
- 정적 검사만으로 설치 성공을 주장하지 않습니다. 프로젝트 검증과 새 Codex 세션 검사를 모두 실행합니다.

## 패키지 구성

```text
installer/codex/root-engineering/
├── SKILL.md
├── agents/openai.yaml
├── references/PROTOCOL.md
├── scripts/root_engineering.ps1
└── assets/templates/
```

Source: https://github.com/Valon-Jang/Root-Engineering  
License: [Creative Commons Attribution 4.0 International](../LICENSE)
