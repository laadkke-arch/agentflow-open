# AF-RES-266 자체 검토

| 질문 | 찾아 읽은 원근거와 위치 | 결론을 깰 관측을 실제로 찾은 범위 | 남은 미확인·다음 최소 확인 |
|---|---|---|---|
| Q1 | J1–J3 원 JSON `/info/{name,version}`와 `/urls`, J4 `/meta,/files` 및 전송 헤더 | 실제 네 HTTP 200을 받은 뒤 지명 버전·본문 포맷·SHA를 검사했다. GitHub REST와 다른 도메인의 프록시 403을 별도 실패로 남겼다. | 현 serial은 과거 스냅샷을 대신하지 않는다. 다른 날짜를 주장하려면 당시 원응답 하나를 확보한다. |
| Q2 | J1–J4 83키 및 P6/P7/P8, `parsers.json` M1–M9의 각 인덱스와 태그 | 두 읽기 경로 18/18 일치. 복합 태그 10개에서 5파일만 센다. 2.16, cp313t, macOS arm64를 넣고 판정 경계를 확인했다. | 다른 고객 호스트의 허용 태그는 미확인. 그 인터프리터에서 `packaging.tags.sys_tags()`로 대조한다. |
| Q3 | D-M1/M2/M5/M8/M9, 각 ZIP WHEEL·METADATA·RECORD 및 MD-M* | 전체 SHA와 길이, 원 파일별 값, 248 URL/해시를 5/5 잇는다. M8/M9는 메타데이터 지문이 동일하고 payload 지문은 달라, 메타데이터 전용 조인이 파일을 구분하지 못한다. | 4개 양성의 로컬 실행 미실시. 실제 바이트 재취득은 [재생 명령](replay.md#원파일-재검산)을 사용한다. |
| Q4 | J1–J3 `urls[*].upload_time_iso_8601` 및 GitHub 각 `relative-time/@datetime` | 양성 5/5 발표 전. 1.14.1 late macOS 행에서 82/83 일반화를 반증하고 두 호스트 바이트를 대조했다. 포럼 표시 시간은 원 UTC와 따로 보존했다. | 조회 실패한 REST `published_at`와 첫 공개·삭제·재발행은 미확인. 1.14.1 공지 직전 수집본 또는 저장소 작업 기록이 최소 증거다. |
| Q5 | J1–J4 `core-metadata`, `requires-python`, `yanked`, filename, digest, provenance | 조인 83/83, 공동 필드 불일치 0. 실제 null·편측 키 부재·sdist false를 따로 저장했다. 4셀 공석은 정상 두 응답으로 확정했다. | 현재 조회가 업데이트되면 원배열·serial을 다시 고정하고 키 차이를 재계산한다. |
| Q6 | X-sdist PKG-INFO, X-macos/X-free WHEEL, 1.14.1 `pyproject.toml`, N1/N2 제조사 대상과 링크 행 | 3.13 하한 통과와 wheel 부재, classifier 누락과 M9 실제 존재를 서로 대조했다. Windows/Mac 또는 공통 CDN만으로 Nikon 대상 모델을 고르면 두 행에서 오탐이다. | 소스 빌드·다른 플랫폼·펌웨어 적용 미실시. 필요할 때만 정확 대상 및 당시 기록을 갖춘 별도 시험을 잡는다. |
| Q7 | R*-checks, T-test, wheels-3, T-21409, provenance 404 원응답, 로컬 M9 stdout | exact-tag CI 지문은 0건 확보. 개발 aarch64 실패와 저장된 GitHub Release 파일 해시를 CI 근거와 분리했다. M9의 CPython 3.13.5 GIL import/solve 및 로드된 member 지문 일치, 저장 응답으로 18개 파서 비교와 9셀·83파일을 다시 계산했다. | 당시 동일 파일을 소비한 job·artifact digest 5/5 미확인, 원 결과를 뒤집을 최소 증거는 그중 하나의 시험 성공과 같은 payload 지문이다. 고정 SHA 별도 풀이/저장소 검사는 인계의 영수증을 참조한다. |

## 납품 점검

- RESULT는 지정 6열·9셀, 지정 5열·7비교행으로 시작하며 각각 분모를 명시했다. 마지막 표는 3행이고 원자료와 반전 조건이 있다. 주 인벤토리 4 원응답·83 파일은 결측 0이다. 직접 ZIP wheel 5/5 및 추가 대조 4파일, 로컬 양성 1/1, 당시 동일 파일 CI는 미확인 5/5다.
- `sources.jsonl` 97행 중 직접 자료 30개, 산입 원천 계보 18개다. 산입은 원인덱스 4, 지정 배포물 5, 패키징 8, SciPy 릴리스/CI 11, Nikon 2다. 관측 성공 78행, 접근 실패 14행, 별도로 원 404 provenance 공석 5행이다. 같은 파일의 태그판, 재표현, 미러, 접근 실패 및 표본 밖 배포물은 하한에서 중복 가산하지 않았다.
- 승인된 경로는 `docs/workstreams/research/AF-RES-266/`다. 248의 matrix는 고정 SHA의 근거를 사용했으며 `dot-control.json`은 통합판에서 읽었다. 커밋 범위와 원격 신선도 정확한 검사는 인계 영수증에 있다.
- 자기 검토를 수행했다. 독립 검토와 과거 환경 실행은 미실시로 남긴다. Q7의 정확한 로컬 양성 궤적이 실행 합격 대안이다. 역사적 부재나 CI 성공을 확정하는 문구는 보류했다. [재생](replay.md), [반례 전후](COUNTEREXAMPLES.md), [원자료 원장](sources.jsonl).
