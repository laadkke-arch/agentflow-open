# AF-RES-086 Q7 — 판을 가리키는 주소, 실제 파일, 보관 기록

## 확보한 판 쌍과 원래 분모

| 제도·작품 | 실제로 읽은 두 판의 원기록 | 양쪽 파일 또는 manifest | 확인 범위 |
| --- | --- | --- | --- |
| 학술 저장소 Zenodo / Umap·Bismap | [60943](https://zenodo.org/records/60943), [800648](https://zenodo.org/records/800648); 공통 concept705645 | 두 tar.gz 전체를 내려받아 MD5 대조·245/263 member manifest·setup.py 판 번호를 직접 읽음 | 현재 공개한 역사판 파일이 서로 다르고 각각1.0.0/1.1.0임을 확인. 당시 웹 게시/독자 응답 연속성은 미확인 |
| Zenodo / matplotlib | [2893252](https://zenodo.org/records/2893252) v3.1.0, [3695547](https://zenodo.org/records/3695547) v3.2.0; concept592536 | 두 레코드의 ZIP명·길이·MD5·태그 링크 manifest | 원장에 기록된 파일 판별. ZIP 바이트 자체는 내려받지 않았으므로 발행자 지문과 직접 검증을 구분 |
| 소프트웨어 보존기관 Software Heritage / GNU hello | [2.9 revision55c14d…](https://archive.softwareheritage.org/api/1/revision/55c14d05501df7b03da249166f077a50007f8acf/), [2.10 revisiondbdaa32…](https://archive.softwareheritage.org/api/1/revision/dbdaa32b99fc923182a4e881b3c6996a8c0ac9d8/) | 각 tar 루트·내부 디렉터리 manifest29/30항목과 configure.ac 실제 바이트. 2.10 NEWS도 읽음 | 2015-08-28 full archive visit→하나의 snapshot→두 synthetic revision→각 파일의 연결. source 보관 증거이며 실행·HTML 게시·HTTP 동시 제공 증거가 아님 |

필수 비교는 **2제도, 3작품의 판 쌍, 실제 판 원기록6개**다. 같은 작품의 두 판을 독립 계보 둘로 세지 않았다. 모든 직접 자료는 `sources.jsonl` 28행이며 중복 표현·래퍼4행을 제외한 최소량 대상은 **24개 원자료 / 7계보**다. 정책 두 계보, 작품 판 관계 세 계보, 철회 사건 한 계보, Gitorious 보존 사건 한 계보로 묶었다. 원자료 수는 서로 다른 API 응답/파일 수이고 계보 수는 독립 작품·사건 수다. 이 분모는 P3·R1·P1·R2 및 12사건 분모와 합치지 않는다.

`pairs.json`이 판별 DOI, concept DOI, 보관 revision/directory, 발행자 체크섬, 직접 계산한 체크섬을 구분한다. `evidence/PR23.manifest.json`과 `PR24.manifest.json`은 tar 안의 각 경로·길이·mtime·파일 SHA256을 기록한다. 압축을 경로에 풀거나 코드를 실행하지 않았다.

## 1. 이동 개념 DOI와 특정 판 DOI

Umap의 구판 DOI60943은 파일명`umap_1.0.0.tar.gz`, 신판 DOI800648은 `umap_1.1.0.tar.gz`를 가리킨다. 두 레코드 모두 concept705645를 선언한다. 이번 concept API 요청은 최종800648로 이동했다(PR06·PR10). 실제 압축 내부 `umap/setup.py`가 각각1.0.0/1.1.0을 선언하므로 FAQ의 예시만 되풀이한 판단이 아니다(PR23·PR24). metadata.version 필드가 없는 점도 보존했다.

| 판 | 발행자가 적은 MD5 | 실제 내려받은 SHA256 | 바이트 |
| --- | --- | --- | ---: |
| Umap1.0.0 | `1e05e5c177ed99b9eab4f82ef122c7c3` | `18797b1de01b6b47187fb64b369e0e6e5898dd3fe7ba8758b3c0adb34c7004e8` | 1,673,515 |
| Umap1.1.0 | `4b256f0b0196175b19f77b26370792de` | `502f9ed7d4a879605985cbbe7fd254803c5f33f9d539975ebe839a02096e9c6c` | 1,868,653 |

직접 계산한 MD5도 발행자 MD5와 두 파일 모두 일치한다. 다른 알고리즘인 MD5와 SHA256 문자열을 서로 같다고 비교하지 않았다. 압축 파일이 현재 보존됐다는 결과를 이 파일로 문서 사이트가 빌드·게시됐다는 결론으로 옮기지 않는다.

matplotlib에서는 v3.1.0과 v3.2.0의 파일 목록이 서로 다른 크기39,444,602/42,576,783bytes와 MD5를 선언한다(PR01·PR02). 현재 concept592536는 v3.11.2인22700776으로 이동한다(PR03). 최신 내용을 원하는 독자와 과거 버전을 재현하려는 독자는 다른 링크를 받아야 한다. 이동 자체는 오류가 아니다. 어느 판을 요구했는지가 먼저다.

현재 [Zenodo DOI versioning](https://zenodo.org/help/versioning)은 판 DOI와 concept의 역할을 나눈다(PR08). 그러나 [Manage files](https://help.zenodo.org/docs/deposit/manage-files/)는30일 내 경미한 파일 수정, 최초 발행45일 내 재게시, DOI 불변을 명시한다(PR16). 따라서 고정 DOI 문자열만으로 바이트가 어떤 시점에도 불변이었다고 단정할 수 없다. 조사한 Umap/matplotlib에서 실제 수정이 발생했다고 주장하지 않는다.

## 2. 보관 목록의 시각과 웹 게시의 시각

SWH의 [full visit1](https://archive.softwareheritage.org/api/1/origin/rsync://ftp.gnu.org/gnu/hello/visits/)은2015-08-28T11:13:26Z와 snapshot `a5e907833c4c1dbacb652e6f65fd9f5fdd1dad5a`를 준다(PR20). 그 [snapshot](https://archive.softwareheritage.org/api/1/snapshot/a5e907833c4c1dbacb652e6f65fd9f5fdd1dad5a/)은 두 tar 파일명에서 각 revision으로 연결한다(PR09). revision의 `type=tar`, `synthetic=true`는 이 정보가 수집자가 만든 모델임을 드러낸다. 이 `date`를 원발행자의 CI 성공 시각이나 게시 승인 시각으로 바꾸지 않았다.

각 revision은 한 단계 래퍼 디렉터리를 거친다(PR25·PR26). 내부 파일 목록은 [2.10](https://archive.softwareheritage.org/api/1/directory/bd2df77b4740795f466bca7ffbf18f395d92a9d4/)과 [2.9](https://archive.softwareheritage.org/api/1/directory/3c6120f00826d297e0a1f1b2191f5e023155fad9/)로 다르다(PR29·PR30). configure.ac 바이트 SHA256은 각각 해당 목록의 발행자 체크섬과 일치한다(PR32·PR33). 구판은AC_INIT에2.9를 직접 적고, 신판 configure.ac는 버전을 간접 계산하므로 이것만으로2.10 문자열을 봤다고 기록하지 않는다. 별도로 읽은 NEWS가2.10(2014-11-16)을 표시한다(PR35).

한 archive snapshot에 두 판의 경로가 함께 들어 있다는 것은 두 판의 보관 구조를 잇는 좋은 근거다. 그러나 브라우저가 원 문서 사이트의stable·1.x로 요청한 결과, 캐시, 리다이렉트, anchor, 게시 구간 교집합은 이 기록에 없다. 따라서 이 제도만으로 P3의 역사적 동시 제공 공백을 메우지 않는다.

## 3. 내용이 남고 주소가 사라진 경우, 주소가 남고 내용이 비공개가 된 경우

| 방향 | 실제 기록 | 판정·한계 |
| --- | --- | --- |
| 주소/식별자는 남지만 원파일 공개는 철회 | DOI [22705920](https://doi.org/10.5281/zenodo.22705920)의 실제 최종 응답410, API의retracted tombstone·철회일2026-09-19(PR07·PR11) | ID와 인용은 남지만 파일 목록이 없다. 의도된 철회이며 호스팅 실패율에 넣지 않는다. 현재410만으로 최초 발행 당시의 공개 여부를 판정하지 않는다 |
| 옛 호스팅 주소의 제공 종료 보고 + 실제 내용 보존 | [ArchiveTeam 고정 위키59702](https://wiki.archiveteam.org/index.php?title=Gitorious&oldid=59702)는 읽기 전용 미러가2024-09-30까지였다고 보고(PR21). SWH origin→snapshot→revision→33항목manifest→Home.markdown 실제1,319bytes를 읽고 SHA256 일치(PR13·PR19·PR27·PR31·PR34) | 보존 파일은 직접 확인했다. 옛 `gitorious.org`의 두 요청은 이 실행환경의upstream timeout503여서 원서버의영구404 증거로 세지 않는다. 옛 주소 종료는 보존 작업 참가측 보고 수준으로 표시 |

Gitorious Home.markdown의 직접SHA256은 `09cdb307d94790b965862f960c5867b90669150cada8079086b726eea2e77d62`다. `https://archive.softwareheritage.org/api/1/content/sha1_git:8f2ec2768803102276967ed51ff598eaf352ae48/raw/`에서 실제 본문을 읽었다. source 보존과 원 도메인 서비스 보존을 분리하는 사례다. 모든 wiki페이지·첨부파일까지 확인한 것은 아니다.

강한 주장인 “옛 URL은 원서버에서 영구 소실됐고 보관소의 모든 파일은 동일하다”는 아직 지지하지 않는다. 이 판정을 바꾸려면 해당 옛repository경로의권위있는종료기록 또는 정상네트워크의원서버응답과 보관tree전체대조가 추가로 필요하다. 현재 존재하는 자료만으로도 “주소와 내용의 생존을 별도 검사해야 한다”는 약한 결론은 지지된다.

## 4. 실제 확인 비용과 역할별 남은 확인

`costs.json`과 `attempts.jsonl`은 비용을 재검산할 수 있게 한다. **계측된 논리GET35회, 받은 응답 본문3,777,598bytes**이며 이 중 압축파일2개는3,542,168bytes다. HTTP200은29회, 실제 철회410은2회, 실행환경의upstream503은4회다. HTTP status의횟수를자료계보나성공률로해석하지않는다.

| 확인 묶음 | 실제 논리GET | 받은 본문 bytes | 목적과 남은 확인 |
| --- | ---: | ---: | --- |
| Umap두 판 metadata+두 파일 | 4 | 3,550,667 | 독자는판·바이트를식별할수있음. 릴리스담당자는기탁파일이정확한태그/빌드산출물인지연결해야함 |
| matplotlib두 판manifest+concept관측 | 3 | 15,252 | 독자는특정판과이동링크를구별. 실제ZIP다운로드는미실시이므로파일바이트대조가남음 |
| GNU hello탐색·visit·snapshot·두판·대표파일 | 12 | 41,108 | 보관기관자료의객체연결과대표바이트대조. 웹서비스제공자는HTML게시·route·응답영수증을따로제공해야함 |
| Gitorious보존·구주소대조·실패조회 포함 | 9 | 46,993 | 보관파일존재확인. 옛도메인종료의직접원서버응답과전체파일범위는미확인 |
| 철회API+DOI직접요청 | 2 | 43,249 | 독자에게원파일을주지못함을명시. 별도대체판을임의로원판취급하지않음 |
| Zenodo·SWH정책조회(실패1포함) | 4 | 66,267 | 현재도움말의계약만확인. 과거계약과개별배포사실은별도 |

위 표의 숫자는 직접기록된 요청묶음이고, 전체35회에는 SWH문서의예시directory를확인한 교정요청1회14,062bytes가 추가된다. HTTP자동redirect의내부hop수는측정하지않아논리GET로명시했다. 계측전탐색3회와웹검색도구의검색6질의·open10개는 `lookup-log.jsonl`에별도남기며, 도구가응답byte수를제공하지않아서합계에추정치를넣지않았다. 파일바이트비용은사람작업시간·서비스요금이아니다.

독자가스스로증명하면목표판의기록과실제파일까지읽는비용이생긴다. 릴리스담당자가source SHA→배포run→artifact manifest를미리제공하면같은출판단계를추정할필요가줄어든다. 서비스제공자만가질수있는라우팅변경·동시게시구간·캐시응답영수증은문서읽기횟수를늘려도생겨나지않는다. 공개기록이없으면독자는“생성물확인,당시제공미확인”을받아야한다. 이것은측정된속도효과가아니라관측권한에따른남은증명항목의분석이다.

## 5. 반대 방향 검토와 재현 한계

- concept가움직였으니링크가틀렸다는첫결론은기각했다. 최신판을요구한독자에게는정책과일치한다. 특정판독자에게만고정DOI/파일을반환한다.
- fixed DOI가있으니bytes가영구불변이라는결론은현재파일수정정책과tombstone으로제한했다. 그렇다고Umap에서실제바이트교체가있었다고추정하지않는다.
- full archive visit가있으니원사이트의두경로가동시에정상이라는결론은보관소데이터의범위를넘으므로기각했다. SWH의synthetic revision과원발행자의run은서로다른식별자다.
- Gitorious의503을원서버폐쇄확정으로분류하지않았다. 직접읽은보존본문,참가측종료보고,실행환경접근실패를세열로남겼다.

재실행 도구는읽기전용GET·메모리내tar검사·원장조립만한다. `fetch_records.py`는주소목록JSON을받으며1회씩만요청한다. `read_archives.py`는두고정metadata를입력으로사용하므로재현시PR06·PR10원API조회후실행한다. `assemble.py`는저장된metadata의추출본도읽는다. 원문전체HTML/긴abstract는보존하지않았고짧은추출과영수증을남겼다. **영수증의sha256은전체받은응답의지문이고extract_sha256은짧은추출파일의지문으로서서로다르다.**

이stream은root의원장합산·독립사건검산·네카드판정자료다. 별도커밋,중앙색인수정,외부서비스생성/변경은수행하지않았다.
