# AF-RES-181 HANDOFF — PARTIAL (자체 판정)

## 결과판 및 검증 범위
- 결과 본문 SHA `668a3d89e4690752cfb5ee17fc83edffc1fa218c`; branch `work/research-af-res-181`. 이 HANDOFF 자체 commit SHA는 자기참조 불가, branch head/외부 반환값으로 확인.
- 시작 통합판 `6fa67328360b02bc7e7270d4ad3300bfe0f286bd`, 계획판 `128f673685ec804c526a38e3f89d4d8a43fcd299` (ahead 3 behind 0, dot-control만 변경); 선행 AF-RES-172 고정 `11d9eb0d498e8f9e7fa6eaa5f3425c2ce588d0f2` 중앙 DONE/자체 PARTIAL. 중앙 181 상태 미변경.
- 대표 파일: [RESULT.md](RESULT.md) 3개 지정 표 + Q1–7 + 마지막 약점 3건; [SELF_CHECK.md](SELF_CHECK.md); [assignments.csv](assignments.csv), [effort-quality.csv](effort-quality.csv), [bounds.csv](bounds.csv), [sources.jsonl](sources.jsonl), [frame.csv](frame.csv), [CONTRAST.md](CONTRAST.md), [OBSERVATIONS.md](OBSERVATIONS.md), [SCOPE.md](SCOPE.md).
- 실제 커밋/대표 파일 재열람: ① 351a14d1c2338079cc1847aed45a68098844e6ea SCOPE; ② 425edfe7357f8550429c6daf8ddc13dbb39649f1 frame; ③ b383a928859fac5ebf5b04432c1d0cca51db8355 assignments/effort; ④ 497fc9d4337523881b1212d13d8f304f612e5bdc sources/bounds; ⑤ 668a3d89e4690752cfb5ee17fc83edffc1fa218c RESULT/SELF_CHECK/sources; ⑥ 이 파일. ⑤ 직접 다시 읽어 처음 표 헤더/마지막 약점 3행과 ledger 36/26 direct/6 failed 확인. ③ fetched CSV 5행 합 2061853ms/111단어 직접 합산 확인. 독립 검토·raw XML 검산은 미수행.
- 좁은 판정: 같은 원문 3조건은 **세 사람 배정**이며 동일인 3조건 반복 아님. PET time은 방문별 사건시각 합; 긴 휴지·재방문·도구 밖 노동 판별 불완전. TUR 후보 doc1 HT processed 5행 2061.853s/111단어, 약 3.23 WPM. 같은 문서 PE1/2 및 ITA 원행 미관측. 논문은 최종 독립 후편집 평가를 범위 밖으로 두었으므로 실제 검수 포함 총인시 미확인. 번역→SW 비용 절감률 환산 없음.
- 부족: 8/8 예정 슬롯의 정확한 순위/완결 미확인, 24/24 raw 예정 문서×사람 자리 미확인; processed 1/24 배정, 나머지 23 조건 매핑 미확인. 5 processed segments, 0 raw event, 0 matched triplets, 0 independent QA joins; 두 언어 각 raw+조건+최종 출력 최소 충족 실패. 고유 직접 열람 26 (전체 36, 실패 6, metadata 2, abstract 2), design 4/4, analysis 8/4, raw work files 0/8 (처리판 1은 별도), 전사 4 보고서/0 역할별 원장, SW 4 incl 1 task CSV/0 독립 QA 시간표. 총 자료 수 초과만으로 완료 아님.
- 실제 반례: D08 필터가 ITA/TUR 자기 trigger가 0이어도 다른 언어에서 선택한 31/32 등을 삭제; E4 긴 pause; D01 Table12 동일 표면 ITA final의 다른 PE 편집량; OCR FindFix accuracy vs efficiency; METR 다른 과제의 0 repair와 missing 구분. 동일 원문 PE>HT 시간 원행은 미발견. 13.2 논문/노트북 열거 차이와 430/450 분모 혼용 재확인 필요.

## 다음 첫 행동: 고정 원본의 바이너리 열기
현재 GitHub text connector는 ZIP 내용을 제공하지 못했고 web raw download, 실행환경 외부 DNS, HF filter/offset 접근이 실패했다. 실패는 자료의 부재가 아니다. Codex Cloud 네트워크 허용된 환경에서 공개 파일만 가져오고, 절대 다른 release의 데이터를 합치지 말 것. 아래 명령은 **실행하지 않은 후속 입력**이다. PC/계정 접근/추가 유료 자원 불필요; 네트워크 차단이면 중단 사유 기록. 먼저 ZIP 내 모든 작업 파일과 완료/비완료 상태까지 목록화한 뒤 main doc ID 실제 순위 및 배정 roster 확인. `unzip` 전체나 preprocessing을 선행하면 비완료 파일 소실 여부와 raw 비교를 먼저 보존할 수 없으므로 원본 읽기부터 한다.

