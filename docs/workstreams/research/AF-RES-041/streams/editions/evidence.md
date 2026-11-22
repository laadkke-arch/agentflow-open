# AF-RES-041 B03 · 원전측 판본 조사와 반례

작성: editions 보조세션, 2026-11-22. 동일 모델의 분담 조사이며 독립 인간 검토가 아니다. 고정 기준은 root SCOPE v1이다. 직접 열람시각과 산입은 `sources.jsonl`, 원래 묶음②와 그 뒤 추가관측은 `baseline.md`에 보존했다.

## 판본 추적의 결론

**정확 원전의 이름은 좁아졌지만, HWN이 실제 본 악보의 물리판·쇄·쪽은 미확인이다.** Bärenreiter의 Schubert판은 공식서문과 기관목록을 이어 BA5635/NSA BA5527, Dürr1988 계열로 좁힐 수 있다. Hofmeister의 Müller판은 op64의 FH6064와 FH6065가 구체적인 후보지만, 1.0.1 주석의 일반제목만으로 권·판을 고를 수 없다. 이 결과는 저자가 그 출판물을 본보기로 명명했다는 수신측 사실을 약화하지 않는다. 정확한 판면에서 어떤 형상변수를 가져왔는지에 대한 별도 공백을 남긴다.

| 직접 읽은 원문 | 닫힌 사실 | 아직 닫히지 않은 접점 |
| --- | --- | --- |
| [Bärenreiter 공식 BA5635서문](https://www.barenreiter.co.uk/prefaces/9790006493296_Innenansicht.pdf), title/printedII–III, ED001 | Dürr;©1988;3쇄2008;ISMN M-006-49329-6; NSA IV/14b BA5527에서 가져온Urtext | preview에 음악쪽 없음.1997당시저자본과2008쇄 동일판면 여부 |
| [NSA공식 발행표](https://schubert-ausgabe.de/en/edition/classification-and-status-of-edition/?detail=106), IV14a+b, ED002; [ÖAW 작품기록](https://schubert-digital.acdh-dev.oeaw.ac.at/W-01032.html), Werkdaten/Literatur, ED003 | BA5527,Dürr1988;Auf dem Strom의 전집쪽196–218는14b | 별책BA5635와전집BA5527 중 실제 본보기 선택, 특정sharp/natural쪽 |
| [NII CiNii NCID BA27399877](https://ci.nii.ac.jp/ncid/BA27399877?l=ja), title/extent/holdings, ED004 | 같은제목,Dürr,Bärenreiter c1988;score24pp+parts2×4pp;기관소장5곳 | 레코드에BA번호없음;소장이저자열람을뜻하지않음 |
| [Hofmeister6064 공식샘플](https://www.hofmeister-musikverlag.com/wp-content/uploads/2023/07/FH_6064_NS.png), 첫연습곡1/바닥FH6064, ED007; [6065공식샘플](https://www.hofmeister-musikverlag.com/wp-content/uploads/2023/07/FH_6065_NS.png), I/편집크레딧/바닥, ED008 | 전자는22Etüden für Waldhorn,후자는12Etüden für Ventilhorn·Neubearbeitet von A.Frehse;두이미지에음악본문과flat이있음 | 인쇄연도·원판/재판관계·정확본보기글리프·double-sharp쪽.두권을한이미지처럼합치면안됨 |
| [BA5635연결 악보발췌](https://cdn.nimq.de/data/file/mgsloib/000/027/076/0000270762.pdf), 단일쪽마디127–135, ED020; [연결판매자기록](https://www.mueller-schade.com/Auf-dem-Strom-D-943-op-posth-119-Gesang-Schubert-Franz-BA5635-237262.html), ED021 | voice m128 sharp,piano m129 naturals,horn m131 flat,m132 natural/sharp를직접볼수있음 | 발췌내부에판번호·쪽번호·colophon없음.상품연결은BA5635이나정확원판면귀속불명 |

### raster 관측과 역사 스캔 판정의 경계

ED020 파일은 `pdftotext`에 텍스트가 없고 `pdfimages -list`에 gray8bit JPEG 이미지 하나(940×1226, object7,72ppi)가 보인다. PDF container metadata의 생성일은2015-03-24이며 original printing date가 아니다. 따라서 **지금 받은 파일이 raster 복제라는 관측**은 참이다. 그러나 인쇄본을 스캔했는지, 후대 재조판을 raster로 내보냈는지, 어느 쇄의 판면인지까지 이 속성으로 판정할 수 없다. 미세한 기울어짐·번짐이 보여도 출처를 대신하지 않는다. 원본이미지는 재게시하지 않고 URL·마디·해시만 남긴다.

IMSLP에는 [Schubert 후보1014719](https://imslp.org/wiki/Auf_dem_Strom,_D.943_(Schubert,_Franz))가BA5527/1988/pp196–218로 올라와 있지만 목록은14a라고 표시한다. 기관은14b라고 한다. 파일 다운로드는JSredirect 및 human-verification에 막혀본문을읽지못했다. 같은페이지의2008/2013/2015 parts는명시적으로새typeset이다. 해당재조판은예전Bärenreiter글리프를입증하는대체재에서제외했다. [Müller op64 후보목록](https://imslp.org/wiki/34_Studies_for_Horn,_Op.64_(M%C3%BCller,_Bernhard_Eduard))도6064/Merseburger C.M.1168와6065/plate10822 관계를제안하지만원인쇄면검증전에는목록후보로만둔다.

## 수신 소스와 병렬로 사용할 수 있는 제한된 비교

원전측은ED020의sharp/natural 기본구조와ED007/008의flat 존재를확인했다. 수신측B03-L011/012는0.1.22→0.1.23에서같은flat의본보기주석을Schubert에서Müller로옮기면서폭·crook두께·outline방식을바꾼다. 이두관측은**같은기호의구현변경**을보강한다. 원전의어느flat이그폭/두께값을유도했는지는미확인이다. 유사한두줄기/가로획/flat배모양은널리공유되므로모양만으로직접복제의증거라부를수없다.

수신측의Wanske sharp규칙과horizontalbeamend를따르지않는주석은선택적모방을직접보여준다. Wanske1988 원책은기관레코드경로가거부/시간초과였으며관련쪽을읽지못했다. 따라서"Wanske가실제로그특징을말하지않았다"는진술은현재원전직접확인이아닌HWN진술이다. Ross1987도같은이유로본문미확인이다. 해당차이는`mechanisms.csv`에변경값/보존값/실패조건으로분리했다.

## 결론을 틀리게 만드는 경우를 찾은 경로

**1. 같은 출판사도 시기·판에 따라 다른 표기규칙을 가질 수 있다.** ED001 printedIII는편집자가추가한principal-noteaccidental을smallprint로구별한다. [NSA7판편집지침](https://schubert-ausgabe.de/download/nga_editionsrichtlinien_7-_fassung_final.pdf)2022 p14 IV.3은같은범주의추가기호를fullsize squarebrackets로표시한다. p17IV.4.g에는일부accidental의현대표기정규화와silentaddition조건도있다. 두원문의규칙차이는직접관측이다. 언제왜바뀌었는지와Feta인과는미확인이다. 이반례는"Bärenreiter모양은시대와판에무관한하나의규칙"이라는추론을막는다.

**2. 실무 지침도 문맥에 따라 기하학적 일관성을 포기한다.** [Gould Behind Bars 공식샘플](https://faber-product-media.s3.amazonaws.com/40c555eb-aa0f-4e02-a7a1-0ec0223f98e4) pp19/315는beam의줄기길이·각도·오선간격조건을제시하고,수평beam이오선과겹치면줄기길이가달라도오선사이로옮기게한다. [저자서문](https://api.pageplace.de/preview/DT0400.9780571590032_A27330093/preview-9780571590032_A27330093.pdf)xi–xv는수행조건과문맥별판단을강조한다. 이것은2011원저작이므로1997Feta의영감으로분류하지않는다. 글리프의선택적모방과layout조건을비교할수있지만두조작을같은결정으로합치지않는다.

**3. 동일작품의서지조합만으로도 잘못된 판을 만들 수 있다.** 현재BA5635의24쪽별책,BA5527의전집196–218쪽,IMSLP의14a표기,새typesetparts를합치면실제로없는"정확한원전"이생긴다. Müller의22곡/12곡과Frehse개정표시도권별로보존해야한다. 이반례는당시가용성과저자실제열람을별개로기록할필요를보여준다.

## 다음 최소 조사

- Schubert: BA5635의1997이전개체와BA5527IV/14b pp196–218의title/colophon·실제판면을정상기관접근으로대조한다. 이어HWN소장/열람본을특정하는당대기록이있어야exact_donor를참으로바꿀수있다. 현재1쪽발췌는마디127–135로재발견가능하다.
- Müller: HofmeisterFH6064/6065의1997이전인쇄개체에서Merseburger C.M.1168 또는plate10822관계를확인하고flat/double-sharp가있는쪽을촬영/기술한다. 정확기호의serif/줄기상단굵기/배곡선을0.1.22/23소스변수와대조한다.
- Wanske/Ross: WanskeISBN3-7957-2886-X 및RossHansenHouse1987판의title/edition과accidental규칙쪽을확인한다. 저자의"언급없음"을검증하려면한쪽예시가아닌해당장·색인범위도확인해야한다.

## 자체 점검

Q1: ED001/003/004서지와ED020실제발췌를별도표시했다. Q2:1988발행·2008쇄·2015PDF·2026접근을분리했다. Q3:저자연결은수신측증거이며원전측서지로대신하지않았다. Q4:보이는기호와소스정의의기본대응만말하고정량모양일치를주장하지않았다. Q5:이번자료는역사LilyPond실행/출력이아니다. Q6:현대편집규칙불일치·문맥조건·서지혼합반례를직접찾았다. Q7:exact_donor미확인때문에엄격인과완결로올리지않았다.

2026-11-22T20:21:18Z 재검산: 원장26행,산입6저작(음악4+기관2),같은저작의다른파일/미러/실패는중복산입하지않음. root MPA와합산할경우음악5이며목표4를넘는것일뿐분모를임의이동한것이아니다. 모든원본PDF/PNG는임시cache로두고커밋대상에서제외한다.

### 산입 최종 정정

위 20:21:18Z 중간 계산의6저작은 ED020을 포함한 당시 값이다. 이후 root가 미러·재게시물 배제를 보수 적용하여 ED020을 false로 정했다. 실제 raster 판독은 유지하고 출처 최소수에만 쓰지 않는다. **현재 산입은5저작(음악3+기관2)**이며 root MPA1993을 더하면 음악4건이다. 원장에 counted_initial과 정정 이유를 보존했다.
