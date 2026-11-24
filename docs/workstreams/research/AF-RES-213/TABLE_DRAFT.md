# 3차 핵심 비교 표 초안

|저널·스타일|정확 파일·판|자식 자체의 내용|실제 부모·로캘 주소|미확인|
|---|---|---|---|---|
|Nature Biotechnology / Nanotechnology|A01/A02 at f123868a546e6e7cec10e808ae04ef0e52bf2210|info only, default en-GB; 각각 id/self|A03 nature.csl; A06 en-GB|설치·실행·저널 승인|
|Nature|A03|8 macros, 2 layouts|A06|실행|
|APA|A04|99 macros, 2 layouts, 10 locale blocks|A05–A07, embedded overrides|실행|

|목적·소비자|이미 있는 자산|추가 필수·조건부|근거 구간|실패 반례|
|---|---|---|---|---|
|목록 Zotero|bundled parent & APA|alias only when absent|C01,C03,X01|unique-only hides alias|
|목록 Pandoc|CLI, Chicago default|explicit file|C07,C08,C14|not a GUI list|
|편집 양쪽|A03/A04|independent full copy or controlled shared parent|A01–A04,B01,B02,C02,C08|alias body is invalid|
|오프라인 Zotero|bundle locales|missing styles only; FR may need locale override|C03,C04,X01–02|fixed locale disables UI|
|오프라인 Pandoc|embed locale data|local style + parent if alias + refs|C08–C13,X06–08|wrong basename / remote fallback|

|원요구|첫 링크|가능한 독립 사본·공유 수정의 파급|실제 후속|미확인|
|---|---|---|---|---|
|R01–R06|requests.csv|scope to actual purpose|D04/D07 merged; other reports/replies separated|current exact journal pair report not found|

12 positions / 24 consumer rows in resolutions.csv. Source-backed expectations, not render runs. R02 historical alias claim requires current XML comparison in next phase.
