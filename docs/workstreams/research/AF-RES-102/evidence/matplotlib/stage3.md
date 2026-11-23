# Matplotlib 3.6.3 → 3.7.0 판독 결과

## 주 표본과 실제 오류

일반층2개와 변경층2개 모두 같은 논리 목적의 예제가 신판의 정확한 절에 남는다. 각 층은 TP2/FP0/FN0/TN0이며 실제 음성 분모는0이다. 부재층은 봉인한40개 후보에서 해당 자원이 없어진 경우가0이므로2쌍 결원이다. 전체12판 자리 중8자리 판독,4자리 결원을 유지한다. 결원을 실제 음성으로 세거나 보조 표본으로 채우지 않았다.

| 사례 | 실제 판독 | URL 반환에 필요한 조정 |
|---|---|---|
| MP-G1 | 양판 동일한 ImageGrid 실행 소스·첫 그림 목적. PNG바이트는 다르고 픽셀은 같다. | 당시 인용은 고정3.6.3 본문/PNG. 이용은 확인한3.7.0 절. |
| MP-G2 | 양판 동일한 append_axes 실행 소스·오른쪽/위쪽 색상 막대 목적. PNG바이트는 다르고 픽셀은 같다. | 같은 목적이므로3.7.0 정확 절과 필요한 그림만 제공. |
| MP-C1 | HBoxDivider 첫 그림의 같은 높이 목적 유지. 신판은 설명 상자를 본문으로 옮기고 VBoxDivider의 같은 너비 그림을 추가. | 옛 #hboxdivider-demo가 신판 정적 HTML에 없다. 신판 #hboxdivider-and-vboxdivider-demo의 **첫** 그림을 반환. U오예측이 아니라 반환 fragment교정이다. |
| MP-C2 | 제목/본문 구두점으로 소스blob은 바뀌었지만 첫 그림의 inset크기·위치 실행 코드는 같다. | source blob변화만으로 목적교체를 주장하지 않는다. |

주8자리 모두 P=YES/U=YES/G=미확인이다. mainPNG8개와2x변형8개를 받아 형식·크기·SHA256을 읽었고, 고정 발행트리의 Gitblob 지문과도 일치했다. exactsection 내부의 img/srcset을 모두 조사했고 main사례에는 base/picture/source/inlineSVG/script/dataURI 대체표현이0이다. HBox신판은 두 그림을 구분해서 읽었다.

## 정확 절·소스 연결

[최종12행](lineage.csv), [adjudicated audit](audit.json), [목적별 반환](returns.json)에 정확 URL·행·관측 영수증이 있다. `main-audit-raw.json`은 자동 추출 중간물이고 U의 PENDING은 최종판정이 아니다. 최종값은 audit.json/lineage.csv를 따른다.

