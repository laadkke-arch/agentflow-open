# AF-RES-045 자체 재판독

## 검토 판과 판독의 독립성

입력의 고정판은 예측 봉인 `0d998cb3503e8a7f0faf2bf2f8e62dd046a662b1`이다. root는 원문을 다시 열고, 세 작업자는 별도 문맥에서 공간·시간/방법·Audacity 판독을 교차 확인했다. 같은 모델을 사용한 병렬·별도 문맥 검토이며 **외부 독립 인간 판독이나 독립 실험은 아니다**. 모델에 과거 공개 자료의 사전학습 노출이 없었다는 보장도 하지 않는다.

최종 원격 RESULT/수용 원장의 재열람 SHA·시각·해시는 [result-verification.json](evidence/result-verification.json)과 마지막 HANDOFF에 남긴다. 이 파일 자체가 예상한 성공을 검증됐다고 선언하지 않는다. 요구·예측·후속의 구조 검사는 [verification.json](evidence/verification.json), 필수 표·말미·원문 필드 검사는 [deliverable-validation.json](evidence/deliverable-validation.json)에서 실제 결과를 확인한다.

## Q1 — 결말을 보기 전 요구가 고정됐는가

**답:** 현재 첫 본문을 대상으로6요구와 첫30×2목록을 고정했고, 결과를 읽기 전에 원격 예측 커밋을 만들었다. 정확한 생성시점의 불변 본문은0/6이며, 현재 제목을 과거 생성일로 정렬한 표본이다. AUD02의 사후 체크리스트 노출과 AUD01의 교차사례 후발 API 노출을 제거하지 않고 감도로 남겼다.

