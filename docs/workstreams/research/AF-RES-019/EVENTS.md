# 사건 표집 규칙과 출처 후보

## 실행 전 등록

사건을 먼저 찾고 신호값과 무관하게 선별한다. 사건 유형별 8건, 최소 5유형 및 40건, 정확한 시행일 30건, 최소 4생태계, 최대 단일 40%, 최대 단일 발표 조직 2건을 목표로 한다. 하나의 결정이 여러 관련 패키지·릴리스에 퍼지면 최초 이유 변화를 호스트 프로젝트에 한 건만 귀속한다. 조직은 발표 책임 팀의 조직과 알려진 동일 모회사를 함께 확인한다. 별도 라이선스 선택지가 실제로 계속 OSI 승인 조건을 제공하면 원 조건과 범위를 비교한다. 재번복·포크가 있어도 최초 대상의 독립 변화를 증명할 수 있으면 포함 가능하다. 날짜가 불분명하면 기록된 정밀도로만 남긴다.

| 유형 | 일차 원문과 입력 후보 |
| --- | --- |
| (a) 라이선스 | 발표자의 공식 블로그·릴리스 / Terraform, Elasticsearch, MongoDB, Redis, Sentry, CockroachDB, Directus, Graylog, Confluent 생태계 프로젝트 |
| (b) 서비스 종료 | 제작자 종료 안내 또는 운영 기관의 날짜가 있는 FAQ / AF-RES-009의 Google Code Search, Microsoft Academic, Openbase·Kite 후보, Stadia, Firefox Send, Parse, AWS OpsWorks Stacks, Flash Player, Dcoder, JFrog Bintray |
| (c) 기능 제거 | 날짜 있는 릴리스 노트와 버전 고정 문서 / CPython distutils, Django url(), pandas append(), NumPy ndarray.ptp(), Kubernetes dockershim, ReactDOM.render(), ESLint 9 rule context, Ruby 키워드 인자, Rails secrets, clap 4 |
| (d) 중단·아카이브 | 공식 종료/관리 상태 선언, 날짜가 있는 GitHub 아카이브 표기, 유지 정책 / Atom, Brackets, AngularJS, Vue 2, CentOS Linux 8, rkt, Docker Machine, Hystrix, kaniko, DeepSpeech, Ruby Sass, Go dep, gorilla/mux |
| (e) 레지스트리 deprecated | 버전별 npm packument와 유지자 공지 / request, node-sass, react-beautiful-dnd, aws-sdk v2, left-pad, tslint, eslint-loader, rollup-plugin-terser, coffee-script, inflight, abab, har-validator, uuidv4 |
| (f) 이전 뒤 조건 | 권리 변경과 소유 이전을 모두 독립 1차 기록으로 확인할 때 추가. 이미 a–e에 든 동일 결정을 중복 계산하지 않는다. |

최초 원문 후보는 공개 GitHub/GitLab 릴리스·README·이슈(관리자 공지), 공식 프로젝트·조직 사이트의 발표·지원 문서, npm/PyPI/Crates/RubyGems 응답, AF-RES-009 및 AF-RES-015의 고정 출처다. 공개 종료 목록과 검색은 후보 발견에 쓴다. 동일 호스트 상한은 방법 문헌에 적용한다. 권한, 비공개 로그, 우회 경로는 사용하지 않는다.

선택한 후보마다 사건 범위·공지 날짜·유효 날짜를 해당 역할의 기록으로 확인하고, 규칙 불합격·원문 차단·중복 조직·비슷하지만 실제 폐쇄/제거가 아닌 후보는 여기 별도로 기록한다. npm 판의 deprecated 텍스트는 현재 존재를 입증하며 정확한 표시 날짜는 유지자 근거나 시간표가 없으면 미확인이다. 이 문서에 적힌 후보의 신호값은 사전 등록 후에 수집한다.

## 선정 결과와 제외

40건을 고정했다. 다섯 유형 각 8건이고, 시행일이 일 단위인 사건 35/40건이다. npm 15/40건이 가장 큰 생태계다. 유형과 조직, 시행 기준, 공지 날짜 및 그 공백은 사건 원장에 있다. 날짜의 일부 공백은 공개 문서의 갱신·이동과 레지스트리 상태의 가변성에서 온다.

| 후보 | 판정과 이유 | 직접 읽은 기록 |
| --- | --- | --- |
| AngularJS / Go dep / kaniko | 별도 종료·보관 후보. Google 그룹을 Reader·Stadia로 두 건 채웠다. kaniko는 포크 반례 입력이다. | [AngularJS](https://github.com/angular/angular.js) · [Go dep](https://github.com/golang/dep) · [kaniko](https://github.com/GoogleContainerTools/kaniko) |
| gorilla/mux | 현 저장소는 활동 중이다. 아카이브 해제·소유권 변경을 별도 대조할 필요가 있다. | [현재 프로젝트](https://github.com/gorilla/mux) |
| Google Code Search | AF-RES-009 F01의 종료 기록은 후보였다. 당초 게시 주소 재열람에서 도구 오류가 있었으며 동일 조직 상한에 도달했다. | [009 고정 입력](https://github.com/laadkke-arch/agentflow-open/blob/7f627a81199f06da7f7b15f979e7fef25dd17602/docs/workstreams/research/AF-RES-009/FAILURES.md) |
| Parse | 원 공지 주소가 현재 오픈소스 후속 블로그로 이동한다. 시작·종료일을 현재 리디렉션 본문으로 판정하지 않았다. | [원 공지 주소](https://blog.parse.com/announcements/moving-on/) |
| AWS OpsWorks Stacks | AWS 이행 안내는 확인했으나 해당 본문에서 종료일 근거를 고정하지 못했다. | [AWS 이행 안내](https://aws.amazon.com/blogs/mt/migrate-your-aws-opsworks-stacks-to-aws-systems-manager/) |
| Rails 7.2 / clap 4 | 기능 변화 후보. 이 표본은 관련 제거·호환성 변경이 다른 c 유형으로 충족됐다. | [Rails 릴리스](https://github.com/rails/rails/releases/tag/v7.2.0) · [clap 릴리스](https://github.com/clap-rs/clap/releases/tag/v4.0.0) |
| inflight / abab / har-validator / uuidv4 / core-js 일부 판 / rollup-plugin-terser | 레지스트리에서 현재 deprecated 표시를 확인한 대체 후보. 사건군의 기존 직접 판·유지자 근거를 유지했다. | [npm 레지스트리](https://registry.npmjs.org/) |

소유 이전 뒤 조건 변경은 독립 사건 표본으로 세지 않았다. 기존 라이선스와 폐기·포크 범위를 사례별로 다룬다.
