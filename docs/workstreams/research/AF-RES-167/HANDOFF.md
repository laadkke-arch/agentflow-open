# AF-RES-167 HANDOFF
- 인계 상태: **PARTIAL** (핵심 판독·선정 하한 미달). 중앙 진행표는 수정하지 않았다.
- 결과판 SHA(이 HANDOFF 직전의 자기검산 포함 고정판): `9f1c3ccda5a4afe75da47645fca8746d352e5c8e`. RESULT 본문 커밋 `5b76dba5a2b1249e7732a94c0441e69180f17887`. 실제 시작판 `d32c697b4345442a4c91f62b8fb0bbed19e58034`; 계획 통합판 `ded3420249a3d60ebbb578a8432cf262d3ffa7d7`; 155 dependency `9a62426f9a989c3c0fff513f66a63d68484cbe3c`. HANDOFF 자체 SHA는 생성 시점에 자기기입 불가, 원격 브랜치 마지막 커밋으로 확인.
- 범위: `docs/workstreams/research/AF-RES-167/`만 작성. 결과판 compare에서 8개 변경 경로, 모두 owned_path 내부 확인. 로컬 checkout/test/build/변환 실행 없음.
- 원장 재검산: 원전 97 열람행, 고유 56(38 교환 후보/6 구현/8 규약·시험/2 MARC/2 AV), frame 268행, exchange 38, properties 43, links 7. 원장 ID 조인 오류 0. 보고상 양쪽 구현+파일명/값 11(6+5); I13 전체 파일 미공개로 전체 공개 사건만 10(6+4), IFC 1 부족. 양쪽 제품 판+고정 공개 파일 보고 I10 한 건(목표 10 중 9 부족); 직접 파일·정확판·수신값 조인 0(10 부족). 자연층 첫 8+조건부 8 미확정, 포럼 통합 순서 미복원 및 후보 원전 미판독. 자연쌍 직접 확인 0/적격 분모 미확정; 완결 왕복 0. 구문/화면/편집/왕복은 별도. MARC 기관 migration 보고2는 읽었지만 두 구현 간 태그별 실제 교환 두 건 미달(확정 0/2); A01/A02 원면 screenshot 접근 오류, 본문 텍스트 직접 판독. 표준·구현 문서의 정확한 당시판 대응 부족. SELF_CHECK는 자기검산.
- 주요 결과: 형식명의 동일성은 값 이전 보증이 아니다. I04 원파일 IFC2X3 단위 FOOT=0.3048m 및 precision0.0001 직접 확인; 수신판 미확인. I10 Archicad24 add-on3008→Bonsai fcee54c의 pinned 파일/경계 차이 보고를 확인했으나 ZIP 내용 직접 검증 없음. M11/I15/I02는 설정·화면·질의 원인 반례; M05/I12는 왕복 결론 금지.

## 단계별 커밋(모두 원격에서 해당 파일 재열람)
| 묶음 | SHA |
|---|---|
| ① 범위 | 74732e80783666a0387f1feab66f583c4c3ece25 |
| ② 모집 | f38be3e3a4871fabe6275e8a13e60555bc6c3f57 |
| ② 원전 | 698758d3ed977773c452bfde389d3b396348d818 |
| ③ 교환 | bb6b7b789bf84685ae4188b4fb07d549d4f508d2 |
| ③ 속성 | 8291ae2a7a813798bf6cdcd0d2c0a004bfee865a |
| ④ 원창 확장 | d2937dbfcbde6261efc08dca4191d0ed777fdb7f |
| ④ 보강 원전 | 4e5512f9abb1fc11bef1df071aa7e3cbed8e4ed8 |
| ④ 교환 보정 | 6ac4d6c581d1258ed848c876ef53b478ab398f4a |
| ④ 속성 보정 | 36e4f326cb74ede14b5e97cfa97623b1fea94dfa |
| ⑤ 링크 | 31ed7179bfbab651c7c44d89388f6a9a2102ce14 |
| ⑤ 분모 보정 | dfc1e66369abd5363ac2eb4382ea13ecb981884d |
| ⑤ 결과 | 5b76dba5a2b1249e7732a94c0441e69180f17887 |
| ⑤ 자기검산 | 9f1c3ccda5a4afe75da47645fca8746d352e5c8e |

