from pathlib import Path

EN = Path('installer/ROOT_ENGINEERING_INSTALLER.md')
KO = Path('installer/ROOT_ENGINEERING_INSTALLER_KO.md')


def replace_once(text, old, new, label):
    n = text.count(old)
    if n != 1:
        raise RuntimeError(f'{label}: expected 1 match, got {n}')
    return text.replace(old, new, 1)

# English VERIFY: explicitly validate Operational Memory.
s = EN.read_text(encoding='utf-8')
s = replace_once(
    s,
    '→ verify the four default Branches in ROOT Map\n→ verify each Branch ID and Parent\n',
    '→ verify the four default Knowledge Branches in ROOT Map\n→ verify each Knowledge Branch ID and Parent\n→ verify the Operational Memory direct specialist Node, ID, Parent, and exact fast-path index\n→ verify a matching known-failure record blocks unchanged same-path retry\n',
    'EN VERIFY operational memory',
)
EN.write_text(s, encoding='utf-8')

# Korean install sequence.
s = KO.read_text(encoding='utf-8')
old_seq = '''5. ROOT Doc 생성
6. Foundation Doc 생성
7. Current Knowledge Doc 생성
8. Learned Knowledge Doc 생성
9. History Doc 생성
10. 모든 Doc을 Project Folder로 이동
11. 실제 Document ID / URL / Parent Folder를 회수
12. 각 Template의 Placeholder를 실제 값으로 치환해 내용 작성
13. ROOT Map에 기본 4개 Branch ID 연결
14. ROOT Knowledge Lookup을 빈 표와 Coverage COMPLETE로 초기화
15. 각 Branch 내부 Root ID / Node ID / Parent 관계 확인
16. 모든 문서 Read Back
17. Project Instructions 완성본 생성
18. Manifest 상태를 AWAITING_PROJECT_BINDING으로 변경'''
new_seq = '''5. ROOT Doc 생성
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
s = replace_once(s, old_seq, new_seq, 'KO install sequence')

# Korean runtime tree: keep four default knowledge branches but expose specialist node.
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
s = replace_once(s, old_tree, new_tree, 'KO runtime tree')

# Korean routing block: distinguish generalized learning vs exact operational experience.
s = replace_once(
    s,
    '재사용 가능한 검증된 방법·성공/실패 교훈\n→ Learned Knowledge\n\n과거 결정의 이유·큰 전환·Rollback·비교\n→ History\n',
    '일반화 가능한 검증된 방법·성공/실패 교훈\n→ Learned Knowledge\n\n반복 작업의 정확한 실패 Fingerprint·Do-not-repeat·Preferred Path·Evidence Gate\n→ Operational Memory\n\n과거 결정의 이유·큰 전환·Rollback·비교\n→ History\n',
    'KO routing distinction',
)

# Korean VERIFY.
s = replace_once(
    s,
    '→ ROOT Map의 기본 4개 Branch 확인\n→ 각 Branch ID와 Parent 확인\n',
    '→ ROOT Map의 기본 4개 Knowledge Branch 확인\n→ 각 Knowledge Branch ID와 Parent 확인\n→ Operational Memory 직계 Specialist Node, ID, Parent, Exact Fast-path Index 확인\n→ Known-failure Record 일치 시 변경 없는 Same-path Retry가 차단되는지 확인\n',
    'KO VERIFY operational memory',
)
KO.write_text(s, encoding='utf-8')

for p in (EN, KO):
    t = p.read_text(encoding='utf-8')
    assert 'package_version: 0.1.12' in t
    assert 'P-021-OPMEM-CREATE' in t
    assert '<!-- BEGIN TEMPLATE: OPERATIONAL_MEMORY -->' in t
    assert 'Operational Memory Document ID' in t
    assert 'known-failure' in t.lower() or 'Known-failure' in t
print('v0.1.12 consistency patch PASS')
