# Python 목적지 관측 · 단계 3

## 판정과 원장 연결

**확인된 것은 원5번 AWS S3 URL의 승격이다. 요구를 완결하는 독립 구현의 승격·손실은 미확인이다.** P-S1에 목록과 독립적으로 고정한 적격 사용자 목적을 연결하지 못했기 때문이다. 관측 뒤 미러링·S3 요구를 새로 만들지 않았다. 공급자 두 곳, 정확 URL 다섯 개, 독립 완결 구현 수, 사람의 채택 수는 서로 다른 단위다.

목적지 이전 배열은 원격 `ea4fa69f841dca2c470b62c3fdf1ee4d9029712e`에 봉인돼 있다. 이 파일은 그 뒤 읽은 내용만 추가한다. 로컬 `P-S1-Un`은 루트 원장의 `P-S1-Rn`과 같다. `D-P1-Un`도 `D-P1-Rn`과 같다. `arrivals.jsonl`은 도착 창, `paths.csv`는 동일 도착을 A/B/C에 재사용한 경로, `evidence.csv`는 주장과 한계, 두 sources 원장은 저작별 출처다.

| 슬롯·원장 | 봉인된 관측 | 최종 판정 |
| --- | --- | --- |
| P-N1 / P-N1-A·B·C | #564의 고정 기능 명사와 목록 제목·명시 별칭 무매치 | 반환 풀 **관측 0**; 모든 방식의 대표·경로 빈칸. 구현 자체가 없다는 뜻이 아니다. |
| P-N2 / P-N2-A·B·C | #574도 무매치 | 반환 풀 **관측 0**; 방식별 조건부 효과율은 **해당 없음**. |
| P-S1 / PY-E01–05 | bandersnatch 절에 정확 URL5개, 원4번도 존재. B가1–4를 묶어 원5번 승격 | 메타데이터 기회 확인. 사전 목적 미연결로 원풀·직접·두 동작·한 시행 최대 완결 ID 및 증감은 **미확인**. |
| P-S2 / P-S2-A·B·C | 첫20 기능 절에서 엄격 C 충돌 미선정 | 미선정 자리 유지. 목적·풀을 바꿔 채우지 않았다. |

## 같은 세 자리에서 무엇이 달라지는가

| 원장 | 대표 원순번 | 숨은 형제 / 잘린 그룹 | 읽은 자료와 정확한 한계 |
| --- | --- | --- | --- |
| P-S1-A | 1,2,3 | 형제 없음 /4,5 | 매뉴얼·이슈 목록·README. 직접 도착4는 잘리지만 B에서는 그룹으로 읽을 수 있다. |
| P-S1-B | 1,5 | 형제2,3,4 / 없음 | 세 번째 자리는 비어 있다. AWS는 별개 공급자의 객체 저장 서비스이며, 공식 저장소 장은 이를 bandersnatch의 **보완 백엔드**로 설명한다. |
| P-S1-C | 1,2,3 | 형제 없음 /4,5 | 제품판과 문서 역할이 알려지지 않아 각 행 단독. 나중에 읽은8.2.0·README 의미로 키를 보완하지 않았다. |

P-S1의 실제 경로 원장은 **49행**이다. 사전 direct/pair/group-member33행에 첫 두 정보 href 경로16행을 더했다(A18/B13/C18). 모두 사람의 연속 클릭 실험이 아니라 직접 획득한 같은 도착 창의 쌍 비교 재구성이다. 한 경로에서 얻는 자료만 묶었으며 서로 다른 시행의 부분조건을 합쳐 정답을 만들지 않았다. 질문 목적이 없으므로 `complete_implementation_ids`와 count는 null이다. 빈 배열을 써서 관측0으로 바꾸지 않았다.

진단 D-P1은 사전 계획 39행, 확인된 첫 href 순서로 만든 16행, 미구체화 hop 자리 2행을 합해 57행이다. 사전 계획 중 6행은 build:index를 포함해 시작 URL이 미해결이다. 따라서 시작 URL이 알려진 경로는 49행이고, 미해결 시작 6행과 hop 자리 2행은 실행 가능한 완성 경로로 세지 않는다. build:index의 정확 목적지 URI가 inventory 실패로 미확인이라 해당 시작 URL 및 다음 href를 발명하지 않았다. 공식 conf.py가 가리키는 build 문서 base를 읽은 것은 별도 맥락 획득이며 D-P1rank6의 성공한 도착이 아니다.