HBox옛 절은 HTML L1025–1074, 새 절은 L1026–1082다. 옛 img는 L1028, 새 첫 img는 L1055다. 새본문은 같은높이 설명을 먼저 둔 후 VBox의 같은너비 설명을 추가한다. 배포Python은 옛 L15–43과 새 L17–32에서 HBox관계가 이어지며 [저자 변경8ecd60d](https://github.com/matplotlib/matplotlib/commit/8ecd60dc48e8767282656c8633415fda1be8beeb)가 같은파일의 VBox추가를 확인한다. [hbox-author-change.json](hbox-author-change.json).

발행3.6.3의 HTML버전은 v3.6.3-3-g655f616e86, 발행3.7.0은 v3.7.0-3-g235131a6bc다. 공식release태그 SHA와 문서revision을 따로 보존했다. 선택한8판의 **실제 문서revision .py = 배포 Download Python = 공식 gallery_python.zip 내부멤버** SHA256이8/8일치했다. [source-distribution-links.json](source-distribution-links.json). 이 세경로의 일치는 소스/배포 연결이고 실제 생성job증거는 아니다. ZIP은 옛521멤버·1,274,739B, 새522멤버·1,296,753B의 Python예제소스 묶음이며 전체HTML/PNG배포아카이브라고 부르지 않는다.

공통 생성소스 앵커 `sphx-glr-gallery-axes-grid1-demo-axes-hbox-divider-py`도 두 고정판 DOM에 존재한다. 제목에서 생성한 fragment와 별도로 이 관측된 앵커를 사용할 수 있으나, 미래 판에서도 유지된다는 보장은 하지 않는다.

## 반례를 찾은 범위

봉인한 보조20개를 같은hash순서로 모두 조사했다. 외부첫그림17개, JS/dataPNG첫프레임3개다. 각사례의 양쪽본문·소스·첫그림을 읽고 목적을 판단했다. [supplemental-audit.json](supplemental-audit.json).

| 유형 | 범위·결과 | 한계 |
|---|---|---|
| ① 경로는 남지만 정확 절은 안 씀 | 주4개 및 보조외부17개 모두 해당 첫그림경로를 정확 절이 참조. 발견0. | 다른절·다른파일·다른릴리스의잔류를 부정하지 않는다. |
| ② 옛경로는 없고 새이름/내장으로 계속 씀 | 모집40개 중외부28개가모두남음. 부재층0이며 보조20에서도없음. | 원래내장인12개를 외부경로삭제로 세지 않는다. 새 모집이 필요하다. |
| ③ 이름·해시는같고목적변경 | 주·보조첫그림은양판바이트가모두달라 동일경로·동일SHA조건의판별기회0. | 관측가능분모0에서 오류율0을 주장할 수 없다. |
| ④ 바이트는다르고같은절목적유지 | 주4쌍전부. 특히HBox는픽셀도변하지만원래목적을유지. 보조20도목적유지,20바이트변화중2픽셀변화. | byte변화를새생성실행이나목적변화로 해석하지 않는다. |

보조 MP-S10도 제목의띄어쓰기로 #inset-locator-demo2→#inset-locator-demo-2가 바뀐다. 원 zoom/inset목적은 이어진다. 이 보조 결과를 주혼동표에 더하지 않았다. MP-S02 animate_decay와MP-S11 bayes_update는098의기존읽기이므로 새고유자료수에서뺐다.

## 생성 실행과 배포 복사

[생성기록조회](generation-search.json)는 여섯정확SHA(source태그/docsrevision/publication×두판)에대한 Actions/status/checks18개와 2023-01-11..14 및2023-02-13..16의source/publication저장소 created창4개, 총22개다. 모두HTTP200, visible total_count0이다. status집계의pending은 상태행0개의기본값이며 실제실행중job이 아니다. 조회한보존범위에서 실행·출력manifest를 확보하지 못했다. 과거job부재나G=NO의증거가 아니다.

[공식releaseguide](https://github.com/matplotlib/matplotlib/blob/d6dd1b79142e4e2483244c25ff1e3ddb664722d3/doc/devel/release_guide.rst#L359)는 release태그설치와ver-doc문서소스를 구별하고 html/pdf를만든뒤발행저장소로rsync한다. [CircleCI배포규칙](https://github.com/matplotlib/matplotlib/blob/235131a6bc2527aee7eea370fd5f94564a48c20d/.circleci/deploy-docs.sh)은 main/non-PR조건에서devdocs로복사한다. 이규칙을선택한release발행의실제job으로취급하지않았다. Makefile에는html-noplot/plot_gallery=0이있고conf에는release이미지압축/2x srcset/animation설정이있다. 설정·가능한실행과실제관측한생성을구별했다.

## 독자 목적별 반환과 값싼 확인

옛판인용은 fixedGitHub HTML소스의정확행과그림주소를준다. 원본의rawHTML을렌더된사이트라고설명하지않는다. 조사한새판의이용은 확인한3.7.0실제fragment를준다.2026최신판을조사한것이아니다. root가live3.7.0 네본문을다시열어 전체바이트는달라도범위본문+img속성은4/4같고연결PNG8개가SHA일치함을확인했다. root영수증은 `evidence/return-url-checks.json`, `evidence/return-url-scope-comparison.json`, `evidence/live-payload-checks.json`이며이중확인은고유자료수를늘리지않는다.

본문설명만이면정확판/절1회확인으로충분하다.그림을재사용하면그절에서실제payload를1회더따라간다.당시생성귀속이나빌드재현을원할때만source/environment/job/outputdigest연결이추가로필요하며현재미확인이다. 각사례의URL/비용조건/경고한줄은returns.json에둔다.

## 실제검토·수정·재현

이작성자의의미판독은자기검토다. root의별도모집/봉인검토및live재열람과구별한다. [self-corrections.json](self-corrections.json)에serialized줄수경계교정,JS세미콜론없는프레임문법교정,실제SHA없는동등성계산금지,재현스크립트의불완전트리조기실패가드를기록했다. 선택·봉인파일은고치지않았다.

재현은먼저봉인파일과commit을읽고,그다음audit_main.py/audit_supplemental.py의정확공식URL을따라관측한다. get/cached는HTTP원영수증을남긴다. stage1.py/stage2.py를현재봉인디렉터리에서덮어쓰도록재실행하지말고별도복사본에서출력을대조해야한다. sourceZIP대조와Gitblob검사는고정파일정합성을보며프로그램·애니메이션·역사적생성job을실행한검사가아니다.

최종원장209행 / 보수적으로고유1차자료54개. 본문22·그림22·발행/목록/배포/변경/규칙10개다. 양판같은저작·density·code표현·동일바이트를합치고,098계승자료·자동모집만한본문·빈실행조회·실패응답을최소수에서뺐다. [counts-project.json](counts-project.json), [source-inheritance-reconciliation.json](source-inheritance-reconciliation.json).
