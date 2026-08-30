from pathlib import Path
import re

EN = Path('installer/ROOT_ENGINEERING_INSTALLER.md')
KO = Path('installer/ROOT_ENGINEERING_INSTALLER_KO.md')

# English installer is already v0.1.12. Patch legacy VERIFY wording only when present.
s = EN.read_text(encoding='utf-8')
old = '→ verify the four default Branches in ROOT Map\n→ verify each Branch ID and Parent\n'
new = '→ verify the four default Knowledge Branches in ROOT Map\n→ verify each Knowledge Branch ID and Parent\n→ verify the Operational Memory direct specialist Node, ID, Parent, and exact fast-path index\n→ verify a matching known-failure record blocks unchanged same-path retry\n'
if old in s:
    s = s.replace(old, new, 1)
EN.write_text(s, encoding='utf-8')

s = KO.read_text(encoding='utf-8')

# Replace the legacy new-install sequence by stable section boundaries rather than exact full-block text.
install_new = '''5. ROOT Doc 생성
6. Foundation Doc 생성
7. Current Knowledge Doc 생성
8. Learned Knowledge Doc 생성
9. Operational Memory Doc 생성
10. History Doc 생성
11. 모든 Doc을 Project Folder로 이동
12. 실제 Document ID / URL / Parent Folder를 회수
13. 각 Template의 Placeholder를 실제 값으로 치환해 내용 작성
14. ROOT Map에 기본 4개 Knowledge Branch ID와 Operational Memory Fast-path Node 연결
15. ROOT Knowledge Lookup을 빈 표와 Coverage COMPLETE로 초기화
16. Operational Memory Fast-Path Index를 빈 상태로 초기화
17. 각 Knowledge Branch와 Operational Memory Node 내부 Root ID / Node ID / Parent 관계 확인
18. 모든 문서 Read Back
19. Project Instructions 완성본 생성
20. Manifest 상태를 AWAITING_PROJECT_BINDING으로 변경'''
if '9. Operational Memory Doc 생성' not in s:
    s, n = re.subn(
        r'5\. ROOT Doc 생성\n.*?18\. Manifest 상태를 AWAITING_PROJECT_BINDING으로 변경',
        install_new,
        s,
        count=1,
        flags=re.S,
    )
    if n != 1:
        raise RuntimeError('KO install sequence boundary not found')

old_tree = '''ROOT
├─ Foundation
├─ Current Knowledge
├─ Learned Knowledge
└─ History
```

- ROOT는 기본 4개 직계 Branch만 안다.
- `Knowledge Lookup`은 ROOT 안의 Routing Index이며 다섯 번째 Branch도, 두 번째 Source of Truth도 아니다.'''
new_tree = '''ROOT
├─ Foundation
├─ Current Knowledge
├─ Learned Knowledge
├─ Operational Memory  [Trigger-only Operational Fast Path]
└─ History
```

- Foundation, Current Knowledge, Learned Knowledge, History는 기본 4개 Knowledge Branch로 유지한다.
- Operational Memory는 비단순 반복 작업·복구·업그레이드·재시도·정확한 Known-failure 재발 가능성이 있을 때만 읽는 직계 Specialist Fast-path Node다.
- `Knowledge Lookup`은 ROOT 안의 Routing Index이며 Branch도, 두 번째 Source of Truth도 아니다.'''
if 'Operational Memory  [Trigger-only Operational Fast Path]' not in s:
    if old_tree not in s:
        raise RuntimeError('KO runtime tree boundary not found')
    s = s.replace(old_tree, new_tree, 1)

old_route = '재사용 가능한 검증된 방법·성공/실패 교훈\n→ Learned Knowledge\n\n과거 결정의 이유·큰 전환·Rollback·비교\n→ History\n'
new_route = '일반화 가능한 검증된 방법·성공/실패 교훈\n→ Learned Knowledge\n\n반복 작업의 정확한 실패 Fingerprint·Do-not-repeat·Preferred Path·Evidence Gate\n→ Operational Memory\n\n과거 결정의 이유·큰 전환·Rollback·비교\n→ History\n'
if old_route in s:
    s = s.replace(old_route, new_route, 1)

old_verify = '→ ROOT Map의 기본 4개 Branch 확인\n→ 각 Branch ID와 Parent 확인\n'
new_verify = '→ ROOT Map의 기본 4개 Knowledge Branch 확인\n→ 각 Knowledge Branch ID와 Parent 확인\n→ Operational Memory 직계 Specialist Node, ID, Parent, Exact Fast-path Index 확인\n→ Known-failure Record 일치 시 변경 없는 Same-path Retry가 차단되는지 확인\n'
if old_verify in s:
    s = s.replace(old_verify, new_verify, 1)

KO.write_text(s, encoding='utf-8')

for p in (EN, KO):
    t = p.read_text(encoding='utf-8')
    assert 'package_version: 0.1.12' in t
    assert 'P-021-OPMEM-CREATE' in t
    assert '<!-- BEGIN TEMPLATE: OPERATIONAL_MEMORY -->' in t
    assert 'Operational Memory Document ID' in t

ko = KO.read_text(encoding='utf-8')
assert '9. Operational Memory Doc 생성' in ko
assert '16. Operational Memory Fast-Path Index를 빈 상태로 초기화' in ko
assert 'Operational Memory  [Trigger-only Operational Fast Path]' in ko
print('v0.1.12 consistency patch PASS')
