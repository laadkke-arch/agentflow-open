# ROR 검색·열람 기록

관측일: 2026-11-22 UTC. 마지막 ledger 체크포인트 03:18:12 UTC. 먼저 GitHub issue/comment를 읽고 고정 release-candidate 파일로 내려갔다. 검색 결과/요약만 본 자료는 최소 원문 수에서 제외했다.

## 실제 실행한 GitHub 검색

| 질의 | 열린 사건/결과 | 반증 또는 한계 |
|---|---|---|
| `repo:ror-community/ror-updates duplicate` |15331,13495,2845 |동명 중복 인정과 지부 병합기각을 대비 |
| `repo:ror-community/ror-updates successor` |20329,3418 |한 후계로 고를 수 없는 경우를 찾음 |
| `repo:ror-community/ror-updates incorrectly` |후속 revert 검색으로 이동 |키워드만으로 원 오류를 확정하지 않음 |
| `repo:ror-community/ror-updates split` |3418 및 다수 무관 ORCID 요청 |요청만 있고 구현없는 사건은 본표 제외 |
| `repo:ror-community/ror-updates duplicate closed:<2025-01-01` |15331,13495,2845 |성공중복병합만 모으지 않기 위함 |
| `repo:ror-community/ror-updates "incorrectly"` |정정 후보 |실제 before/after 파일 있는 후보로 좁힘 |
| `repo:ror-community/ror-updates "split" closed:<2025-01-01` |3418 |기관분리와 카탈로그분리를 구별 |
| `repo:ror-community/ror-updates "successors"` |20329 |복수 후계 경계 |
| `repo:ror-community/ror-updates "00zg0xv61"` |유효 결과 없음 |정책 blog 예시를 실제 사건으로 승격하지 않음 |
| `repo:ror-community/ror-updates "000qg0t28"` |15331,15407;14362는 검색만 |원 생성요청14362는 직접원문수에 제외 |
| `repo:ror-community/ror-updates "merged in error"` |유효 원문 없음 |literal 오병합 취소 표본을 충분히 찾았다고 주장하지 않음 |
| `repo:ror-community/ror-updates "revert"` |25805,19416,25802,16454,17073,6693,21008,19286,21009 |동일 ID 잘못된 대상 갱신과 실제 정정판 확보 |
| code search `01z6gk692`, `00ks26d70`, `041xzk838` in ror-updates |각 rc 파일, CNR v1.3 부모파일 |원 dump 없이는 이전 정체성 전체를 재구성했다고 쓰지 않음 |
| `repo:ror-community/ror-updates "merged to form"` |159,43488 |현실 기관합병과 카탈로그 반영일의 차이를 보강; supplement 참조 |

## Web 검색 및 직접 열린 소비자

- `"041xzk838" -"ror-community"`, `"04xjkmz40" -"ror-community"`, `"01sxmzj91" -"ror-community"`, `"01z6gk692" -"ror-community"`를 실행했다.
- `"041xzk838" "Biofisika" -site:github.com` 및 논문 전체 제목을 검색했다.
- `"041xzk838" "Biofisika" -site:github.com -site:colab.ws -site:openalex.org`, `"04xjkmz40" "San Luis" -site:github.com`, `"01z6gk692" -site:github.com -site:ror.org`, `"000qg0t28" -site:github.com -site:ror.org`를 실행했다.
- COMTES Contacts, EQAR205, CoLab041xzk838, OpenAlexI4210143448, science.eus metadata를 직접 열었다. 같은 COMTES .cz/.de 번역판은 검색결과가 나왔으나 별도 독립 소비자로 추가 산입하지 않았다.
- GitHub의 #13357 Rockwell 후보는 현재 open 상태의 제안으로 읽었으나 구현 증거를 확보하지 못해 사건 표본에서 제외했다. 두 회사/연구기관의 현실 흡수합병을 이유로 완료된 카탈로그 병합이라고 추정하지 않았다.

## 직접 접근 실패/산입 제외

