# AF-RES-041 · 자체 점검과 반증 기록

이 문서는 같은 연구 작업 안의 재판독이다. 세 보조 세션의 교차 검토는 동일 모델 계열의 조사 분담이며, 독립 인간 검증이나 재현 실험으로 표시하지 않는다. 역사 프로그램은 실행하지 않았다. 정적 원문 열람·PDF 저장 도판 판독·자료 형식 검산을 구분했다.

## Q1–Q7 주장과 반증

| 질문 | 현재 주장·정확한 근거 URL/위치 | 반증하려고 실제로 찾은 경로와 결과 | 미확인 | 결론을 뒤집을 조건 |
| --- | --- | --- | --- | --- |
| Q1 정확 저작·판 | [Thành2000 pp117–118 refs40–43](https://www.tug.org/tugboat/tb21-4/tb69thanh.pdf), [Karow1997 p34 각주](https://www.numdam.org/item/CG_1997___27_34_0.pdf). [BA5635 서문 III](https://www.barenreiter.co.uk/prefaces/9790006493296_Innenansicht.pdf)는©1988·2008쇄·Dürr·BA5527의 관계. [ÖAW](https://schubert-digital.acdh-dev.oeaw.ac.at/W-01032.html)는NSA IV/14b pp196–218. 서지와 본문 관측은 별도. | 원 발행처→기관→원문 경로. Zapf Nottingham/NTNU 접근 실패, URW영어책자는 원본 URL·본문 미확보. IMSLP 원본 경로 실패 뒤 공식 Müller 견본과 판매자 Schubert raster를 판독했으나 정확 사용판으로 대체하지 않음. [Karow2015 p97 ref5](https://tug.org/TUGboat/tb36-2/tb113zapf-karow.pdf)의1992표기는 수신ref40의1993과 불일치. | URW1992/1993 판 관계, 영어 원판 직접 대조, HWN 사용 악보의 판·쇄·쪽·double-sharp 위치. | 원본 표제·간기·해당 쪽과 저자 사용본 연결이 확보되면 exact_donor를 재판정. 목록만 추가되면 본문 칸은 유지. |
| Q2 변경 전 선택 | [1996 p248 §7](https://tug.org/TUGboat/tb17-3/tb52sojk.pdf)에 폭 축/문단 줄바꿈 제안. [0.0.1](https://lilypond.org/download/sources/v0.0/lilypond-0.0.1.tar.gz) `lilyponddefs.tex` L3–10에musix20. 원안·최초 남은 구현·회고는 다른 단위. | 1997 설명서보다 앞선 논문,0.1보다 앞선0.0.1까지 추적. 0.1.13/15/19/23/27의 단계별 변경을 열어 ‘0.1 전체가 변경 전’ 가설을 반박. 보존0.12h의 실제 primitive·줄바꿈 부분도 확인. | 이러한 기록이 첫 원전 독서 전이었는지, 최초 미공개 선택은 무엇이었는지. | 1996 제안 또는 더 이른 원안의 구체적 선택이 첫독서 전임을 고정하고 후속 변경을 연결하는 당대 기록. 반드시1996보다 이른 기록만을 요구하지 않음. |
| Q3 저자 연결 | [Thành2000 §4 p38](https://www.tug.org/tugboat/tb21-4/tb69thanh.pdf)의 명시적 hz영감·구현정보부재. [1.0.1](https://lilypond.org/download/sources/v1.0/lilypond-1.0.1.tar.gz) `fonts.doc` L11–23·`feta-toevallig.mf` L11–27의 출판물·기호 명명. | 1998 pdfTeX 논문에는 hz 명명이 없고, 명시적 연결은2000회고 계통. LilyPond는1997 소스 자체에 귀속이 있어 순전한 후대 회고 가설을 약화. 반복 저작을 독립 증언으로 합산하지 않음. | 정확 자료의 어떤 규칙을 읽은 뒤 같은 최초 선택을 바꿨는지, 입수·독서 날짜. | 날짜 있는 메일·패치 설명에서 donor의 특정 규칙, 이전 선택, 바꾼 이유가 함께 확인됨. |
| Q4 같은 조작 | [Karow1997 pp49,54,56–57](https://www.numdam.org/item/CG_1997___27_34_0.pdf)와 [0.14f](https://ftp.math.utah.edu/pub/tex/historic/systems/pdftex/pdftex-0.xx-web2c/web2c-7.3.3-pdftex-0.14f.tar.gz) `pdftex.ch` L5108–5129. [0.1.22](https://lilypond.org/download/sources/v0.1/lilypond-0.1.22.tar.gz) L119–167 ↔[0.1.23](https://lilypond.org/download/sources/v0.1/lilypond-0.1.23.tar.gz) L114–205; `autometric.mf` L46–63,99–110. | Ek의 획 보존과 균일 가로 확대의 차이, hz가 유보한 합자, Feta의 sharp끝 미채택을 확인. flat의9/12→.8을 전체폭으로 읽는 초안도 반증: 이는w#이고 b#도 바뀜. | 정확 donor glyph와 구현의 수치 일치, 스캔이 원판인지 후대 재조판인지. | 인증된 판면과 같은 기호의 대응 규칙·변수가 확보되면 좁은 일치를 보강. 변형이 글자 정체성·편집 의미를 깨면 적용 카드를 축소. |
| Q5 반영 시점·범위 | [Thành2000 pp69–71](https://www.tug.org/tugboat/tb21-4/tb69thanh.pdf) level1/2, [2001 pp146–148](https://tug.org/TUGboat/tb22-3/tb72thanh.pdf),0.14f 정적소스. [Debian1997-10-20](https://lists.debian.org/debian-changes/1997/10/msg00023.html) HTML L564–573은0.1.22/23공개상한. | [1998 Fig1p285](https://tug.org/TUGboat/tb19-3/tb60than.pdf)과 [2004 Fig2p37](https://tug.org/TUGboat/tb25-1/thanh.pdf)는 각각 같은 논문 내부의 출력 짝으로 판독. [LilyPond2003 Fig5](https://lilypond.gitlab.io/static-files/media/xivcim.pdf),2006slides9/16은 후대 출력. [Vieth2007 slide11](https://tug.org/~vieth/papers/bachotex2007/tex-history-talk.pdf)의 archive재구성 한계 확인. | 첫 도입 릴리스의 정확 공개일, 보존archive의 원배포 바이트 동일성,1997동일 입력·설정 실제 출력. | 인증된 당시 배포·입력·font·설정·저장 출력이 연결되면 반영 범위를 강화. 함수 존재만으로 실행 성공을 인증하지 않음. |
| Q6 다른 설명 | [Thành2000 p38](https://www.tug.org/tugboat/tb21-4/tb69thanh.pdf), [Feta1.0.1 L25–27](https://lilypond.org/download/sources/v1.0/lilypond-1.0.1.tar.gz), [BA5635III](https://www.barenreiter.co.uk/prefaces/9790006493296_Innenansicht.pdf) ↔[NSA2022 p14](https://schubert-ausgabe.de/download/nga_editionsrichtlinien_7-_fassung_final.pdf). | 독자구현·이미정한방향·선택적모방·후대회고를 두 사건별로 비교. MPA/MOLA의 연주·배치 제약, [Bravura2013](https://blog.dorico.com/2013/05/introducing-bravura-music-font/)의다른본보기·매핑한계, [Petaluma2018](https://blog.dorico.com/2018/05/introducing-dorico-pro-2-and-dorico-elements-2/)의손필사선택을 실제 읽음. | Feta가 무시한 일반 특징을 관찰한 정확 악보판, Wanske 원책의 해당 규칙·언급부재, 미감과 실험적 가독성의 관계. | 특정 기호·장르·크기에서 반대 선택이 더 잘 작동한다는 같은 조건의 관측 또는 당대 기록이 확보되면 카드의 적용 범위를 수정. |
| Q7 판정·카드 변화 | SCOPE v1 원격`2021e2f`, `judgments.csv` 4행. B01에서는 [2000 p38](https://www.tug.org/tugboat/tb21-4/tb69thanh.pdf) 연결을 제거, B03에서는 exact_donor 접점을 제거하고 재판독. | 최초안0/2, 코드로 옮겨도 엄격완결0/2, 기능반영2/2를 별도 계산. B01제거시기능은남으나영감귀속은보류. B03는이미미확인인접점제거이므로불변이며견고성증거가아님. | 첫노출,현재탐색기회수가능성,정확원판짝의일치율. 적격짝0이므로비율은해당없음. | 사전다섯접점의결손을닫는관측이생길때만강도상향. 코드발견이나출판사계열일치만으로최초안인과를올리지않음. |

## 수량·중복·분모 자체 점검

- 필수 범주에 서로 다른 저작을 단일 배당했다. 고유 산입29: 인쇄4, 악보4, 수신10(B01=6/B03=4), 독립 발행·기관4, 반례6, 추가1. 명시22개 하한은 `streams/pdftex/corpus-review.md`에 있다.
- 같은 배포 파일, 미러·재인쇄·번역, 반복 열람, 실패, 검색 스니펫은 추가 산입하지 않았다. 원저자의 역사분석과 실제 과거 실물 검사는 구별했다.
- 두 LilyPond 릴리스를 한 진화 계통으로 묶어도 전체28, 수신9(B01=6/B03=3)이다. 고유 저작 수와 독립 인과 증언 수는 같지 않다.
- 네 판독은 B01-I/B01-C/B03-I/B03-C로 고정했다. 최초안 분모2와 코드 분모2는 별개이며 합쳐서 성공률을 만들지 않았다. 기능별18행도 사례 분모를 늘리지 않는다.
- 원장 필수14키·고유ID·산입저작군·출처참조, CSV 원문 문자열 보존, RESULT 첫4행/두번째2행/마지막3행, 카드2개×2링크를 실제 스크립트로 검산한다. 결과는 `evidence/validation.json`과 `evidence/artifact-table-check.json`.
- Artifact Tool의 날짜 자동변환은 text format을 먼저 지정하여 작성 단계에서 방지했다. CSV 재입력에서 정규화한 시각 개수는 기록하되, 배포 CSV의 정확 문자열은 Python csv로 따로 대조했다.

## 확인된 범위와 미충족 관측

원전 후보 조사·반증 시도·원장·코드 비교·카드 작성은 수행했다. 그러나 **정확 영어 원판, 정확 저자 사용 악보판, 첫 독서와 동일 최초안 변경의 연결은 미충족**이다. B03의 일반 sharp 특징 미채택 진술은 확인했지만, 정확한 특정 본보기의 기호와 나란히 놓은 완전한 반례쌍은 미충족이다. 역사 프로그램 재실행은 처음부터 제외된 범위다.

고정된 RESULT와 acceptance 파일을 다시 여는 작업 및 `workbench.session check --fetch`는 결과 묶음 커밋 뒤에 실행해야 하므로, 그 실제 SHA·결과는 마지막 별도 HANDOFF 커밋에 남긴다. 결과 수용 원장은 커밋 직전의 관측과 그 뒤에 남은 절차를 구분한다.

## 마지막 원문 재개봉과 교차 검토

`evidence/final-recheck-downloads.json`은 RESULT 초안 뒤 실제 URL을 다시 내려받은 시각·HTTP상태·SHA256을 담는다. `evidence/root-recheck.md`는 Q1–Q7의 정확 쪽·멤버·행을 root가 다시 판독한 기록이다. 재열람은 sources.jsonl에서 counted=false로 기록하며 고유 저작 수를 늘리지 않는다.

세 보조 세션의 `streams/*/result-review.md`에는 반증 검토와 수정 이유가 있다. 핵심 수정은 flat의 좌우 extent 구분, 버전 경계의 공변경과 실제 편집 동시성 구별, URW 미확보와 Zapf 접근실패 구별, 첫 독서 전 선택이 반드시1996보다 이른 문서일 필요는 없다는 SCOPE 원규칙의 유지다. 연구자는 이 검토를 독립 인간감사로 주장하지 않는다.

## 재개·검산 명령

저장소 루트에서 아래 명령은 원장·표의 재계산과 검산용이다. 외부 PDF와 archive는 해당 URL에서 정적으로 읽으며 역사 바이너리는 실행하지 않는다.

```sh
python -B docs/workstreams/research/AF-RES-041/evidence/merge-sources.py
"$CODEX_PRIMARY_RUNTIME_PYTHON" -B docs/workstreams/research/AF-RES-041/evidence/prepare-tables.py
"$CODEX_PRIMARY_RUNTIME_PYTHON" -B docs/workstreams/research/AF-RES-041/evidence/add-judgments.py
"$CODEX_PRIMARY_RUNTIME_NODE" docs/workstreams/research/AF-RES-041/evidence/write-tables.mjs
python -B docs/workstreams/research/AF-RES-041/evidence/validate.py
python -B -m workbench.session check docs/workstreams/research/AF-RES-041/manifest.json --fetch
```

정확 원판 접근이 계속 불가능하면 추가 일반 지침으로 대체하지 않는다. 첫 재개 자료는 RESULT 마지막 W1–W3 표의 식별자·쪽·버전이며, 접근실패의 실제 URL·범위·다음 자료는 원장과 frame.csv에 남아 있다.
