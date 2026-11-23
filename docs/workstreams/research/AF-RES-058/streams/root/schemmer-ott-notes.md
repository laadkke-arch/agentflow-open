# Root 직접 판독: 사전 답·정답 라벨·판 대응

## Schemmer et al. 2023, DOI10.1145/3581641.3584066

root는 prior-knowledge seed로 이 논문을 찾았으며 primary B 방법선정과 독립이다. 선정되면 같은 저작으로 합친다. 확인판은 [KIT 저자판](https://publikationen.bibliothek.kit.edu/1000158077/150613452), 표지 `arXiv:2302.02187v3 13 Apr2023`, SHA256 `3238886354f687e7893898ff8d3f6fcdc93f0f1e5ab3f09b116a1e2546dab161`. DOI publisher 검색결과의 editorial note는2023-04-16 corrected version을 알리지만, 직접ACM HTML/PDF는403, UBC 검색된 PDF는404였다. correctedVoR와 읽은v3의 일치는 미확인. correction note를 새 독립저작으로 세지 않는다.

- §3.2/식1–3, PDF6–7: RAIR는 원래 사람오답·AI정답인 시행에서 정답으로 바꾼 비율, RSR는 원래 사람정답·AI오답인 시행에서 정답을 지킨 비율. 전체 정권고수락/전체 오권고수락과 분모가 다르다. 처음부터 같은 답인 확인 사례를 제외한다. 사전답이 없는 연구에서 이 척도를 복구하지 않는다.
- §5, PDF10–13: 호텔리뷰 진위 이진분류, 사람간 무작위2조건. AI권고와 LIME단어강조 유무. 200모집, 설명군1명 제외, 분석100대99.16과제,32리뷰집에서TP/FP/TN/FN각4를 선택하고각cell긍정2/부정2; 학습모델86%와 시행집50%는 다른 수치. 사람의 처음답→권고/강조→수정답. 훈련2개 feedback있음, 본과제 feedback없음. 동일개별항목의 조건별배정표/스크립트는 확보하지 못함(E2 또는EU, 같은모델만으로E1 아님).
- Fig5(PDF11) 실제 화면 시각확인: 왼쪽첫답 plain review, 오른쪽 feature condition에 색/강도별단어강조와AI권고, 아래 confidence평정. 저자는 예시참값fake라고명시. 이는 step1/2 쌍이지 동일항목의 control/feature 실제 렌더쌍을 직접 확보했다는 뜻은 아니다. 원문링크열람 조작 아님.
- Table2(PDF13) 및Table3/Fig6(PDF14) 시각확인: 분석N100/99. RAIR29.59%/38.87%, RSR71.87%/69.45%, AI-assisted53.94%/56.30%, initial55.50%/53.85%. 전원정오층수락의 원개수 없음. 숫자에서정수역산금지. 저자 단위가 participant rate이므로 pooled trial수락률로 바꾸지 않음.
- §6.3/§7: 'no missing data'는 SEM 전처리 맥락의 저자 진술이며 원배정·최종응답 전체의 결측0을 검증한 것이 아니다. 제외1명도 취소하지 않는다. 구pretest[63]의RSR감소가larger study에서는유의하지않았다고명시; 같은연구팀/관련코호트가능성을확인해야독립복제로셀수있음. sequential설계자체가anchoring/인지참여를바꿀수있음을저자가한계로명시.
- 후속 동료 검토(2026-11-23): Table3 confidence change Control0.19/Feature0.06과 §6.1 설명조건 증가라는 서술의 방향이 일치하지 않는다. 정정된 VoR 전문 미확인 상태에서 자신감 증가를 결과 주장에 쓰지 않는다. adjacent의 별도 원문/표 시각 판독은 streams/adjacent/self-review.md에 기록한다.

## 정답 원천: Ott2011와Ott2013

[Ott2011](https://aclanthology.org/P11-1032.pdf) §3.1–3.3, printed311–313: 허위리뷰는crowdworker가가상후기를쓰도록배정한출처라라벨을안다. truthful쪽은TripAdvisor의인기호텔후기를선별하고첫작성자등을제외한것이며개별실제투숙을검증한원장이아니다. 인간3명의사후다수결은기준라벨이아니라비교용성능이다.

[Ott2013](https://aclanthology.org/N13-1053.pdf) §2.1–2.2, printed498: 부정리뷰400개를새로수집하고6사이트의1–2star후기와대조. 저자는웹에서수집한truthful리뷰가gold-standard truth라고할수없음을명시한다. 따라서후속실험의권고정오는**원코퍼스라벨상정오**로서해석하며모든실제리뷰진위의완전한검증이라고하지않는다. 기존2011positive코퍼스를재사용하는부분과새negative수집을구분한다.

공식ACL의[P11-1032 dataset](https://aclanthology.org/attachments/P11-1032.Datasets.zip)은확장자는zip이나실제gzip-tar였다. zip parser실패를접근불가로끝내지않고file-signature와tarfile로읽었다. `op_spam_v3/README`와파일구조확인: 400truthful+400deceptive, 실제파일2000(각review의unigram/bigram,허위만raw추가). 총2000을2000독립리뷰로세지않는다. 개인정보보호를위해truthful원문은배포하지않는다고명시. 이2011positive-only판이후속연구의positive+negative판과동일하다고주장하지않는다. 입력해시/표현별개수는 `ott-schema-audit.json`.

## 제품으로 옮길 때

동일권고의최종수락은사전답이없어도관측할수있다. 그러나권고때문에바꾼선택을주장하려면사전답또는그에상응하는배정설계가필요하다. 진위코퍼스의라벨처럼참값도생성과정에의존한다. 부품적합성에는버전·환경·필수제약을명시한참값또는검증절차가별도로필요하다. 이문헌은설계자의총노동시간/설치/재작업효과를측정하지않는다.