## 원5개 도착과 첫 두 정보 href

| 도착 ID·원순번 | 실제 도착 절·판 | 첫 두 실제 정보 링크 | 결측·노출 |
| --- | --- | --- | --- |
| PY-A01 /1 | [매뉴얼](https://bandersnatch.readthedocs.io/en/latest/) 제목 뒤 본문,8.2.0;786단어에서 본문 소진 | [PEP381](https://peps.python.org/pep-0381/); -h 옵션 링크 | 옵션 링크 클릭이 fragment를 노출하지 않아 정확 anchor 도착 미확인. Sidebar·Contents와 제목¶를 건너뛰었다. |
| PY-A02 /2 | [Issues 목록](https://github.com/pypa/bandersnatch/issues),400단어 반환 본문 | [#2320](https://github.com/pypa/bandersnatch/issues/2320); [#2059](https://github.com/pypa/bandersnatch/issues/2059) | 목적지 목록은 관측 당시 동적 순서. 이2025/2026년 요청들을2022–2024 자연 프레임에 추가하지 않았다. |
| PY-A03 /3 | [README 고정판](https://github.com/pypa/bandersnatch/blob/81a81eb894fa5a014298c04be2c956f620864648/README.md) L30 Installation 뒤800단어 | [Docker Compose tree](https://github.com/pypa/bandersnatch/tree/main/src/bandersnatch_docker_compose); [PyPI통계](https://pypi.org/stats/) | 첫 실제 Markdown 제목 전의 배지·머리말은 창 밖. SHA는 제품판을 뜻하지 않는다. |
| PY-A04 /4 | [PyPI 초기 반환](https://pypi.org/project/bandersnatch),7.0.0;347단어까지만 같은 스냅샷 확보 | [메타데이터 확인 규칙](https://docs.pypi.org/project_metadata/); [Homepage](https://github.com/pypa/bandersnatch/) | 같은 ref의 연속 열람이 다른8.2.0 배치를 반환했다. 첫800단어를 이어 붙이지 않았다. **부분 도착**이다. |
| PY-A05 /5 | [S3](https://aws.amazon.com/s3/) L220 제목 뒤800단어 | [Tables](https://aws.amazon.com/s3/features/tables/); [Express One Zone](https://aws.amazon.com/s3/storage-classes/express-one-zone/) | 두 링크 모두800단어 안. 계정·영업 CTA와 장식 이미지는 제외. 별도 제품판은 미확인. |

웹 도구는 HTTP 응답 코드를 제공하지 않았다. 따라서 `opened`를 HTTP200이라고 바꾸지 않았고 전체 redirect chain도 확인했다고 하지 않는다. 실제 반환 canonical URL만 기록했다. 렌더된 브라우저 화면이나 사람의 이해를 측정한 자료가 아니다. 공개 원문 링크를 직접 읽은 사실과 도구가 제공한 캐시 본문의 신선도를 구별한다.

## 보완 정보가 가려지는 경로와 반례

**이슈 본문 접근은 실제 차이가 난다.** A/C는 Issues 대표→#2059를 두 동작에 읽는다(PY-A02→PY-A09). B의 그룹 목록→Issues는 이미 두 동작이므로 해당 보고 본문은 세 번째 동작이다. 보고에는6.6.0의S3·여러 필터 조합 문제와 상호작용 시험 부족을 인정한 후속 응답이 있다. 이것은 보완 정보의 경로 차이지만, 사전 P-S1 목적에 필요한 절이라고 입증하지 못했으므로 필수조건 손실 양성으로 세지 않는다(PY-E08).

README→Compose 예제도 A/C에서 두 동작, B의 그룹 경유라면 세 동작이다. 다만 실제 tree URL은 `Failed to fetch restricted URL`로 실패했다(PY-A10). 이후 [고정 README 소스](https://github.com/pypa/bandersnatch/blob/81a81eb894fa5a014298c04be2c956f620864648/src/bandersnatch_docker_compose/README.md)를 승인된 GitHub 경로로 별도 읽어 nginx·볼륨·MTU·HTTPS 조합 설명을 확인했다. 이 소스를 원 tree 도착의 성공이나 두 동작 완결로 간주하지 않았다(PY-E10).

반대로 B에서 앞으로 온 AWS는 bandersnatch 대체 구현으로 확인되지 않았다. [공식 저장소 장](https://bandersnatch.readthedocs.io/en/latest/storage_options.html)은 S3를 선택 저장 백엔드로 놓고 extra 설치와 설정을 설명한다. 같은S3 이름으로 도착한 Tables·Express의 다른 버킷 유형까지 해당 백엔드가 지원한다는 근거는 없었다. 공급자 다양성이 조합의 유용성을 높일 가능성은 있으나 이 표본의 독립 구현 증가와 동일하지 않다(PY-E06; PY-O12/13/15).

PEP381은 매뉴얼에서 가장 먼저 읽히지만 현재 상태가 Withdrawn이다. 이름이 공식 규격과 같다는 사실만으로 현재 동작·판의 완결을 보장하지 않는 반례다(PY-O06). #2320의 API 전환 제안도 이미 출시된 기능으로 읽지 않았다(PY-O08).

## 코드·시험 정답과 사용자 창을 분리한 확인

[CHANGES 고정판](https://github.com/pypa/bandersnatch/blob/81a81eb894fa5a014298c04be2c956f620864648/CHANGES.md)에서8.0.0·8.2.0 절과Unreleased를 구별했다. [S3 시험 파일](https://github.com/pypa/bandersnatch/blob/81a81eb894fa5a014298c04be2c956f620864648/src/bandersnatch/tests/plugins/test_storage_plugin_s3.py) L964–1000은 HeadObject 호출 수, L1002–1018은stat 모드, L1448–1491은메타데이터/명시 설정 보존을 검사하는 정의다. 두 저작은 별도 릴리스·행동시험 배당에 사용한다(PY-T01/02).

시험은 **읽었고 실행하지 않았다(D2)**. 해당 tree의 모의 S3 시험 정의를 실제 AWS·모든 필터 조합에서 통과한 D3 결과로 바꾸지 않는다. 현재판 코드와 6.6.0의 사용자 보고도 합쳐 하나의 버전 정답으로 만들지 않는다. 사용자 목적이 미연결이므로 코드 근거가 늘어도 P-S1 완결 ID는 미확인인 채다.

필요한 다음 실행을 구체화하려면 먼저 동일 분야에서 사전에 적격 판정한 사용자 요구에 연결되는 기능 절을 확보해야 한다. 그 뒤 해당 요구의 판·환경과 조합을 고정해 실행한다. 현재 목적 없는S3 네트워크 배포를 실행해 빈 목적을 사후 보충하지 않는다.

## 감도와 추가 반례

`sensitivity.csv`는 슬롯 수 감도 6행, C 판 미상 완화 1행, 늦은 병합 1행을 포함한다.

| 감도 ID | 기본3자리 | 변경 | 정확히 달라지는 rank·조건 |
| --- | --- | --- | --- |
| P-S1-A-SLOTS / P-S1-C-SLOTS | 1,2,3 | 4자리면 1,2,3,4 | PyPI 원4번만 새 대표. AWS 원5번이 A/C에서도 직접 보이려면 5자리가 필요하다. |
| P-S1-B-SLOTS | 1,5 | 4자리여도 1,5 | 원풀 그룹 두 개에서 소진. 빈 슬롯을 구현 증가로 세지 않는다. |
| P-S1-C-VERSION-ONLY | 1,2,3 | 제품판 미상만 동일 sentinel 처리해도 1,2,3 | 문서 역할이 여전히 미상이므로 단독 유지. 역할까지 같다고 바꾸는 감도는 이번 규칙에 없다. |
| CONTEXT-TROVE-LATE-A-MERGE | A/C 모두 1,2,3 | 원4·6의 같은 URL은 A에서만 병합 | [trove-classifiers 절](https://github.com/pypa/packaging.python.org/blob/5ecbc0db967843e64d55da165b72e773888860c5/source/key_projects.rst) L284–285,L294. 첫3·4·5대표는 그대로이며 6번째 중복 자리까지 가야 멤버 차이가 보인다. 주표본으로 추가하지 않았다. |

첫20 기능 절 중 trove-classifiers의 늦은 중복은 실제 관측한 반례다. 없는 B 효과를 만들기 위해 upstream을 바꾸지 않았다. 또 [build 1.6.1의 비교 절](https://build.pypa.io/en/stable/)은 한 원문이 이미 여러 도구의 역할 차이를 설명한다(PY-E07). 여러 이름을 보는 일과 요구별 두 독립 구현의 완결을 입증하는 일은 다르다. build는 P-S1 밖 맥락이며 진단의 미해결 URI를 복구하지 않는다.

## 반환 카드 제안의 지위

| 카드 형태·원장 | 한 줄 제안 | 깨지는 조건 |
| --- | --- | --- |
| 원문 하나 / PY-E01 | [bandersnatch 8.2.0 매뉴얼](https://bandersnatch.readthedocs.io/en/latest/) — PyPI 미러의 명령·처리 개요; 특정 사용자 요구의 완결은 미판정. | 과거 버전·특정 필터 조합·S3 실서비스를 이 창 하나로 확인하려는 경우. |
| 보완 절 묶음 / PY-E06·10 | [저장소 장](https://bandersnatch.readthedocs.io/en/latest/storage_options.html) + [Compose 소스](https://github.com/pypa/bandersnatch/blob/81a81eb894fa5a014298c04be2c956f620864648/src/bandersnatch_docker_compose/README.md) — 저장·서빙 조합의 검토용 자료; 현행 두 동작 예산 밖이라고 표시. | 원 tree 도착 실패를 소스 복구로 대체하거나 latest 이미지를 고정 제품판으로 오해하는 경우. |
| 구현 둘 / PY-E05·06 | [bandersnatch](https://github.com/pypa/bandersnatch) + [AWS S3](https://aws.amazon.com/s3/) — **독립 대안 둘로 반환 보류**, 미러와 저장 서비스라는 역할 차이를 표시. | 둘을 대체 가능한 동일 기능 구현이라고 세거나 사전 목적 없이 적격 ID를 부여하는 경우. |

차이가 있는 문서 경로는 위 카드에 드러내되 검증된 요구별 효용 차이로 포장하지 않는다. 자연층의 빈 매치와 P-S2의 정원 미달에도 각자의 근거 행을 유지한다.

## 자료 수·재개 조건

공급자 문서 배당에 중복 없는 저작 6개를 기록했다: bandersnatch 매뉴얼, README, S3 개요, Tables 명세, Express 명세, build 매뉴얼. AWS의 세 페이지를 하나의 제품 문서군으로 더 보수적으로 합쳐도 Python 배당 4개는 충족한다. 저장소 장은 매뉴얼과 중복이고, PyPI 설명은 README 재게시이므로 배당에 중복 산입하지 않는다. 릴리스·시험 2저작, 실제 행동시험 실행 0회다. 조회 실패 1개는 직접 자료 수에서 제외했다. 세부 저작 ID는 `observation-summary.json`과 sources 원장에 있다.

실제 첫 5 URL에서 완전한 한 창을 확보한 것은 4개이며 rank4는 347단어의 동일 초기 스냅샷만 확보했다. 같은 canonical URL의 새 8.2.0 창은 별도 저장했다. 이를 수정하려면 당시 7.0.0 반환 창의 잔여 원문 또는 처음부터 고정된 8.2.0판의 동일 예산 재실험이 필요하다. 도구 캐시의 이 상태를 판 없는 C 필드 추론이나 역사적 가용성 주장으로 사용하지 않는다.

다음 최소 조사 우선순위는 (1) 독립적으로 고정한 요구와 일치하는 발행 목록 기능 절 확보, (2) rank4 초기 스냅샷과 -h fragment·Compose 정확 도착의 복구, (3) 필요할 경우 정확한 판의 요구 조건을 검사하는 시험이다. 이 중 첫 항이 해결되지 않으면 문서 수를 더 늘려도 완결 ID·요구별 증감은 판정할 수 없다.
