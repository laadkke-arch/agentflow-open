# AF-RES-046 · 자체 재판독과 반증 점검

## 검토의 성격

이 파일은 결과가 좋아 보이는지 평가하는 서술이 아니라 Q1~Q7에 필요한 고리와 그 고리를 깨는 자료를 다시 연결한 기록이다. 담당 AI가 자기 원문을 재판독했고, root는 L-S2의 첫 링크·사전 실패·작성자 설명·실제 diff 및 pandas의 양성/음성 반응을 별도로 재열람했다. 다른 AI가 선택 원장·저작 중복·분모·시간 산술을 대조했다. **외부 독립 인간 판독, 완전한 눈가림 코딩, 참여자 실험은 수행하지 않았다.**

자체 재열람 시각은 각 sources.jsonl 영수증의 checked_utc와 stream 자체 검산 파일에 있다. root가2026-11-22 22:32:38.775Z에 직접 다시 연6원문은 `streams/root/sources-supplement-recheck.jsonl`의 RR-Q1/RR-P2-R/RR-P2-C/RR-P1-R/RR-COST/RR-S1-C다. 앞선 L-S2 독립 재열람은 `streams/root/audit-L-S2.md`와 root source R-LS2-*에 있다. 같은 저작의 재방문은 최소수에0을 추가한다.

## Q1~Q7 답·반증·최소 뒤집기 자료

