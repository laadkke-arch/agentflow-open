# R 모집 및 원요구 — 사전 단계

고정 조직 목록 164개 중 원순번 1–9를 조사했다. 기간 내 정식 배포 후보는 7개이며, 문서 원본과 자기 문서 사이트의 외부 링크가 함께 있는 첫 세 자리는 archive / asciicast / bench다. 주언어는 C++ / R / R이며 언어로 임의 제외하지 않았다. 후순번 155개는 선정 완료 후 열지 않았고 FRAME에서 유지한다. 현재 조직 소속을 2024–2025년 소속으로 소급하지 않는다.

| 자리 | 원순번 | 고정 태그/출판 날짜 | 문서 진입 URL | 알려진 조건 수 |
|---|---:|---|---|---:|
| R1 archive | 4 | v1.1.12, 2025-03-24 | https://archive.r-lib.org/ | 공개 문서 진입 의도 1; 별도 보존 약속 미확인 |
| R2 asciicast | 5 | v2.3.1, 2024-01-21 | https://asciicast.r-lib.org/ | 공개 문서 진입 의도 1; 별도 보존 약속 미확인 |
| R3 bench | 9 | v1.1.4, 2025-01-16 | https://bench.r-lib.org/ | 공개 문서 진입 의도 1; 별도 보존 약속 미확인 |

README·NEWS·DESCRIPTION은 읽었고, source tree에서 `man`, `_pkgdown.yml` 및 workflow 파일 이름은 보았지만 구성 본문·사이트 HTML·공급자 계약을 아직 열지 않았다. archive의 `No changes`는 제품 릴리스 기록이지 웹 문서 무변경 관측이 아니다. asciicast의 SVG/HTML/vignette 기능은 제품 기능이며, 이를 자동으로 문서 사이트의 두 번째 보존 요구로 세지 않는다. bench의 mark/press 기능 설명도 동일하다.

## 제외와 모집 정의

- actions(원순번1): NEWS로 v2.11.4(2025-10-08)가 기간 마지막 정식 태그임을 확인했다. GitHub의 v2 release 객체는 2021 최초 발행 후 갱신되므로 GH release 날짜만으로 기간 부재라 오인하면 안 된다. 해당 README는 개별 action README, 사용 예와 외부 블로그/참고책을 안내하며 자기 문서 사이트의 출판 경로를 안내하지 않는다. 대상 문서 사이트 자격 제외다.
- actions-files(2): v2.0.0 정식 배포, README 한 파일뿐. 문서 원본 추가 조건 미달.
- ansistrings(3): release와 tag가 모두 비어 있다. NEWS 날짜 없음·개발 버전 표기만 있으므로 기간 정식 태그 미확인.
- askpass(6): 1.2.0 정식 배포와 man 원본은 있지만 README/DESCRIPTION에 자기 docs 사이트 링크/게시 안내가 없다. 태그 전체도 1.2.0 하나다. CRAN 설치/상태 배지 링크를 독립 문서 사이트 약속으로 바꾸지 않는다.
- available(7): 마지막 정식 1.1.0은 2022-07-13. 태그·NEWS를 대조했으나 기간 배포 없음.
- backports(8): v1.5.0 배포·man 원본은 있으나 자기 GitHub와 외부 base R 설명서만 안내한다. 자기 docs 사이트 자격 제외.

## 증거 저장

`receipts.jsonl`은 직접 조회 URL/UTC/status/지문과 tag refs를 보존하고 `sources.jsonl`은 읽은 내용·한계·주장을 제공한다. `raw/`는 재판독 임시 캐시이며 Git 저장 대상이 아니다. 모든 재취득은 receipt의 URL과 고정 tag SHA로 가능하다. 이 단계의 독립 소비 프로젝트 계보는 3개다. 모집 metadata를 22개 기준에 보태지 않는다.

현재 `requirements.jsonl`은 자리별 2행(총6행)이며 C2 미확인 3행을 유지한다. 이는 세 자리를 교체할 이유가 아니다. A/B 첫 안내 동결과 동일 2회 예산 판독 뒤 사후 배포·이슈 조사를 진행한다.