| URL 또는 경로 | 실제 관측 | 처리 |
|---|---|---|
| `https://ror.org/blog/2022-12-07-handling-org-status/` |403/접근실패 |검색 snippet의 예시만으로 사건 수 산입안함 |
| `https://ror.readme.io/docs/ror-identifier-pattern` |web 접근실패 |정책수 제외 |
| `https://ror.org/` 및 ROR API 경로 |shell403 등 접근실패 |HTTP가 엔티티404라는 해석 금지 |
| `rc-v1.23/updates/01dbbht76.json` |GitHub 파일404 |해당경로 부재일 뿐 ROR 엔티티 삭제가아님 |
| `rc-v1.67/updates/01fva0642.json` |GitHub 파일404 |잘못 추정한 release; 실제 v1.68 파일확보 |
| `https://pmc.ncbi.nlm.nih.gov/articles/PMC11415298/` |web recaptcha, shell203/5581bytes에ROR없음 |검색결과의ROR소속 인용을 직접원문수로세지않음 |
| `https://www.nature.com/articles/s42256-024-00883-x` |web IDP경유실패; shell200/453104bytes이나041xzk838 문자열 없음 |논문 본문이 읽힌다고 ROR메타데이터 직접확인했다고 쓰지않음 |
| `https://dataverse.csuc.cat/dataset.xhtml?persistentId=doi:10.34810/data1547` |web502 |검색소속값 제외; session query URL 저장안함 |
| `https://portalcientifico.uned.es/documentos/61d68a2fb32d1a43ae9f2279` |접근실패 |Cuauhtémoc소속 검색snippet만으로소비자수산입안함 |
| WebometricsRankingJanuary2025 PDF 검색결과 |기간부 서명URL만있었음 |토큰/서명URL 보존안함, 소비자수 제외 |
| `https://www.imbiomed.com.mx/articulo.php?id=120086` |검색만 |직접원문수 제외 |
| `https://www.schleswig-holstein.de/DE/landesregierung/ministerien-behoerden/LLUR/llur_node.html` |robots 차단 |현실 분리 사실의 독립 검증은 미확인 |
| EQAR direct shell URL |403; web 도구에서는 본문 직접 열림 |web 열람은산입, shell403을페이지실제삭제라해석하지않음 |
| science.eus direct shell URL |200/63699bytes, RORgeocard확인 |web본문과동일항목재확인; 같은원문두번산입안함 |
| ROR updates docs direct shell |403; web에서는본문열림 |접근경로별결과기록; 현재HTTP를일반화안함 |
| `https://www.irif.fr/en/informations/presentation` |web restricted URL |기관합병의독립기관원문미확인; supplement에한계기록 |

## 부정 사례 탐색 결과

마지막 검증에서 공개 GitHub issue-comment 원문 14건의 `created_at`/`updated_at`을 조회했다. URL은 해당 `sources.json` 행의 `comment_metadata`에 남겼다. 정규화 도구의 빈 댓글시각을 issue 종료시각으로 대체하지 않기 위한 확인이며 같은 사건을 추가 원문으로 산입하지 않았다. 특히 PTSD 기각 댓글은 2024-11-05, issue 종료는 2024-12-02다.

실제 기관합병 보강 검색은 `IRIF LIAFA PPS 1 janvier 2016 site:u-paris.fr`, `IRIF LIAFA PPS 1 janvier 2016 site:cnrs.fr`였다. 별도 공식 대학 페이지 `https://www.informatique.u-paris.fr/ufr/presentation_ufr`를 직접 열어 Recherche 절의 합병일과 페이지 수정표시를 확인했다. IRIF 자체 사이트 접근 실패를 해결한 것으로 기록하지 않고 별개 출처로 기록했다.

“정상 이름 alias면 충분하다”는 가설에 ROR06–08을 대조했고 같은 ID가 다른 기관/캠퍼스 내용을 잠시 담은 정정 사례를 확보했다. “수정 승인/배포면 모두 복구된다”는 가설에는 ROR07 locations 잔존이 반한다. “조금이라도 다른 이름/웹이면 분리한다”에는 ROR01의 같은 회사 중복 통합과 ROR08의 실제 Netrokona ID 안의 역사명 alias가 반한다. “후계이력이 있으면 하나를 자동추천한다”에는 ROR04·05의 복수후계가 반한다. “본부와 지부는 항상 합친다”에는 ROR02의 기각 판정이 반한다.

정정 사례의 외부 사용자가 실제로 오류 인용을 되돌린 날짜/commit은 확보하지 못했다. 같은 ROR ID의 하위카탈로그 설명 불일치를 실제 이용자 피해나 보편적 오병합률로 바꾸지 않는다. 이 목적 표집으로 전체 오류율을 계산하지 않는다.

