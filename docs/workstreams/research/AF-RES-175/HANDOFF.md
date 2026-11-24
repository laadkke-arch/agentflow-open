# HANDOFF — AF-RES-175
**작업자 판정: PARTIAL.** 중앙 진행표는 변경하지 않았다. 작업 중 확인한 AF-RES-175 RUNNING과 선행 167 DONE은 중앙 상태이며, 선행 worker PARTIAL과 이번 worker PARTIAL을 구별한다. 8자리 원보고 판독 8/8, 같은 객체·판·원값·수신값 완결 0/8, 실제 왕복 0. 자료원장 57행, 고유 본문 work 23, 층별 하한 미충족. 개별 제출 파일 내용 0/6, 적격 보충 시험 0/2, 엄격 AV/MARC 개별 수용 결과 각각 0/3, 역사판 계열 문서 3/6 및 정확 두 제품판 옵션 미확인. 단위 count 7/16과 표시 14열 분모 조인 미완료. 독립 검토·새 변환·설치 없음.

## 고정판 / 원격 결과
- 계획 입력: 53eaa286136019510f052179f5f51d901bdac858; 시작 통합: 2ca38b464dcf72fc2570d77f44cc29ee7c9a4cbc; 선행 HANDOFF: 0d7917cc6ba0a2a0d161a3f45a1d9763030a90e7.
- 작업 브랜치 work/research-af-res-175. 모든 수정은 docs/workstreams/research/AF-RES-175/에 한정.
- 결과 체크포인트(이 인계문 직전): 357d92b426841bdae9a9ff7f258df3e535e476ed. HANDOFF 자체 SHA는 이 파일의 커밋 후 확인한다(자기참조 SHA를 미리 기입하지 않음).
- ① SCOPE 4715291df8abf19178ce87d36815653e861f3c0b, ② frame 70f4b5f803d865ff571b2f2affe119d705bc51dc / sources 14dcd14e09db280ca3b57c47e30cab0ee19e1523, ③ models 351069d5c63cab3015ca2bf54d7d10cafe06f326 / directions 56a029b49fa0b986906caf99229bf3d003564ea2, ④ 보강 sources 85c4d9c9d9474171930120834f39525e1e5f41dc / scope dd6086cc35ebf472204d73c6698c4790558cb99b / frame 531b17701c234da9853cad0c50de867be8c2e1c7 / models b8a37a02fb5c2c75efdaf7692e8909b856e68bac / advice 334d5ca25e0e165c5fea6e22f2f7013b8d026199, ⑤ RESULT 3a3a1d382a10dc05d064419073417460f9b54ed2 / SELF_CHECK 357d92b426841bdae9a9ff7f258df3e535e476ed. 각 파일 커밋의 원격 내용 일치 확인.
- 대표: [RESULT](https://github.com/laadkke-arch/agentflow-open/blob/3a3a1d382a10dc05d064419073417460f9b54ed2/docs/workstreams/research/AF-RES-175/RESULT.md), [SELF_CHECK](https://github.com/laadkke-arch/agentflow-open/blob/357d92b426841bdae9a9ff7f258df3e535e476ed/docs/workstreams/research/AF-RES-175/SELF_CHECK.md), sources.jsonl, models.csv(GD01–15 directory-only), directions.csv, advice.csv.

## 첫 재개 행동 (명령 미실행, 다운로드/판독만)
새 변환이나 독점 소프트웨어 실행에 앞서 공개 보고 자료를 확보한다. 원 모델은 저자 사용 조건과 허용 범위를 확인한 뒤에만 내려받는다. 실행 공간은 owned_path 밖의 임시 저장소를 쓰되 repo에 쓰지 않는다. 결과의 파일명/지문/실제 읽은 행만 owned_path에 추가. 웹의 429/400은 계속 재시도하거나 우회하지 말고 정상 접근 가능한 환경에서 제한에 맞춰 작업한다.

```sh
# 먼저 작은 공개 설문 xlsx, 이어 최신 인간 판독 PDF; 실패하면 중단하고 원주소 기록
mkdir -p /tmp/af-res-175
cd /tmp/af-res-175
curl -fL --retry 0 'https://zenodo.org/records/3964445/files/Task1_complete_anon.xlsx?download=1' -o reports.xlsx
printf '%s\n' '46b45b8eed8e2d6199b9f875d0448eea  reports.xlsx' | md5sum -c -
curl -fL --retry 0 'https://zenodo.org/records/6470370/files/1Task_DelResults_Rlinks.pdf?download=1' -o reports-v2.pdf
printf '%s\n' '0ab606fd83e743064570ad50dd5ea6ad  reports-v2.pdf' | md5sum -c -
pdftotext -layout reports-v2.pdf reports-v2.txt
grep -niE 'Myran|FreeCAD|ArchiCAD|Allplan|AutoCAD|FME|Tekla|Revit' reports-v2.txt | head -100
# openpyxl이 이미 있는 환경에서만 시트/열 확인(설치 요청 아님)
python - <<'PY'
import openpyxl
w = openpyxl.load_workbook('reports.xlsx', read_only=True, data_only=True)
for s in w:
    print(s.title, s.max_row, s.max_column)
    for row in s.iter_rows(min_row=1, max_row=min(3,s.max_row),values_only=True):
        print(row)
PY
# ZIP은 약 5GB이므로 저장공간/정상 접근 허용 확인 뒤에만 수행.
# 먼저 Zenodo 3964368 메타데이터에서 checksum을 가져와 대조할 것.
curl -fL --retry 0 'https://zenodo.org/records/3964368/files/benchmarkTask1_exportedIFC.zip?download=1' -o exported.zip
unzip -l exported.zip
# unzip -p exported.zip '<GD01의 실제 경로>' > freecad.ifc
# sha256sum freecad.ifc
# head -40 freecad.ifc
# grep -niE 'IFCDERIVEDUNIT\(|IFCDERIVEDUNITELEMENT\(|IFCUNITASSIGNMENT\(' freecad.ifc | head -60
```

GD01–07 후보와 보고 참가자/원표 열을 매핑한 뒤 원 Myran IFC2x3 CV2.0 원판 지문을 확인; 첫 GlobalId/단위값/공간 관계, G4 대응 속성의 고정 순서를 유지하여 STEP 참조를 읽는다. 제출 파일에서 같은 객체 또는 증명된 매핑의 값/단위·관계 확인. 빈 Revit 등도 파일명 크기만으로 확정 금지. PDF/설문 데이터가 열려도 원본 접근/정확 판이 없으면 PARTIAL 유지. S는 [Table7](https://www.mdpi.com/2076-3417/11/23/11430)과 Fig6의 50 kN/m, 25 kN를 시작 입력 후보로 유지하되, native/IFC 원본, 부호, 대상, 좌표계, unit, load case, restraint DOF, 정확 A/B 구현판·MVD 및 실제 수신값 미확보. 따라서 아직 재생할 수 있는 특정 조합이 없다. 자료 확보 이후 Codex Cloud로 넘기며 새로운 실제 변환은 이번 범위 밖. R14–16 다음 원 참고문헌 순으로 적격 공개시험 2개 확보; AV/MARC 기관별 실제 동일 키 수용 결과를 각 3개 찾는다. 동수·다른 실제값 반례는 미확보.

저장소 검사(미실행; 정상 git checkout 있는 작업자):
```sh
git fetch origin chore/workspace-foundation work/research-af-res-175
git switch work/research-af-res-175
git diff --name-only 2ca38b464dcf72fc2570d77f44cc29ee7c9a4cbc HEAD
git diff --check 2ca38b464dcf72fc2570d77f44cc29ee7c9a4cbc HEAD
python - <<'PY'
import json,csv,pathlib
p=pathlib.Path('docs/workstreams/research/AF-RES-175')
r=[json.loads(x) for x in (p/'sources.jsonl').read_text().splitlines()]
assert len(r)==len({x['source_id'] for x in r})==57
assert len({x['work_id'] for x in r if x['include_unique_read']=='yes'})==23
for name,expected in [('frame',34),('models',29),('directions',10),('advice',6)]:
    with (p/(name+'.csv')).open() as f:
        assert len(list(csv.DictReader(f)))==expected
PY
```
GitHub API 자기검사로 JSON 행/참조, 각 커밋 대표 파일 재열람 완료. 로컬 git/checkout session 검사 미실행. 독립 검토 아님.

색인 제안: `AF-RES-175 — PARTIAL; G Table7 분모 불일치와 제출 목록 후보, S Table7 버전/방향별 정성 등급, 속성별 보류·재시험 입력(advice.csv), 원값 조인 0/8; 후속 원자료 확보 필요.`
