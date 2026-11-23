# A층 재현과 실제 실행 기록

## 고정 입력

- A01 저자 package: `bcbi-edu/p_eickhoff_transparent-ir@4a308f735066b2741d2931cd0e5dc0d372f06429`.
- [ZIP 원주소](https://codeload.github.com/bcbi-edu/p_eickhoff_transparent-ir/zip/4a308f735066b2741d2931cd0e5dc0d372f06429), SHA256 `c4a91787e7858d8f65fafd2b3dcd7a68978cd1c74d657d159ac119bf6b749db0`.
- [Cranfield 원판](https://ir.dcs.gla.ac.uk/resources/test_collections/cran/cran.tar.gz), SHA256 `8c48a8412e4a7e6e0dd5af99c959f8d75fdf88135602adc1a56aa22770652d64`.
- A01 paper preprint SHA256 `582eed2a9689d06a359f84a6da0532a906cf3740c6c06c8a4b0787696c855361`.
- Brown 저자보고서 SHA256 `3d3e3678f13212ea33517ce717b8a31ddc354d0bf374fa90d5794c4b2d9d4e95`.
- A02 authorposter SHA256 `594e2f4142c5806c207fb4076ad6f7266603ca7babf44878486fb6a93516db77`.

모든 취득시각/HTTP상태/최종URL은 `fetch-receipts.jsonl`에 있다. 취득은 열람과 다르며 실제로 읽은 절은 `sources.jsonl`을 따른다. 원저작/익명원행은 ignored `_cache/`에만 남겼다. 공개산출물은 schema·합계·제한·재현코드뿐이다.

## 실제 실행한 집계 명령

실행주체는 software_ir 보조조사자, cloud workspace의 Python이다. 두 명령 모두 종료코드0이었다. 원래 저자 실험서버·JavaScript앱·외부 API는 실행하지 않았고, 새사람실험도 하지 않았다. 아래스크립트는 내려받은 공개파일만 읽는다. 실행UTC는 결과JSON의 `observed_utc`에 있다.

저장소 최상위에서:

```bash
python -B docs/workstreams/research/AF-RES-058/streams/software/audit_sigir2020.py --package-root docs/workstreams/research/AF-RES-058/streams/software/_cache/repo2020/p_eickhoff_transparent-ir-4a308f735066b2741d2931cd0e5dc0d372f06429 --output docs/workstreams/research/AF-RES-058/streams/software/package-audit.json

python -B docs/workstreams/research/AF-RES-058/streams/software/audit_cranfield.py --archive docs/workstreams/research/AF-RES-058/streams/software/_cache/cranfield.tar.gz --package-root docs/workstreams/research/AF-RES-058/streams/software/_cache/repo2020/p_eickhoff_transparent-ir-4a308f735066b2741d2931cd0e5dc0d372f06429 --output docs/workstreams/research/AF-RES-058/streams/software/cranfield-audit.json
```

캐시가 없는 환경에서는 고정ZIP을 내려받아 `_cache/repo2020/`에 풀고, tar.gz는 풀지않고 위경로에 둔다. `fetch_public.py LABEL URL EXT`는 공개파일 취득과 해시기록만 수행한다. 위저장경로를 사용하며 원저작이나 원행을 git add하지 않는다.

## 자료 구조와 연결 규칙

`client/data/batch_1..5/*.json`은 확장자가json이지만 실제JSON Lines다. `json.loads(entire_file)`로 읽으면 Extra data가난다. 실행한 집계는 비어있지않은 각행을 독립JSON으로 해석했다. batch1 CSV는 헤더행이아니라 데이터로시작하며, 동일package의 보조export라 추가시행으로세지않았다.

`id`는 App.js/server.js가 만드는 익명UUID형태다. 이값이 같은batch의 exit응답·quiz·links를 연결한다. 이는 같은사람을 외부에서 식별한 것이아니며, 실제150완료자대응표가없다. `session`은 App.js의정수와 HTMLform의문자열에 모두등장하므로 정수표현인값만 같은정수문자열로 정규화했다. 중복 id/session키는 단일최종행으로 임의선택하지않았다.

단순파일감사 결과는 다음과같다.

- links:81+179+118+129+52=559행, 익명id185종.
- verify:20+162+111+116+50=459행, 익명id165종.
- responses:19+15+13+10+10=67행, 익명id67종.
- 모든67exit id는 같은batch의다른두표와연결된다.
- 단일대응 links–verify id/session키는20+149+99+109+48=425개다. 이는425명의사람이나425개의추천수락시행이아니다.
- 185id중quiz표에없는id20,165quizid중exit표에없는id98이라는 export상결손은 관측된다. 배정·탈락참가자수를뜻하지않는다.
- 조건열, 노출된전체결과/순위목록, 확정 relevance threshold, 권고전 자기답이부재하므로 `outcomes.json`의 정오별분자/분모는 미확인이다.

## 저자 집계표 손검산

[Brown 저자보고서](https://cs.brown.edu/media/filer_public/36/96/36968fbe-c532-4630-a5b9-18c512efb1c7/ramosjerome.pdf) PDFp7의 Table2와 p8의 Table2/Table3를 직접렌더링해 perceived-truth 문항5개범주를 읽었다.

| 조건 | SD,D,N,A,SA 원개수 | 분모 손합 | 긍정응답A+SA |
|---|---|---:|---:|
|TAB/ExplainSearch|2,1,11,28,8|2+1+11+28+8=50|28+8=36|
|TA|0,4,22,20,4|0+4+22+20+4=50|20+4=24|
|T|3,1,13,26,7|3+1+13+26+7=50|26+7=33|

TAB−TA=(36−24)/50=0.24. 이 산식은 **지각된참값**의 이분화주변수다. 권고정오에조건화하지않았으므로 정확한권고수락이나틀린권고거절로 해석하지않는다. 원시표는 `diagnostic-margins.json`에보존했다. 원문그래프백분율을 정수로역산하지않았다.

## 공개원행 채점 검산

batch4/5만 `numCorrect`가있다. 해당166행을 저자server.js의1/4/2/2 answerkey와대조했으며166/166행의저장점수가일치했다. 원행은공개하지않고 score빈도만남겼다.

`29+59+57+19+2=166`

`0×29+1×59+2×57+3×19+4×2=238`

문항기회 `4×166=664`, 통과시행 `19+2=21`. 같은id의반복시행이포함되며, 배정조건을알수없다.166을독립표본수로,238/664를권고수락률로쓰지않는다. 저장score없는293quiz행을 HEAD키로소급채점하지않았다. 당시버전이입증되지않았기때문이다.

## 원래참값 자료 검산

Cranfield1,400문서,225query,1,837qrel행을읽었다. query002는선택실험prompt와문자상대응한다. query2의25qrel은 `2+5+13+4+1=25`다.원등급은1이완전답변이고4가최소관심이다. -1은동봉README에서정의되지않는다.

공개bookmark143제목중142는공백·대소문자만정규화한 corpus제목과유일하게일치하고1은중복제목이다. fuzzy matching이나행정렬대응은하지않았다. 이는가능한문서키연결점검이다. 배포판의본문일치나실제노출모집단은확인하지못했으므로 이를관측된권고수락cross-tab으로변환하지않았다.

## 재현불가능한 칸과 최소추가입력

A01에서필요한것은 원래배포SHA/세조건구현, 익명id조건배정표, 실제노출후보·rank·docID·시각, relevance threshold와참값판,150완료자분석포함표다. 새배정표를만들거나 batch명을조건으로가정해서는안된다. A02는원논문/원자극/사람-과제-조건표/정답키/최종선택및결측이필요하다. 그때도단순클릭과 최종채택을구분해야한다.

## 자체검토 범위

software_ir이PDF원화면, 코드구조, 원행schema, 집계산식을검토했다. `/root/diagnostics`의독립검토는원장·계보·파일접근범위를감사했고 SW-S15 원논문방법대신demo를읽은것을지적했다. 이정정은 `methods-sensitivity.json`과원장에반영했다. 다른검토자가개인별원행을독립재분석했다고주장하지않는다. 본스크립트실행성공은 연구의정오별수락식별성충족과별개다.