| 질문 | 현재 답과 원장 | 직접 다시 연 원문·정확한 위치 | 결론에 반대되는 관측 또는 탐색 경로 | 판정을 바꿀 최소 자료 |
|---|---|---|---|---|
| Q1 어떤 PR이 들어오는가 | 4개 query×40=160행, 자연8+추가4 슬롯. 자연 순번P3/9/11/14,S2/4/5/8; 링크P6/13,S3/6. 표본 바꿔치기 없음. frame.csv·selection-freeze.json | [25268 review1233732288](https://github.com/scikit-learn/scikit-learn/pull/25268#pullrequestreview-1233732288)의 commit_id d5a1cbaf와 changelog 요청; 공개 opened 이벤트와 정확 base...head compare는 초기판 복원 영수증에 기록 | current commits=[]라서 초기 코드 없는 변경으로 오인할 수 있었으나 옛 review head에서 복구. #25272 surviving판의 committer 시각이 개설 뒤인 문제를 발견하고 공개 opened head33ee1f59의 실제 test-only diff로 재검토. R01 및 후속 reviewer 단서 노출은 남음 | 결과를 가린 별도 코더가 같은 query와 당시 body/diff만으로 앞선 탈락·첫4/2를 재현. 다른 적격 선행행 발견 시 frozen 원장 유지한 채 대안 집계를 추가 |
| Q2 링크 전에 무엇을 골랐는가 | 실제 최초 opened head/base/body와 링크 전 review head를 분리. 모두 현재판과 동일하다고 가정하지 않음. baselines.csv·initial-public-heads.csv·streams/pandas/initial-public-head-recovery.json·streams/sklearn/initial-public-head-recovery.json | [bf9e2641](https://github.com/scikit-learn/scikit-learn/commit/bf9e2641c811e177870880a28b8b3a1e0b19e6a9)의 _tree.pxd/.pyx; [a897a34d testing helper](https://github.com/scikit-learn/scikit-learn/commit/a897a34d7d989bf317de17f80948639c0fd5ecf1); 생성 당시 body/compare 재조회 | 50523 현재body의issue50514,25540의25484와완료문구가 후첨. 51116 earliestcommit과openedhead가 다름. 25535 최초head도링크전a897과다름. 따라서 현재body나gitauthor date만으로 당시지식을 소급할 수 없음 | 해당 이벤트/compare가 다른PR/판이라는 반증 또는 원형 GitHub event 원문과 충돌하는당시push기록. 링크직전실제head까지필요한사례는누락push복원 |
| Q3 누가 무엇을 읽었는가 | 첫 적격URL4건. 명시적 읽음/최초발견 확인0/4. target내용관여2/4, 제안응답3/4를 별도코딩. events.csv/cases.json | [P51109 댓글1454857966](https://github.com/pandas-dev/pandas/pull/51109#issuecomment-1454857966)의 _name 비교와timeit; [P51116 댓글1474292973](https://github.com/pandas-dev/pandas/pull/51116#issuecomment-1474292973)의52043/52053; [S25540 댓글1416936430](https://github.com/scikit-learn/scikit-learn/pull/25540#issuecomment-1416936430)의인용·감사 | 감사만으로열람판정을올리면L-S2가양성으로과장됨. P2는target의기존작성자라‘처음알았다’와반대. S1은외부프로젝트사전명명이나특정workflow열람은없음 | 특정원문·판을읽었고그때처음알았다는당사자발언, 또는명시적기존인지발언. 자료없는노출을비노출로바꾸지않음 |
| Q4 같은 작성자가 같은 목적을 바꿨는가 | 기본2/4확인(기존로직통합1), P1미관측1, S1미확인1. 타인포함4확인. 첫링크엄격확인0/4. changes.csv38행 | [f95152e7](https://github.com/pandas-dev/pandas/commit/f95152e78c8baa2b1f4e07ecebb31496b3956c65): any/all→_cython_agg_general/ WrappedCythonOp, 별도_bool_agg삭제. [eb6a658b](https://github.com/scikit-learn/scikit-learn/commit/eb6a658b0ada3464e0fa79da716f57af053141fe): constfloating→DOUBLE_t. [feaabb7e](https://github.com/scikit-learn/scikit-learn/commit/feaabb7e6f2ccecced7a6847a267ad54b026f8a3): 다른작성자의xfail/예외제거 | P2후속52089의f951 공개미확인정정은유지. R04에서는[19e8640](https://github.com/pandas-dev/pandas/commit/19e864062c0d253db1b10469876b553391dad0db)의첫부모대비2파일통합·링크후생성부모1f7a·종결전review1349064316으로독립양성을확인. 사전작성로직통합을새설계창작과구별. S1패치작성자는fcharras로원작성자ogrisel과다름. 같은S2PR의더강한두번째링크사슬을첫사건으로바꾸지않음 | 원작성자누락후속SHA·공개시각·같은요구diff, 또는firstlink가그변경이유였다는당사자연결문장과대응시험/반영 |
| Q5 어느 단위가 사람 노동인가 | 주창 직접로그0/12·표본작성자소요시간자기보고0/12·동등품질시간쌍0/12. 값과절감량은미확인. labor.csv | [issue25261 Describe the bug](https://github.com/scikit-learn/scikit-learn/issues/25261):소비자manyhours,2022-12-30. [51109 timeit block](https://github.com/pandas-dev/pandas/pull/51109#issuecomment-1454857966); [eb6a658b metadata](https://github.com/scikit-learn/scikit-learn/commit/eb6a658b0ada3464e0fa79da716f57af053141fe) | 노동언급자체가전혀없다는결론은틀림:소비자정성비용은있다. 그러나사람/창/단위가다름. 139292초·17.2s·6.31s·commit13개를작성자작업시간으로환산하지않음 | 행위자와같은요구가명시된시작/중지로그또는본인수치소요시간,그리고동등품질무링크비교쌍. 후자는절감판정에추가필수 |
| Q6 링크 이외의 설명은 없는가 | 링크전실패/선행patch,타인수정,설명만변경,설계유지,후기회귀를보존. counterexamples.md | [P52043](https://github.com/pandas-dev/pandas/pull/52043)03:36:48·[P52053](https://github.com/pandas-dev/pandas/pull/52053)16:00:14와firstlink18:45:21; [S25540 사전실패1416766187](https://github.com/scikit-learn/scikit-learn/pull/25540#issuecomment-1416766187), [caller1418381186](https://github.com/scikit-learn/scikit-learn/pull/25540#issuecomment-1418381186); [OSM node history v3/v4](https://api.openstreetmap.org/api/0.6/node/11329057532/history) | OSM실제수정은링크26초전. MB포럼은취소/대체보고뒤규범제시이지만실제편집원장403으로적용미확인. 무링크N-P1실제수정도있다. 링크만유일한설명이아님 | 링크전수정이전혀다른목적이었다는diff근거,시간순서를뒤집는공개원본,MB개별노트/적용판. 원인추정에는별도비교설계필요 |
| Q7 어느 수준까지 말할 수 있는가 | 참고가능; 주창동일인변경2확인(통합1)·1미확인과종결뒤f951실재를분리; 첫발견유발수정/노동절감일반수치불가. RESULT필수표2·statistics | 표1의4첫링크·실제patch·작성자응답, [MusicBrainz How to Write Edit Notes](https://musicbrainz.org/doc/How_to_Write_Edit_Notes), [OSM Key:opening_hours](https://wiki.openstreetmap.org/wiki/Key:opening_hours) | 원문54개가있어도음악필수원장1개미달. linked4/4는선정조건. 무링크8과같은품질시간대조가아님. 대상PR자체가최초설계뒤에생긴경우정확그주소의조기제공반사실도불성립 | 충분한선정재현·첫발견/이유연결·동일인실제patch·정해진품질·작업로그·대응비교를함께확보한새사례. 0조건부분모는해당없음유지 |

## 관측 뒤 바뀐 내용과 원래 집계 보존

R01은 추가층 조건의 오적용을 고쳤다. 원본 규칙과 중간 원격 SHA는 REVISIONS.md에 보존한다. N-S2는 봉인 당시 provisional이었다. 후속 리뷰head·opened이벤트복구로 구체 구현을 확인했지만 슬롯을 교체하지 않았다. 최초 공개판 복원 전 집계는 묶음3 `57d749eeae66a1e62b5e75cce644c6ba82b5d47b`에 남는다. 역사적 첫판은0/12에서12/12공개미러+정확diff복원으로보완했고(rawevent독립확인0/12), R02에서는링크4·같은작성자변경2·엄격0·측정가능노동0이유지됐으나R03공개경계대조로같은작성자확정을1,미확인2로낮췄다. 원2/4는c9afe55커밋에보존하고새분모를다시검산한다.

복원으로 바뀌는 것은 초기head/base/body와 당시에 제시했던 후보의 근거다. 현재body의후첨링크를초기인지로쓰던표현을고쳤다. publicevent1초차는별도필드다. 첫공개판을복원했다고링크전후모든push나원작성자사적작업까지확인한것은아니다.

## 별도 AI 원장 대조에서 수정한 오류

`streams/crossdomain/final-ledger-audit.md`는 읽은입력의UTC/SHA256과조치결과를남긴다. pandas additional영수증누락,sklearn종료창pending,타인L-P1의선행수정을동일인flag와혼용할위험,L-S1의잘못된exceptions파일경로를확인하고수정했다. 작업중갱신된cases입력지문은마지막재생성으로동기화한다. 자연층의변경0은첫링크조건부확정수이며실제무링크수정0이아니라는해석을명시했다.

## 검산과 고정 결과 재열람

`python -B docs/workstreams/research/AF-RES-046/synthesize.py`, `assemble.py --stage all`, `validate.py`로 슬롯·원장 join·고유저작·날짜·감도·표행수를검산한다. 실제로그는 evidence/validation.json이다. 지시된 `python -B -m workbench.session check docs/workstreams/research/AF-RES-046/manifest.json --fetch`는 2026-11-22T23:07:21.471908+00:00~23:07:34.854842+00:00에 실제 실행했다. exit0/status=passed, outside_paths=[]/unmerged_paths=[]/errors=[]이며 원 stdout·stderr·UTC는 evidence/session-check.json에 보존했다. 검사 당시 최신 통합판89203e81a83d51e581ef81fb04c7573753f87234과 최초 시작판4492dd8e9978087b32897ec2685110d24f510473은 별도 기록하며, 검사 도구는 계약 일치를 확인했다.

RESULT와acceptance-evidence는원격결과커밋을먼저만든뒤그SHA로두파일을다시읽는다. 실제확인SHA·blob/내용검사·표행수는evidence/fixed-result-recheck.json에후속보존한다. 그다음HANDOFF만마지막단독커밋으로작성한다. 이파일의예정절차만으로재열람을완료했다고간주하지않는다.

남은미충족은음악개별편집원장접근,완전한선정결과가림,첫링크의엄격연결·사람시간/반사실이다. acceptance-evidence의각항목에분자·분모·단위·원장행·이유·최소후속을분리한다. 근거가없어엄격분자가0인것과실제효과가0인것을끝까지구별한다.

## R03 · 스스로의 양성 집계를 뒤집은 공개 경계 확인

pandas52089는원PR종결45초전개설됐지만정확f95152e를고정한첫회수근거가20:36:41의[review1349354160](https://github.com/pandas-dev/pandas/pull/52089#pullrequestreview-1349354160)로종결17:38:10뒤였다. source RR-LP2-FIRST-PUBLIC과pandas sources-supplement-successors를직접대조했다. 그래서기본동일인2/4→1/4(미확인2),타인포함4/4→3/4(미확인1)로둘다낮췄다. 후기실제코드변화·선행재설계·엄격0·노동미확인은유지한다. 빈opened조회는코드부재증거가아니므로0변경으로내리지않았다.

소비자25261비용문구는IssuesEvent개설본문에서확인돼시점공백을해소했다. 타인후속25605는openedhead=feaabb7e로확인했고정확head관측상한은REST개설보다1초뒤09:22:47이다. 두사실은기존사람/창/노동단위구분을바꾸지않는다. 각보완파일은stream원장과별도로저장해원해석을숨기지않았다.

## R04 · 하향 판정에도 반례를 적용한 후속 통합 확인

R03 중간1/4·3/4는 원격416c6739ce24c7a2f77f4fd6911655363834652a에 보존했다. f951의 잘못된 공개 연결은 되살리지 않았다. 대신52053의4commit을 다시 열어19e8640의 첫 부모3ce5 대비 any/all result_mask 실제2파일 변경을 확인했다. [부모1f7a의GitHub생성/병합](https://github.com/pandas-dev/pandas/commit/1f7a7f20b1a3aeb66527df0d9a3682159e56917e)19:48:49에서 통합 하한을 추론하고, [review1349064316](https://github.com/pandas-dev/pandas/pull/52053#pullrequestreview-1349064316)3/20 17:17:26에서 공개 상한을 직접 확인했다. 작성자ID8078968·같은목적diff·정확tree시험은 final-risk-review.json과P-FR-8개영수증에 연결했다.

최종 동일인2/4·타인포함4/4, 미확인동일인은L-S1만1이다. 이 가운데1건은 이미 작성한 로직을 뒤에 통합한 변화다. 그 유형을 양성에서 빼면1/슬롯4이며, 선행동일인착수PR을 빼는 감도는1/슬롯3이다. 둘은 분모가 다르다. 엄격사슬0·직접노동0관측·절감량미확인은 유지한다. 판정을 뒤집을 최소자료는19e첫부모diff/작성자/부모생성기록의 불일치, 또는 실제링크기여와작업시간을직접연결하는새기록이다. 이 추가감사도외부독립인간판독이아니다.