**다시 연 근거:** root가2026-11-22T22:47:58.041Z에 [Audacity511 timeline](https://api.github.com/repos/audacity/audacity/issues/511/timeline?per_page=100)의2022-03-22T18:00:37Z rename을 확인했다. 원제목에는selection이 없다. 같은 시각 [Matplotlib13600 댓글470135635](https://github.com/matplotlib/matplotlib/issues/13600#issuecomment-470135635)을 다시 읽어 제목만 제출한 뒤 본문을 완성했다는 설명을 확인했다. 재방문은 sources의SELF-Q1-TITLE/SELF-Q1-BODY에 있으며 추가 산입하지 않는다.

**반대 관측·탐색:** [frame.csv](frame.csv)의Matplotlib13311 탈락과13650 정원 후 우연 노출, [amendments.md](amendments.md)의E01–E03을 확인했다. 현재 제목에selection이 있다는 이유로 역사적 원제목도 같다고 추론하면511에서 틀린다. GitHub의updated_at만으로 본문 변경일을 단정하지 않았다.

**판정을 바꿀 최소 자료:** 선정 이슈의 해결 조언 전 본문·제목 snapshot이나 편집 이력 한 건부터 복원. 현재 사용한 요구가 그 판과 같은지 대조해야 완전 가림·역사적 검색 표본 주장 범위를 넓힐 수 있다. 0인 최초판 분모는 해당 없음으로 유지한다.

## Q2 — 같은 목적의 A/B와 두 입력이 검사 가능하게 적혔는가

**답:** 6요구마다 두 조작·정상·경계 입력을 적었고 작성자 조건과 연구자 추가를 분리했다. 그러나 A/B 모두가 당시 실제 수신 API에서 동작한다고 검증한 것은 아니다. AUD01의Nyquist속성 존재는pipe전달을 증명하지 않으며, AUD02의임의RGB는당시palette API를 넘고, AUD03은localundef때문에 실제 적용이 막힌다.

**다시 연 근거:** root가22:40:49.166Z에 [Matplotlib3.0.0 API Changes](https://matplotlib.org/3.0.0/api/api_changes.html)의L90–110(set_in_layout), L171–173(get_position의apply_aspect)을 다시 읽었다. root는22:30:53.903Z에 [Audacity2.4.2 NoiseReduction L75–77](https://github.com/audacity/audacity/blob/16d52f63a4183bba77ef7305d14622958dc0d1d5/src/effects/NoiseReduction.cpp#L75-L77)도 확인했다. source IDs RMO-API30-REVISIT/REV-AUD-NR242.

**반대 관측·탐색:** [requests.csv](requests.csv)의researcher_added/choice_feasibility와 [재현 통제](evidence/reproduction/REPRODUCE.md)를 대조했다. M01의B축척0.90·중앙배치, M02seed45045·Agg·글꼴 고정은 봉인 후 재현 도구의 추가 매개변수다. 이 값들을 사전 봉인 값으로 소급하지 않았다. 최초 저장 전에bbox를 측정하려고draw/get_position을 부르면 상태를 바꿀 수 있어 계측은 passive필드를 사용하도록 준비했다.

**판정을 바꿀 최소 자료:** 각 고정판에서 두 조작이 실제로 적용되는 실행 경로와 입력·환경 로그. AUD03은 먼저 활성 spectral-selection API를 확인해야 하며, undef제거를 과거 기능의 재현으로 세면 안 된다.

## Q3 — 두 제공 분야의 정확한 규칙과 그 한계가 있는가

**답:** 고유 제공 저작9개(공간4·영화/방송4·접근성1)를 읽었다. 시간 경계 원전 자체는Avid·Premiere·Netflix의3개다. 같은 수신 프로그램의 매뉴얼은 제공 원전으로 세지 않았다. 지도/시각화와 영상/음향은 인접 분야인 부분을 그대로 표시했다. 제공 규칙에서 exactAPI나5bin kernel을 유도했다고 주장하지 않는다.

**다시 연 근거:** root가22:47:58 이후 [W3C Media Fragments2012](https://www.w3.org/TR/2012/REC-media-frags-20120925/) §6.1.1 L343,§6.2.2 L385–391을 다시 읽었다(SELF-Q3-W3C의정확UTC). a=b는오류이며원문은SHOULD ignore라고 한다. 모든player의실행보장이나유효한editor빈구간으로바꾸지않는다. 별도 방법 판독자는 [WCAG2.1 §1.4.11](https://www.w3.org/TR/2018/REC-WCAG21-20180605/#non-text-contrast)을 재열람해 essential예외와 대비비1:1을 확인했다(WD01-METHOD-REVISIT).

**반대 관측·탐색:** [공간 원문·실패 탐색](evidence/spatial-donor-sources.jsonl)과 [시간 원문·실패 탐색](evidence/temporal-donor-sources.jsonl)을 확인했다. 같은매뉴얼의다른절·실패PDF·현재도움말·검색요약을새저작으로늘리지않았다. Netflix확인본문의2025/2026수정판, Apple의날짜불명판은현대적용진단이다. USGS/ArcMap/CS6의정확한최초공개일미확인을보존했다.

**판정을 바꿀 최소 자료:** 필요한 제공 절이 수신 결정 전에 공개됐음을 보여주는 고정판/배포 기록과, 같은 조작·입력·불변조건으로 대응할 수 있다는 명세. 현대판과모양의유사성만으로과거영감이나역사적가용성을채우지않는다.

## Q4 — 결과 전에12행이 봉인됐으며 서로 다른 예측인가

**답:** 6×2=12행을 원격22:19:23Z에 봉인했고 원격prediction본문을22:19:27Z에 다시 읽었다. 최초 후속 열람22:20:00.421Z보다 앞선다. 봉인 SCOPE/frame/requests/predictions의4개SHA-256이 일치한다. 넓은 분류3/2/1을 보존하지만 M01의P2는 이미 내부 기하 scaling실패를 예상하므로 반대 성공 예측으로 바꾸지 않는다.

**다시 연 근거:** [고정 predictions.csv](https://github.com/laadkke-arch/agentflow-open/blob/0d998cb3503e8a7f0faf2bf2f8e62dd046a662b1/docs/workstreams/research/AF-RES-045/predictions.csv)의M01-P1/P2와AUD03-P1/P2, [봉인 파일 해시](evidence/prediction-seal.json), [방법 재판독](evidence/method-review.json)의m01/분류 항목. root와별도문맥판독자모두 M01의다른조작과반대예측을구분했다.

**반대 관측·탐색:** AUD03에서평균공간·안쪽feather·Fs/N을바꾸면수치또는구별여부가변한다. [verification.json](evidence/verification.json)의arithmetic은−2.4dB/−1.9330457dB/0dB를분리한다. 사후 계산을 실제NR시험으로 부르지 않는다.

**판정을 바꿀 최소 자료:** 서로 반대되는 관측을 같은 입력에서 예측하도록 추가 원리를 새로 명세할 수는 있으나, 이는 새 실험이다. 기존12행을 결과에 맞춰 다시 봉인한 것으로 쓰지 않는다. 원격순서의반증은더이른후속열람기록또는다른원격본문이면가능하다.

원래 SCOPE의 같은입력후속증거 문구에는 두입력·A/B완결비교가 명시되지 않았다. 최종 방법검토의 반론을 수용해 완결비교0을 사후강화로 표시하고, 원문을관대하게읽은 M01분모1·유일지지0·판정불가1과 입력동일성까지완화한M01+M03분모2·유일지지0·판정불가2를 RESULT·outcomes·수용원장에추가했다. 원래규칙과초기집계를삭제하지않았다.

## Q5 — 후속 결정·명세·코드·시험·실행을 분리했는가

**답:** 9개의별도후속저작을확인했다. 원래요구이슈의댓글은근거로연결하되새저작으로다시세지않았다.6사례중정성적원작성자수락은공간3사례에서보이지만, 봉인정상·경계입력모두에대한동일조건공개시험은0이다. 실제선택이제3안이면A/B중하나로강제하지않았다.

**다시 연 근거:** root가22:30:53.904Z에 [M03고정 test_collapsed L313–327](https://github.com/matplotlib/matplotlib/blob/f9d8cd7e0c9a4e94962fc925c57fb678ba252f87/lib/matplotlib/tests/test_tightlayout.py#L313-L327)을읽어colorbar없는다른입력임을확인했다. [M02댓글470121184](https://github.com/matplotlib/matplotlib/issues/13522#issuecomment-470121184)은정성적수락일뿐이다. root는22:47:58.041Z에 [GetInfo 고정코드 L634–645](https://github.com/audacity/audacity/blob/0ffa73b9f44acc339e12a350edadd96590dc4b17/src/commands/GetInfoCommand.cpp#L634-L645)를다시읽었다.

**반대 관측·탐색:** [2713종료댓글](https://github.com/audacity/audacity/issues/2713#issuecomment-1150354103)은완료가아닌유보다. [PR13603실행보고](https://github.com/matplotlib/matplotlib/pull/13603#issuecomment-470368884)는crash시험의보고다. [407기여자그림](https://github.com/audacity/audacity/issues/407#issuecomment-2076865041)은다른값이며원작성자재시험이아니다. PR파일목록에서시험을못찾았다는것을저장소전체시험부재로확대하지않았다.

**판정을 바꿀 최소 자료:** 원래A/B각각과봉인두입력, fixedbinary/code판, 예상·실제출력을같이보여주는공개자료. 현재완결비교분모0의비율은해당없음이며, 이를실패율이나성공률0%로표현하지않는다.

## Q6 — 추천을 뒤집는 반례와 다른 관점을 확인했는가

**답:** 공간가독성과정확위치, frame/sample/주파수단위, 원리를실행하지못하는수신API, 양쪽후보가같은수락조작을가리킨경우를검토했다. 다만양쪽후보가봉인두입력의출력을실제로맞혔다는완결비교사례는없다. M02의공유B수락은그보다약한근거다.

**다시 연 근거:** root가22:30:53.904Z에 [Cartopy1370 철회댓글569853924](https://github.com/SciTools/cartopy/pull/1370#issuecomment-569853924)을다시읽었다. 전역초기화는자동범위를잃는다. 공간판독자는 [3.0.2 colorbar L1001–1003](https://github.com/matplotlib/matplotlib/blob/8858a0d1bdd149a0897789e8503ac586be14676d/lib/matplotlib/colorbar.py#L1001-L1003)을22:46:14.736735Z, [2.2.2 _config_axes L430–440·_uniform_y L779–785·_mesh L843–861](https://github.com/matplotlib/matplotlib/blob/b471ee21cbe0d0fdd9cf5142d0a4be01517f4e68/lib/matplotlib/colorbar.py)을22:47:37.713097Z다시열었다(SPREV기록).

**반대 관측·탐색:** 3.0.2는x와y를모두환산한다. 따라서목표를실제y값.5로바꿨을때B의y고정논리가맞을수있어도기본(.5,.5)전체를권할수는없다. 가로중앙은별도transform이필요하다. [QGISdisplacement](https://docs.qgis.org/2.18/en/docs/user_manual/working_with_vector/vector_properties.html)L324–326, [Cartopy1956비용비교](https://github.com/SciTools/cartopy/pull/1956), [Audacity5653색보존회귀](https://github.com/audacity/audacity/pull/5653)를독립비교로유지했다. 선택·목적·판을바꾼진단을원실험적중으로세지않았다.

**판정을 바꿀 최소 자료:** 목적우선순위와비용예산을정한동일입력비교, actualaxislimits, 활성API와정해진noiseprofile/window/overlap. 단위변경때index86을같은Hz로취급하지않고새bin경계를계산해야한다.

## Q7 — 설계자에게 어느 수준의 링크를 반환할 수 있는가

**답:** [cards.md](cards.md)6카드로조건부조작진단, 구현찾기, 요구충돌/변수대응실패를구분했다. 완전한원리→조작→두판별입력→동일입력후속사슬은0/6이다. 원래요구에있는목표, 기존API, 연구자추가, 실제작성자수락, donor채택을따로적었다. 제공원전의채택·역사적영감·회수율·수정노동절감은미확인이다.

**다시 연 근거:** [M03조언·수락](https://github.com/matplotlib/matplotlib/issues/13600#issuecomment-470153183)을root22:47:58.041Z에재열람했고, [GetInfo 제3API](https://github.com/audacity/audacity/blob/0ffa73b9f44acc339e12a350edadd96590dc4b17/src/commands/GetInfoCommand.cpp#L634-L645)도같은시각확인했다. 이들은maintainerAPI조언과구현을뒷받침하며donor원전채택을뒷받침하지않는다.

**반대 관측·탐색:** M02의동률, M03의이미명시된중앙목표, AUD03의원래Audition참조와비활성API가추천의새로움·타분야성주장을제한한다. 결과사전노출AUD02를제외한5자리, 추가로AUD01을제외한4자리도완결비교분모는0이다.

**판정을 바꿀 최소 자료:** 실제설계자가어느원전의어느규칙을어떤조작으로옮겼는지와그선택전후자료, 같은입력의경쟁예측시험. 노동절감을주장하려면설계수정시간·비교조건이별도로필요하다.

## 집계·정정·남은 미충족

- 원문배당은소스원장으로재계산한다. 최초요구6·제공9·후속9·비교6=30고유저작이며, source기록수에는실패·검색·재방문이포함된다. 후속9는동일입력시험9가아니다.
- 원래6자리·12예측을유지한다. M02/AUD01의동률은판별성공에서제외하며, AUD02미결정·AUD03활성API오류를감추지않는다.
- 봉인뒤수정한메타데이터는원래필드를함께남긴다. final_url의literal“same as url”정규화, 실패후성공URL의중복연결, M03의y/x구분은[amendments.md](amendments.md)에연결한다. 원래source본문과판정규칙은봉인SHA에서도열수있다.
- 역사프로그램을이환경에서실행하지않았다. 현재Matplotlib를과거판대신쓰지않았고, 재현코드는정적문법·논리검토만했다. 실제계산은표준라이브러리의산술검산과구조검사뿐이다.
- 최종수용은“부분인계”다. 수량·문서·봉인순서의충족과, 불변최초판·같은입력시험·유일지지·당대활성API조건의미충족을[acceptance-evidence.json](evidence/acceptance-evidence.json)에항목별기록한다.

## 별도 문맥 검토와 root 반영

[방법 검토](evidence/final-method-review.md), [공간 검토](evidence/final-spatial-review.md), [Audacity 검토](evidence/final-audacity-review.md)를받았다. 공간검토의M03 x/y조건보정을RESULT·카드에반영했으며예측CSV는그대로다. 원문필드정규화도산입수나판정을바꾸지않았다. 신규원문재방문은sources에추가하되고유원문수에는추가하지않았다. 정확한최종파일구조와검사출력은최종커밋에서다시확인한다.
