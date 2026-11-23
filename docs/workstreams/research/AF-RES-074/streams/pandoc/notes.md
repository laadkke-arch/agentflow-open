# Pandoc 판독·반례·검산 (AF-RES-074 하위 묶음)

## 핵심 결과

자연 모집은 고정된 `docx`/`metadata` 두 검색 큐의 합집합을 번호순으로 읽었다. 첫12개는 **7008,7019,7022,7027,7028,7029,7030,7031,7033,7041,7054,7065**다.7008·7041은070 중복으로 제외했고, 나머지 중 처음 네 요구7019·7022·7027·7028을 그대로 유지했다.7030/7031은 동일 작성자·본문·첨부의 중복 사건으로 출처 최소량에서 함께1건만 센다. 후속 유무는 선정에 쓰지 않았다.

자연4건의 opening event는 모두 canonical GH Archive에서403이었다. 현재 본문을 먼저 읽었다는 사실과 최초판 미회수를 보존했으며, 이를 성공 사례로 교체하지 않았다. 따라서 원래 요청 시점의 독립 효과 분모는0이고, 이후 분석은 **현재판 재구성**이다. 자연4건×3정책×3분기36행은 모두 엄격 정오를 판정할 수 없다. 정책 내용·다음 행동의 기술적 판독은 따로 남겼다.

구성 대조2쌍은 공식2.11.3.2 회귀 시험의 동일한 입력·동일한 버전·다른 플래그1개다. `parse-raw.md`는 `raw_tex` on/off에 출력이 갈리고, `sloppypar.md`는 같은 필드를 바꿔도 저장된 기대 AST가 같다. 실행된 바이너리를 관측한 것은 아니다. 기대값 선노출·결과 기반 후보탐색이 있었으므로 두 쌍은 사후 구성 기술 대조이며 사전 예측 검정이 아니다.

## Q별 결과와 뒤집을 자료

| Q | 결과행·직접 원절 | 판독과 반례 | 미확인·최소 재개 입력 |
| --- | --- | --- | --- |
| Q1 | PAN-F01–12, PAN-N1–4; issue7019/7022/7027/7028 현재본문; test-origin.json | 최초본문4건 미회수. parse-raw 최초2017 기대직렬화는2019수정/2021tag와 다르며 sloppypar 최초2018은2021tag와 동일. | archive403이 해소된 원 opened event4개 또는 공개 편집원장. 단순 updated_at은 최초본문 증거 아님. |
| Q2 | packets-pre.json, C02 seal6a5dda48…; controls-pre.json,C03 0eb5235… | N1/N3의 목적은 현재본문에 이미있다. N2 literal lang 유지와 의미 보존을 혼동해 과잉질문 확정 철회. N4 새번호/원번호보존은 아직 구분안됨. | N2는 인용부호·폰트 결과를 보존할 다른 해법 허용범위; N4는 원 Word 번호의 exact preservation 조건. |
| Q3 | PAN-C1-CR=parse-rawL1–13; PAN-C2-CR=sloppyparL1–23 | raw_tex 같은toggle이 unknownmacro에서는 다르고 parsedsloppypar에서는 같다. 태그·입력·다른플래그는 일치. | 공식 저장 기대값과 공개실행은 다르다. 역사적tag를 실제 실행한 commit/환경/명령별 영수증은없음. |
| Q4 | policies.json54행, scores.json54행 | C1의 B는 보존목적을 아는 독자가 한 명령을 선택할 수 있는 조건부 기술답. N1/N3의 개발 경로 링크는 작업을 남기며 완성답이 아님. N2는 후보가 서로배타적이지 않음. | 실제독자가 조건을 식별·선택했다는 사용관측 없음. C1 purpose질문→raw_tex setting 매핑은 연구자설계. |
| Q5 | PAN-C2-CR, N1/N3 현재본문 | negative의 동일기대 AST는 질문 불필요의 기술근거. 무응답N3/N4 자체는 질문불필요 근거 아님. | 최초판복구 이후 known값 재질문 판정을 시간순으로 재확인. |
| Q6 | events.json;7019/758272588,7022/1236589386,1237700534 | N1은 이미있던 목적 반복. N2는 다른필드 진단, 유지보수자의fix/nightly보고이며 독립 OP성공 아님. N3/N4댓글0. | 선택한 같은필드 새값0은 현재판 재구성 관측; 질문효과0 아님. 우리후보 적용의 별도OP결과·정확fixSHA가 필요. |
| Q7 | empty_paragraphsL1–33; Docx.hsL251–273,L1024–1070; PAN-N2사후감사 | writer flag만 켜거나 reader flag만 켜면 빈문단이 소실되고 둘다켜야 보존. N2의script language 속성은 처음 고른목적필드 밖. | 한필드정책이 충분하려면 인접단계를 고정해야한다. multi-stage지원완성 여부를 새과제로 시험. |
| Q8 | policies literal_link_entries/unique_candidate_documents/roundtrips_required | A/B 추가대화0, C 설계상추가왕복1. 한문서의 서로다른절 링크를 문서2건으로 세지않음. C2음성에서는 C가분기선택을바꾸지못함. C1은 B만으로도 목적선택가능해 반드시한번질문할 근거가아님. | 실제왕복완료0, 사람이 소요한시간·응답확률미측정. 실행성공·문의빈도로 외삽하지않음. |