```sh
git clone https://github.com/gsarti/divemt.git divemt-af181
cd divemt-af181
git checkout --detach 934c4106001adeaa982a882d063f33ce0a398217
git rev-parse HEAD
git ls-tree -r --long HEAD data/raw
sha256sum data/raw/ita.zip data/raw/tur.zip
python3 - <<'PY'
import collections, pathlib, zipfile, xml.etree.ElementTree as ET
for lang in ('ita','tur'):
    p = pathlib.Path('data/raw') / (lang+'.zip')
    with zipfile.ZipFile(p) as z:
        print(lang, 'entries', len(z.namelist()))
        docs = collections.Counter()
        statuses = collections.Counter()
        errors = []
        for i in z.infolist():
            if i.is_dir() or not i.filename.lower().endswith('.per'):
                continue
            try:
                root = ET.fromstring(z.read(i))
                job = root.get('id','')
                status = root.get('status','UNKNOWN')
                parts = job.split('-')
                statuses[status] += 1
                if len(parts) >= 5 and parts[1] == 'main' and parts[2] == lang and parts[3].isdigit():
                    docs[int(parts[3])] += 1
                else:
                    errors.append((status,'non-main-or-key-schema'))
            except (ET.ParseError, OSError, ValueError) as e:
                errors.append((type(e).__name__,'parse-failure'))
        print('statuses',statuses,'distinct main numeric docs',len(docs),'first4',sorted(docs)[:4])
        print('first4 raw file counts',[(n,docs[n]) for n in sorted(docs)[:4]])
        print('other or failed',collections.Counter(errors))
PY
```

예상: main 연구 107 documents/430 segments per person(논문·notebook 보고), 사람×언어 매핑과 각 문서 세 조건 예정. 실제 수는 출력 결과로 정정. schema 가정 틀리면 D03 `per2metrics` root 및 annotation 구조를 먼저 읽고 맞춘다. 이 스모크 명령은 누락·비완료 구분을 위한 목록화로, 실제 배정표 대체 아님. archive entry 경로/파일명의 공개 익명키 여부 먼저 확인. ZIP 내부 README/배정표 포함 여부도 조사. 이후 정렬된 첫4에 대해 **모든 .per(비완료 포함)**, root id/status, producer 익명키, unit id, orig_id, mode, 각 annotation 마지막 이벤트 t 및 editing indicator, pause 계산, target presence/hash(UTF8 exact), src/draft hash 추출. D03/04 실제 파일명·folder 매핑 규칙으로 subject_id 대조하고 FINISHED-only 처리판과 left join; 파일 존재하지 않는 예정 배정도 남겨야 한다. 최종 output hash 단위로 독립 QA key 탐색; 없어도 0점/0분 처리하지 않는다. 결과는 비식별 키/집계만 저장; 전체 텍스트·개인 속성 미복제.

처리판 비교가 필요하면 HF 별도 입력 9abd1d1cea118ad7a9946e7f1f5a1a29c2a01762의 공개 파일/loader를 확인한 뒤, 동일 버전으로 불변 다운로드가 가능한 경우에만 비교. 먼저 schema, sha256, row counts, expected/observed conditions; D18의 5행(2061853ms/111 source words)을 검산. 고정 raw와 맞지 않으면 이유·판을 분리. 저자 notebook의 전언어 17개 제외 ID 정확히 복원하고 paper 13.2 차이 확인. 같은 원문 PE>HT 최소 1행, ITA/TUR 각 1행 time/condition/target 확인, 모든 예정 자리 상태 갱신. 같은 원문 비교 전 output quality 미확인이면 노동 차이는 translator-window에만 제한.

추가 대조층: DTA/Kokos/FindFix/ERP 원래 correction ticket 및 시간 원장(두 입력자와 독립 판정자); METR 공개 anonymous task CSV와 연결 가능한 별도 PR 수용/검수자 시간표. 미공개라면 직접 미확인으로 남겨야 한다. 소프트웨어 참여자 모집 및 Lattanzi/172 재실험 금지.

## 저장소 쪽 검산 (미실행)
```sh
git fetch origin work/research-af-res-181
git checkout --detach 668a3d89e4690752cfb5ee17fc83edffc1fa218c
git diff --name-only 6fa67328360b02bc7e7270d4ad3300bfe0f286bd HEAD
python3 - <<'PY'
import csv, json, pathlib, collections
p=pathlib.Path('docs/workstreams/research/AF-RES-181')
s=[json.loads(x) for x in (p/'sources.jsonl').read_text().splitlines()]
a=list(csv.DictReader((p/'assignments.csv').open()))
e=list(csv.DictReader((p/'effort-quality.csv').open()))
assert len(s)==36 and len({r['source_id'] for r in s})==36
assert collections.Counter(r['access_result'] for r in s)=={'direct':26,'failed':6,'metadata':2,'abstract':2}
assert len(a)==26 and len(e)==5
assert sum(int(r['event_time_ms']) for r in e)==2061853
assert sum(int(r['src_words']) for r in e)==111
print('ledger and current processed rows only OK')
PY
```
위의 출력 기대값은 현재 보존 파일 자체 검산용이지 외부 원행 재실행 성공 의미 아님. 후속 보정 커밋은 own path만. 기존 결과의 불확실성 유지, 독립 검토 상태 별도 표시.

색인 제안: AF-RES-181 | PARTIAL | DivEMT 동일 원문 다른 사람 조건 배정·PET ms/visit·독립 검수 노동 미관측; TUR HT processed 5행, 고정 raw/ITA/PE 매핑 부족; OCR/PR 대조 | RESULT.md + HANDOFF.md.