## 다음 첫 행동 / 공개 재개 입력
1. 고정 결과판의 frame.csv를 읽고 M0/I0 최초 미판독 원순위부터 날짜/번호/요구·상대도구·파일/값을 직접 판독. M0/I0 반환 각 100행을 재선별하지 않고 이어서 첫 적격 8을 고정하고 조건에 맞으면 다음 8. buildingSMART forum의 공개 날짜/번호 목록을 복원하여 별도 프레임/병합 순서를 명시. 불가능하면 자연층 PARTIAL 유지. 이후 정확판·파일 접근 보강, 실제 양판 조인 9 추가, 수신값 10 직접 검증, MARC 2 태그별 실제 교환 보고를 추가한다.
2. **작은 왕복 후보 M05** (아직 양 배포판 확정 조건 미달): [원 보고](https://github.com/musescore/MuseScore/issues/24870), [원본 8va ZIP](https://github.com/user-attachments/files/17090130/8va.musicxml.zip), [편집 ZIP](https://github.com/user-attachments/files/17090148/8va-edited.musicxml.zip). MuseScore 4.4.2 확정, Finale 정확 배포판 미확인(추측 금지). Codex는 원 ZIP을 공개 경로에서 확보해 파일명/해시와 MusicXML identification/encoding/software 확인, 이슈 원 작성판을 고정할 수 있는 경우만 해당 두 배포판으로 시험. 원본 Finale의 E가 8va에 포함되는 기대(당사자 보고), grace-note octave, octave-shift type/down/start/stop의 앞뒤 note ID를 비교. Finale source→MusicXML 원본→MS4.4.2 import→MS export→원 Finale 동일 판 import; 각 단계 원값/편집 객체/재생/표시를 따로 기록. edited ZIP은 별개 조건. Finale 판/배포판 사용 권한 확보 실패면 실행하지 말고 결측 유지. 공개 파일을 이번 세션에서 읽지 못했으므로 이 사례를 재현 완료나 왕복 검증으로 간주하지 않는다.
3. **정확판 보고가 있는 단방향 I10**: [보고 #6113](https://github.com/IfcOpenShell/IfcOpenShell/issues/6113), 고정 입력 `https://raw.githubusercontent.com/CyrilWaechter/IfcRelSpaceBoundary_TestFiles/851d80d82d3470765baccd1f8133a7ff7ee31d59/IfcRelSpaceBoundary2ndLevel/Triangle_AC24_IFC4.ifczip`. 송신 Archicad24.0.0 FRA FULL IFC add-on3008, EDM5.02.0100.09; 수신 Bonsai fcee54c, Blender4.3.2, exact IfcOpenShell geom library 판 추가 확인. 원 #5889 IfcCurveBoundedPlane의 closed triangle(보고 4점 첫=끝, 기대 3 unique vertices/nonzero face); #5915 reversed orientation, 보고 shape.verts 6 scalars=2 3D points. Tab 전후 표시와 모델 관계/face가 정말 달라지는지 분리. 다음 명령은 실행하지 않았으며 Codex 입력으로만 넘긴다.

```sh
curl -fL 'https://github.com/user-attachments/files/17090130/8va.musicxml.zip' -o 8va-original.zip
sha256sum 8va-original.zip
unzip -l 8va-original.zip
curl -fL 'https://raw.githubusercontent.com/CyrilWaechter/IfcRelSpaceBoundary_TestFiles/851d80d82d3470765baccd1f8133a7ff7ee31d59/IfcRelSpaceBoundary2ndLevel/Triangle_AC24_IFC4.ifczip' -o Triangle_AC24_IFC4.ifczip
sha256sum Triangle_AC24_IFC4.ifczip
unzip -l Triangle_AC24_IFC4.ifczip
# exact Bonsai/IfcOpenShell 환경과 배포판 확보 후 원문/shape 확인
python - <<'PY'
import ifcopenshell, ifcopenshell.geom
f = ifcopenshell.open("Triangle_AC24_IFC4.ifczip")
print(ifcopenshell.version, f.schema)
for n in (5889, 5915):
    print(f.by_id(n))
s = ifcopenshell.geom.create_shape(ifcopenshell.geom.settings(), f.by_id(5889))
print("verts", s.verts, "faces", s.faces)
PY
```

실행 제한/정확 환경 미확보 시 재개 입력과 원문만 확인한다. 직접 확인하지 않은 ZIP 내부 값은 원문 보고에서만 왔다.

## 후속 검사 명령 (미실행)
```sh
git fetch origin chore/workspace-foundation work/research-af-res-155 work/research-af-res-167
git diff --name-only d32c697b4345442a4c91f62b8fb0bbed19e58034 9f1c3ccda5a4afe75da47645fca8746d352e5c8e
git diff --check d32c697b4345442a4c91f62b8fb0bbed19e58034 9f1c3ccda5a4afe75da47645fca8746d352e5c8e
git show 9f1c3ccda5a4afe75da47645fca8746d352e5c8e:docs/workstreams/research/AF-RES-167/SELF_CHECK.md
python -m workbench.session --help
```
로컬 workbench session start/check 미실행; 해당 작업의 허용 경로 및 dependency 고정 입력은 SCOPE에서 확인하고 repository의 실제 명령 도움말에 맞춰 실행. 원격 API로 결과판 7종 재판독·행/ID 계산은 이미 수행.

색인 제안: `exchange-evidence` — 요구 속성 × 송신판/프로필 × 동일 파일 key × 수신판 × 구문/화면/편집/왕복 × 첫 결측/설정 × 사양·구현·실사건 링크.

| 불일치·약점 | 영향을 받는 판단 | 다음 조사와 자료 | 결론을 뒤집을 관측 |
|---|---|---|---|
| 파일 링크/값 보고와 바이트·양판·수신값의 동시 확인 차이 | 실제 이식 가능한 속성 및 왕복 | I10 pinned ZIP, M05 original ZIP/Finale 판, I16 EXAMPLES.zip | 정확 두 판과 동일 원본에 대한 요구값·수신값·재출력 값 직접 일치/결측 |
| 자연층 첫 적격 8 및 포럼 통합 순서 미확정 | 대표성·자연 성공과 실패 비교 | frame 최초 미판독 원순위, forum 공개 archive, 순서 고정 후 판독 | 완결 자연 프레임에 같은 파일 비교와 조건별 판정이 존재 |
| 화면·설정·질의의 차이와 값 소실 혼재, MARC 태그 원면 부족 | 원인 귀속 및 기능 링크 충분성 | M11/I15/I02의 설정 반례, 역사판 두 절, A01/A02 및 태그별 migration 원전 2건 | 동일 바이트/설정에서 표시만 다른 경우와 실제 값 삭제 분리, 태그별 수락 결과 확인 |