## 유지한 반례와 탈락

- `vars-and-metadata.md`는 template variables가 YAML메타데이터에 새지않는 저장기대값이지만 명령이1개다. 다른값의 결과를 스스로 만들어 음성쌍으로 채택하지 않았다.
- `smart.md`의 같은 출력 두명령 일부는 Markdown/RST writer까지 바뀐다. 같은필드 대비로 쓰지않고 추가열람으로만 남겼다.
- `empty_paragraphs.md`는 단일toggle의효과가 인접stage설정에 달리는 정확 반례다. natural군과 합산하지않는다.
- 현재 자연후보7029/7030/7054는 왕복형식·버전·다단계가 엮이며 다음슬롯으로 바꾸지않았다. 특히7030/7031중복을 두독립원작으로세지않는다.
- N2는 root와 별도 model감사자가 원문을 재판독해 문제를 제기했다. 작성자는 동의하고 post-analysis에 수정했다. pre는 변조하지않았다. 독립 사람 채점이 아니다.

## 자료량·검증범위

sources.jsonl32행 중 minimum_count=true인 고유work_id20개다: 요청9, 공식시험/예제5, 명세/매뉴얼/변경공지3, 구현코드3. 현재본문인 요청을 최초판복구성공으로 세지않는다.070중복2,7030/31중복1,댓글·복구실패·실패한Microsoft문서접근은 최소량에서 제외했다.

events.json19행은 현재본문4,댓글13,댓글없음확인2다. 두 없음확인은 실제 발언이 아니다. 원장 원행이 없는 실제 사용자선택·사람시간을 계산하지 않았다. 실제 보낸 질문0, 새 사람 접촉0, 독립 사람판독0이다.

## 실행하지 않은 재현

저장소의 Pandoc **2.11.3.2 / dcbd8d326cce4960e0d736e25e7d00f9057a1fc2** 빌드 또는 검증된 해당 릴리스 바이너리 환경에서 다음을 수행한다. 호스트에 다른 Pandoc이 있더라도 같은판의 증거로 대체하지 않는다.

1. 공식 `test/command/parse-raw.md` L3의 exact stdin을 두 명령 `pandoc -f latex+raw_tex -t markdown`, `pandoc -f latex -t markdown`에 각각 제공하고 L5/L12의 기대값과 비교한다.
2. 공식 `test/command/sloppypar.md` L3–7(두번째입력L15–19와 동일)을 `pandoc -f latex+raw_tex -t native`, `pandoc -f latex -t native`에 제공한다. 두stdout이 서로같고 L9–10/L21–22와 일치하는지 확인한다.
3. 공식 `empty_paragraphs.md` L3 AST를 L2/L10/L18/L26의 네파이프라인에 제공하고, 양단extension을 켠 마지막경우만 빈Para가보존되는지 확인한다.

stdin의 sourceSHA, hash, binaryversion, stdout/stderr, exitcode를 저장해야한다. 현재기록은 해당 실행을 했다는 주장이 아니다. 외부 질문 전송이나 원이슈 댓글 게시가 필요한 절차는 없다.
