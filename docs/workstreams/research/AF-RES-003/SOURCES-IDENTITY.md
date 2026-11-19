# AF-RES-003 — 제품·출처·포크·이름 변경의 실제 사례

조사 축: identity/storage. 작성자: 이 과제의 하위 조사자 `identity_cases`.
기준 입력: `chore/workspace-foundation@9d728dfe2c2f3a13d9995b5fdc14a252aeddfdad`의 `AGENTS.md`, `docs/RESEARCH_WORKFLOW.md`, `docs/product/RESEARCH_BRIEF.md`와 부모가 전달한 AF-RES-003 범위.
확인일: 2026-11-19 UTC (한국 2026-11-20). 열람 직후 기록 시각은 실제 clock 기준 `2026-11-19T15:42:43Z`이며, 각 접근의 초 단위 시각은 별도 계측하지 않았다. 아래에는 서로 다른 1차 출처 12개를 기록했다. I01–I11은 본문을 직접 읽은 자료 11개이며, I12는 도구가 재작성 요약을 반환했으므로 직접 원문 열람 수에서 제외한다. 같은 README의 GitHub 화면과 고정 파일 재열람은 한 자료로 센다. API에서 얻은 커밋 메타데이터는 고정 위치 확인이며 추가 연구 자료 수로 세지 않는다.

**읽은 문서의 주장(D1)만 확인했다. 프로그램 실행·서비스 접속 후 기능 시험·마이그레이션·라이선스 적법성 판정은 하지 않았다.** 아래 `same/related/unresolved`는 제품 카탈로그 설계에 대한 연구자 판단이며, 원문이 쓰지 않은 동등성 관계를 검증 사실로 승격하지 않는다.

## 1. 핵심 결론

제품 항목을 합치는 일과 출처 링크를 함께 묶는 일은 별개다. Supabase의 저장소·공식 문서는 동일 제품군을 설명하지만, managed와 self-hosted의 기능은 같지 않다(I04–I06). Paperless의 계승 프로젝트들은 함께 찾아볼 이유가 강하지만 기능 속성을 서로 옮겨도 되는 동일 객체가 아니다(I01–I03). Supabase 내부 GoTrue→Auth는 이름 변경 근거가 있지만, 출발점인 Netlify GoTrue와의 관계는 포크다(I07–I08). 같은 URL 아래 콘텐츠가 앱에서 목록으로 바뀌는 OpenAlternative 사례는 URL 안정성이 대상의 의미 안정성을 보장하지 않음을 보여 준다(I09).

따라서 이 표본에서 필요한 최소 구분은 **어느 대상에 대한 말인지, 그 대상과 다른 대상이 어떤 관계인지, 그 말이 어느 버전·배포 범위에 해당하는지, 어느 출처의 어디에서 언제 읽었는지**다. 이것은 저장 원리의 제안이며 테이블 수나 API 필드 확정이 아니다.

## 2. 직접 읽은 자료 원장

### I01 — 원 Paperless의 보관·포크 안내

- URL: <https://github.com/the-paperless-project/paperless/blob/9b0063c9731f7c5f65b1852cb8caff97f5e40ba4/README.md>
- 확인: 2026-11-19 UTC. D1, 고정 문서.
- 고정 위치: 커밋 `9b0063c9731f7c5f65b1852cb8caff97f5e40ba4`; README `Important news about the future of this project`, `How it Works`, `Important Note`. 커밋 날짜 2021-02-18.
- 확인 내용: 작성자는 저장소를 읽기 전용으로 보관하며 업데이트·기여를 원하는 사람에게 별도 Paperless-ng 포크를 안내한다. 당시 조직 이전은 가능성으로만 언급한다. 문서에는 원본 파일 암호화와 OCR 텍스트 평문 저장을 구별하는 설명이 있다.
- 한계: 작성 당시의 관리·기능 설명이다. 실제 암호화 동작, 현재 구형 배포의 안전성, 포크 간 데이터 이전을 시험하지 않았다. 미래 조직 이전을 완료된 사건으로 읽으면 안 된다.
- 식별에 쓰는 범위: 원 Paperless와 Paperless-ng는 `related: fork`; 옛 제품의 속성을 후계에 자동 복사하지 않을 근거.

### I02 — Paperless-ng의 기능 차이와 ngx 계승 안내

- URL: <https://github.com/jonaswinkler/paperless-ng/blob/3050ed3cb27d0b356ba383ddfc2ceea5fabbf8c8/README.md>
- 확인: 2026-11-19 UTC. D1, 고정 문서.
- 고정 위치: 커밋 `3050ed3cb27d0b356ba383ddfc2ceea5fabbf8c8`; `Archive notice`, `Paperless-ng`, `Migrating from Paperless to Paperless-ng`. 커밋 날짜 2023-01-12.
- 확인 내용: 원 Paperless에서 포크했으며 UI·API 등이 달라졌고 GnuPG 지원을 제거했다고 설명한다. 별도 ngx 저장소를 공동체의 직접 계승·대체 프로젝트로 안내한다.
- 한계: README의 대체 가능 설명은 연구자가 모든 버전 조합을 실제 이전한 증거가 아니다. 원본과 ng 사이의 API·암호화 차이가 명시되므로 이름의 유사성만으로 기능 동일성을 주장할 수 없다.
- 식별에 쓰는 범위: `fork`와 `successor/replacement`를 구별할 수 있다. 세 프로젝트를 한 제품군으로 탐색하도록 묶는 것은 가능하되 구체 제품·버전 경계를 보존한다.

### I03 — Paperless-ngx가 자신을 설명하는 README

- URL: <https://github.com/paperless-ngx/paperless-ngx/blob/4973be8499bc61dc4f791a609d0d31e9ac9ccd41/README.md>
- 확인: 2026-11-19 UTC. D1, 고정 문서.
- 고정 위치: 확인 당시 `dev`의 커밋 `4973be8499bc61dc4f791a609d0d31e9ac9ccd41` (릴리스 버전으로 취급하지 않음); README `Paperless-ngx`, `Getting started`, `Documentation`.
- 확인 내용: Paperless와 Paperless-ng의 공식 후계라고 소개하고 자신의 문서·데모 링크를 제공한다. ng에서 새 컨테이너 이미지로 이전할 수 있다는 안내가 있다.
- 한계: README 링크로 공식 문서의 귀속을 확인했으나 문서 사이트 첫 화면 자체는 이 도구에서 403으로 읽지 못했다. 데모에 로그인하거나 이전 절차를 실행하지 않았다. linked source의 내용까지 읽었다고 세지 않는다.
- 식별에 쓰는 범위: ngx 저장소와 ngx 문서 URL은 같은 제품을 가리키는 서로 다른 출처 역할로 묶을 수 있다. 웹 문서와 제품 자체를 무차별 `same` 관계로 병합하지 않는다.

### I04 — Supabase 저장소의 제품·배포·구성 설명

- URL: <https://github.com/supabase/supabase/blob/4c4112fa1fda81ef36a0f32580f7766e2eca2f9c/README.md>
- 확인: 2026-11-19 UTC. D1, 고정 문서.
- 고정 위치: 커밋 `4c4112fa1fda81ef36a0f32580f7766e2eca2f9c`; README `Documentation`, `How it works`, `Architecture`, `Client libraries`.
- 확인 내용: 공식 문서 URL, hosted 플랫폼, self-hosted와 local development 경로를 구별해 연결한다. 여러 도구의 조합으로 제품을 설명하며 Auth·Realtime·Storage 등의 별도 저장소를 가리킨다. 클라이언트도 개별 외부 시스템용 하위 라이브러리로 나눈다고 설명한다.
- 한계: README 기능 목록은 각 배포 형태의 기능 동등성이나 라이브러리의 독립 실행 성공을 입증하지 않는다. 저장소 하나가 제품의 모든 실행 코드와 운영 기능을 담는다는 결론은 불가하다.
- 식별에 쓰는 범위: 브랜드/플랫폼, 구성 도구, 출처 페이지를 필요한 질문에 따라 구별하되 저장소 개수대로 제품 개수를 정하지 않는다.

### I05 — Supabase self-hosted와 managed 차이

- URL: <https://supabase.com/docs/guides/self-hosting>
- 확인: 2026-11-19 UTC. D1, live 문서.
- 위치·시점: `How self-hosted Supabase differs`, `Not the same as local development`, `Your responsibilities when self-hosting`; 페이지 표시 갱신일 2026-10-19. 웹 열람 위치 L203–232.
- 확인 내용: self-hosted는 단일 프로젝트로 동작하며, managed의 branching·managed backups/PITR·Management API 등 일부 기능을 제공하지 않는다고 설명한다. CLI의 local stack도 self-hosted 운영 배포와 구별한다.
- 한계: 이번 확인 시점의 문서 설명이며 실행이나 계정별 사용권 확인이 아니다. 전체 차이 목록을 영구 계약으로 취급하지 않는다. 이 조사에서는 일부 예만 사용했다.
- 식별에 쓰는 범위: 같은 제품군 안에서도 주장 적용 범위가 필요하다. 세 배포 경로의 설명을 하나의 무조건적 기능 목록으로 합치면 오판한다.

### I06 — Supabase 아키텍처의 구성 도구와 독립성 원칙

- URL: <https://supabase.com/docs/guides/getting-started/architecture>
- 확인: 2026-11-19 UTC. D1, live 문서.
- 위치·시점: `Architecture`, `Studio`, `GoTrue (Auth)`, `PostgREST`, `Product principles`; 페이지 표시 갱신일 2026-11-18. 웹 열람 위치 L199–309.
- 확인 내용: 한 Supabase 프로젝트를 여러 도구의 조합으로 설명하고 각 도구에 문서·소스 링크를 따로 준다. 독립 작동과 통합을 동시에 제품 원칙으로 제시한다. PostgREST는 Postgres를 REST API로 드러내는 별도 서버로 설명된다.
- 한계: 설계 원칙은 구성 요소의 설치 조건·현재 배포 동등성·사용자 환경의 실제 성공을 보증하지 않는다. live 문서와 I04의 소스 스냅샷이 동일한 배포 상태라고 가정하지 않는다.
- 식별에 쓰는 범위: 독립적으로 골라 재사용할 수 있는 부품을 제품의 단순 태그만으로 처리할 때 생기는 손실을 보여 준다. 반대로 모든 API·문서 절을 독립 제품으로 만들 근거는 아니다.

### I07 — Supabase Auth와 Netlify GoTrue의 분기

- URL: <https://github.com/supabase/auth/blob/10ef10789d1ee4fb422b448047e67e3e264c0482/README.md>
- 확인: 2026-11-19 UTC. D1, 고정 문서.
- 고정 위치: 커밋 `10ef10789d1ee4fb422b448047e67e3e264c0482`; README 첫 설명, `Running in production`, `Backward compatibility`.
- 확인 내용: Supabase Auth는 Netlify GoTrue에서 비롯되었지만 기능·능력이 크게 갈라졌다고 명시한다. 서버와 라이브러리 사용을 구별하며 Go 라이브러리 사용 시 API 호환성 보증이 없다고 설명한다.
- 한계: 구체 Netlify 최신 기능과의 전체 diff를 읽거나 두 서버를 실행하지 않았다. 공통 기원은 기능 호환성의 증거가 아니다.
- 식별에 쓰는 범위: Supabase 내부의 옛 이름 GoTrue와 Netlify 제품 GoTrue를 소유자·계보 없이 합치면 오병합이다. 같은 언어라는 이유만으로 서버를 재사용 라이브러리로 분류하는 것도 실패한다.

### I08 — Supabase가 명시한 GoTrue→Auth 이름 변경

- URL: <https://supabase.com/blog/supabase-auth-identity-linking-hooks>
- 확인: 2026-11-19 UTC. D1, 날짜 있는 공식 발표.
- 위치·버전: 2023-12-14 게시; `One more thing…` (웹 L243–246).
- 확인 내용: Netlify GoTrue에서 포크한 뒤 Supabase의 저장소 명칭을 gotrue에서 auth로 변경한다고 설명한다. 당시 v2에 대해 옛·새 JS 패키지 명칭을 지원 기간 동안 같이 쓸 수 있다고 설명한다.
- 한계: 발표 당시 v2의 약속이지 모든 생태계·모든 미래 버전의 별칭 호환성 보증이 아니다. 이 명칭 변경을 Netlify 저장소까지 적용할 근거가 없다.
- 식별에 쓰는 범위: **Supabase 내부 이름 변경은 같은 계보의 이름 이력**, **Netlify→Supabase는 포크 관계**로 별도 해석해야 한다. 이름이 달라졌다는 이유만으로 Supabase의 두 이름에 서로 무관한 제품 항목을 생성하는 과분할도 피한다.

### I09 — OpenAlternative의 동일 저장소 역할 변경

- URL: <https://github.com/piotrkulpinski/open-source-alternatives/blob/156045dde3d74a6bfdad675c13521718ca0e50b5/README.md>
- 확인: 2026-11-19 UTC. D1, 기존 표본의 원문을 다시 직접 읽음.
- 고정 위치: 커밋 `156045dde3d74a6bfdad675c13521718ca0e50b5`; README 첫 `Note`.
- 확인 내용: 저장소를 curated awesome-list로 전환했고 전에 있던 Next.js directory boilerplate는 Dirstarter에서 제공한다고 설명한다.
- 한계: Dirstarter를 열거나 구매·실행하지 않았다. 코드 동일성, 이전 버전의 라이선스, 현재 상품 조건은 미확인이다. 작성자의 이전 안내만으로 `OpenAlternative = Dirstarter`를 확정할 수 없다.
- 식별에 쓰는 범위: 같은 repo URL의 시간별 역할을 구별한다. 현재 목록, 이전 앱 자료, 이동했다고 설명된 코드/상품 사이 관계는 보존하되 완전 동일성은 `unresolved`로 둔다.

### I10 — GitHub 이름 변경과 주소 재사용의 한계

- URL: <https://docs.github.com/en/repositories/creating-and-managing-repositories/renaming-a-repository>
- 확인: 2026-11-19 UTC. D1, live 공식 문서.
- 위치: 이름 변경 설명·Note·Warning (웹 L20–41).
- 확인 내용: 저장소 이름 변경 후 여러 웹/Git 경로는 새 위치로 리다이렉트된다. 프로젝트 사이트와 해당 저장소의 Action 호출에는 예외가 있으며, 옛 이름을 다른 저장소에 다시 쓰면 이전 리다이렉트가 작동하지 않는다고 설명한다.
- 한계: 일반 서비스 동작 설명이다. 이 조사에서는 특정 저장소 이름을 직접 변경하거나 옛 이름 재사용을 재현하지 않았다. 리다이렉트만으로 소프트웨어 제품의 완전한 동일성을 판정할 수 없다.
- 식별에 쓰는 범위: 원래 발견 URL·관측 시점·새 위치·관계 판단 근거를 함께 보존한다. 모든 경로를 현재 canonical URL 하나로 덮어쓰면 과거 자료가 가리킨 대상을 잃는다.

### I11 — 보충: Grafana Agent의 종료·후계 안내

- URL: <https://grafana.com/docs/agent/latest/>
- 확인: 2026-11-19 UTC. D1, live 공식 문서.
- 위치: 상단 Caution, 소개, variant 구별; 화면 표시 `v0.44 (latest)`.
- 확인 내용: Agent의 EOL 시점을 2025-11-01로 설명하며 Static/Flow/Operator 사용자에게 Alloy 이전을 권한다. 한 페이지 안에서 Flow 중심 설명이라는 범위도 밝힌다.
- 한계: 지원 종료라는 공식 설명을 읽었을 뿐 실제 서비스·설치본 상태를 조사하지 않았다. 과거 release cadence 문단도 남아 있어 페이지의 모든 문장을 동일 시점 현재 사실로 읽을 수 없다.
- 식별에 쓰는 범위: 같은 페이지의 소개·현재 종료 안내·과거 릴리스 원칙은 적용 시점이 다르다. 제품 전체와 특정 variant의 범위를 섞으면 후계 관계도 과도하게 일반화된다.

### I12 — 보충: Grafana Alloy의 코드 계승과 전환

- 요청 URL: <https://grafana.com/blog/2024/04/09/grafana-alloy-opentelemetry-collector-with-prometheus-pipelines/>
- 열람 도착 URL: <https://grafana.com/blog/grafana-alloy-opentelemetry-collector-with-prometheus-pipelines/>
- 확인: 2026-11-19 UTC. D1, 공식 발표. 웹 도구가 재작성 요약을 반환한 페이지이므로 세부 원문 표현·발행일의 완전한 재현은 보장하지 않는다.
- 위치: 상단 Note와 `From Agent to Alloy`; 반환 화면 게시 표시는 2024-04-10, 본문 출시/LTS 기준일은 2024-04-09. 둘을 같은 날짜로 정규화하지 않았다.
- 확인 내용: Alloy가 Agent Flow의 구성 요소·코드·개념을 이어받는다고 소개하면서 기존 Agent/Operator의 지원 단계와 전환을 구별한다.
- 한계: 이 원문 반환 범위는 출시 설명이며 모든 Agent variant와 Alloy의 설정·실행 동등성을 검증하지 않는다. 본문이 예상한 미래 EOL과 I11의 현재 종료 안내도 다른 시점의 주장이다.
- 식별에 쓰는 범위: 코드를 이어받았다는 관계와 현재 지원되는 같은 제품이라는 관계를 동일시하지 않는다. 이 보충 사례는 핵심 결론의 단독 근거로 사용하지 않는다.

## 3. 읽기 실패·재열람·검색 경로

| 시도 | 결과와 처리 |
| --- | --- |
| `https://docs.paperless-ngx.com/` open | 403. 본문을 읽었다고 세지 않음. I03의 README에서 문서 링크의 귀속만 확인함 |
| I09 GitHub blob 웹 open | DisabledError. 공개 GitHub 파일 도구로 같은 고정 README를 읽어 I09에 기록함 |
| 각 README의 GitHub repo 화면→고정 파일 | 중복 접근. 원문 수는 문서별 1개로 유지함 |
| `site.supabase.com "gotrue" "renamed" "auth"` | I08 발견 후 본문 직접 열람. 다른 검색 결과는 미열람으로 판단 근거에서 제외 |
| `site.grafana.com "Agent Flow" "renamed" "Alloy"` | 보조 탐색. 검색 결과만 나온 release-notes·discovery.file 페이지는 직접 읽은 자료 수에 포함하지 않음 |

고정 SHA는 공개 GitHub `repos/{owner}/{repo}/commits/{branch}`의 읽기 응답으로 확인한 뒤 그 SHA의 README를 열었다. 최신 브랜치의 다른 코드·PR은 이번 근거 범위가 아니다.

## 4. 같은 실제 사례에 세 저장 원리 적용

여기서 A/B/C는 물리 테이블이 아니라 정보 표현의 원리다. A의 자유문이 충분히 길면 아래 모든 차이를 문장으로 적을 수 있다. 비교 대상은 '가능/불가능한 파일 형식'이 아니라, 짧은 설명만 남겼을 때 어떤 질문을 다시 원문에서 복원해야 하는가다.

| 같은 사례·판정 질문 | A: 링크 + 짧은 설명 | B: 대상과 출처 링크 분리 | C: 주장·근거·적용 범위도 분리 |
| --- | --- | --- | --- |
| ngx 저장소와 문서: 중복 제품인가? (I03) | 두 링크를 두 결과로 보여주거나 한 줄에 함께 적을 수 있다. 후자는 링크 역할을 문장에서 해석해야 한다 | ngx 하나에 repo/docs 역할을 붙이면 탐색 결과 중복을 줄인다 | 이 질문만이라면 C까지 늘릴 이익이 작다. 기능·상태 충돌이 생길 때 추가 |
| Supabase: self-hosted에도 managed backups가 제공되는가? (I04–I06) | 짧은 브랜드 기능 목록으로 합치면 잘못 옮겨진다. 설명에 배포 범위를 매번 써야 한다 | 대상 분리만으로는 충분하지 않다. 같은 제품 항목에 managed/self-hosted 범위가 남아야 한다 | '제공됨/없음'을 해당 배포 범위와 근거 절에 묶으면 충돌처럼 보이는 차이를 설명할 수 있다 |
| Paperless→ng→ngx: 옛 암호화 속성을 후계에 적용할 수 있는가? (I01–I03) | URL별 설명을 모두 읽어야 기능 삭제와 계승을 구별한다 | 별도 대상 + fork/successor 관계로 잘못 합침을 막는다 | 원본의 기능·ng의 제거 설명을 서로 다른 범위로 유지. 마이그레이션 성공은 별도 미확인 |
| Supabase GoTrue→Auth와 Netlify GoTrue: 무엇을 합치나? (I07–I08) | 표시명 GoTrue로 중복 정리하면 포크를 섞는다 | Supabase 내부 이름 이력은 묶고 Netlify와 fork 관계로 연결한다 | 당시 v2 호환 약속을 해당 버전·작성 시점에 묶는다. '모든 이후 버전 호환'으로 확장하지 않음 |
| OpenAlternative: 현재 repo를 앱 코드로 재사용해도 되나? (I09) | 같은 URL의 최신 짧은 설명으로 덮으면 옛 설명의 의미가 사라진다 | 대상/링크 분리로도 시간에 따라 링크가 다르게 설명한 역할은 남겨야 한다 | 고정 README의 현재 목록 설명과 '옛 앱은 이동했다'는 문서 주장을 분리. Dirstarter 동일성/재사용 조건은 보류 |
| Agent/Alloy: 후계이면 같은 실행·지원 조건인가? (I11–I12) | 이름 변경 같은 한마디로 합치기 쉽다 | successor 관계와 variant 범위를 유지하면 제품 구분은 가능 | 출시 시점 예상과 확인 시점 지원 안내를 구분한다. 기능 상속은 주장별로 검토 |

### 질문에 비례한 비용과 조합 조건

- A는 사람이 소수 자료를 직접 읽는 북마크 묶음에 적합하다. 짧은 설명만으로 모든 버전·배포 정보를 반복 관리하려 할 때 갱신 누락이 생긴다. 이것을 곧바로 대형 지식 그래프의 필요성으로 해석하지 않는다.
- B는 같은 제품의 repo/docs·별칭과 포크를 함께 다루는 시점에 이득이 있다. 그러나 '대상이 같음'만으로 모든 속성을 공유하게 하면 Supabase 사례를 해결하지 못한다.
- C는 실제로 서로 다른 근거·시점·범위의 기능 주장이 나타날 때 선택적으로 붙일 수 있다. 모든 마케팅 문장과 문서 절을 별도 주장/개체로 만들어야 하는 것은 아니다. 단순한 공식 문서 링크 하나라면 B 안의 짧은 메모로 충분할 수 있다.
- A→B 전환 때 원래 URL과 문장을 버리지 않고, B→C 전환 때 대상·출처의 기존 참조를 유지하면 재조사가 줄어든다는 것은 설계 가설이다. 이 조사에서 이행 도구나 검색 정확도를 시험하지 않았다.

## 5. 처음 생각을 뒤집는 구체 반례

| 단순 규칙 | 실제 반례 | 바꾼 판단 |
| --- | --- | --- |
| 같은 이름이면 같은 제품 | Netlify GoTrue와 Supabase의 옛 GoTrue는 분기되었다(I07–I08) | 이름은 식별 후보일 뿐. 소유 맥락과 계보 근거를 함께 확인 |
| 이름이 달라지면 새 대상 | Supabase가 gotrue→auth 이름 변경을 직접 설명한다(I08) | 이름 이력을 보존하고 동일 계보로 연결. 옛 참조를 삭제하지 않음 |
| 후계·대체품이면 동일 속성을 상속 | Paperless-ng는 이전 GnuPG 지원을 제거했다(I01–I02) | 후계 관계와 기능 사실을 분리. 호환성은 범위 있는 별도 주장 |
| 같은 URL이면 시간과 무관하게 같은 내용/역할 | OpenAlternative repo가 앱에서 목록으로 바뀌었다(I09) | 주소와 그 시점에 설명한 대상을 구별. 역할 변경 기록 유지 |
| 같은 브랜드의 docs·repo·SaaS를 합치면 정확 | Supabase self-hosted의 기능 차이(I05) | 같은 제품군으로 탐색하더라도 배포 범위 있는 주장은 독립 유지 |
| 각 URL·문서 페이지를 별도 제품으로 만들어야 정확 | ngx README가 공식 문서와 기능 문서로 연결한다(I03) | 같은 대상에 속한 출처 역할을 묶고, 선택할 수 있는 제품/부품과 출처 페이지를 구별 |
| 리다이렉트면 영구 별칭 | GitHub는 옛 이름 재사용으로 리다이렉트가 사라질 수 있다고 설명한다(I10) | 관측 시점의 주소 관계로 남기며 과거 증거를 현재 URL 하나로 덮지 않음 |

## 6. 병합·분리·대체에서 남겨야 할 연결

연구 제안이며 저장 계약 확정이 아니다.

1. **이름 변경 병합:** 이전 표시명·이전 출처 참조·같은 계보로 판단한 원문·판단 시점을 남긴다. Supabase 내부 alias를 Netlify까지 전이하지 않는다.
2. **잘못 합친 대상 분리:** 원래 묶음에 있던 주장을 새로운 대상에 자동 복사하지 않는다. 예컨대 `GoTrue`라는 모호한 원문은 출처를 따라 귀속할 수 있을 때만 옮기고, 출처가 모호하면 보류한다. 옛 항목을 열었을 때 분리 이유와 두 목적지를 찾을 수 있어야 한다.
3. **제품 후계·대체:** 구제품 참조를 삭제하지 않고 fork/successor/replacement 이유를 연결한다. 새 제품 추천과 과거 기록 해석은 다른 질문이다. Paperless의 옛 기능과 당시 조건을 보존한다.
4. **출처 내용의 역할 변경:** URL을 덮어써 옛 주장까지 새 콘텐츠에 귀속시키지 않는다. I09처럼 고정 위치와 읽은 시점을 남기고, 현재 용도와 이전 용도를 구별한다.
5. **과도한 분해 방지:** 독립 선택·재사용·호환성·변경 판단이 없는 문서 페이지는 새 제품으로 만들 필요가 없다. 새 대상으로 나눌 때는 '나눠야만 답할 수 있는 실제 질문'을 먼저 제시한다.

## 7. 남은 불확실성과 답을 바꿀 최소 확인

- Paperless의 실제 마이그레이션 호환성: 선택된 구버전/신버전·표본 입력을 지정한 별도 실행이 필요하다. 이번 식별 결론에는 필요하지 않아 실행하지 않았다.
- Supabase 특정 기능의 self-hosted 가능성: 기능·배포 버전이 정해지면 해당 소스·설정과 공식 문서를 더 좁혀 확인한다. 제품군 전체 기능 동등성을 입증하려는 실행은 범위 밖이다.
- OpenAlternative와 Dirstarter의 코드·상품 동일성: 필요할 때 공개 가능한 Dirstarter 원문, 실제 코드 버전과 제공 조건을 확인해야 한다. 현재 문서 주장만으로 보류를 풀 수 없다.
- 이 연구의 A/B/C가 실제 관리 비용·찾기 정확도를 얼마나 바꾸는지: 같은 소수 사례로 사람이 중복 정리·귀속 복원 과제를 수행한 비교가 필요하다. 이 파일은 그 성능 검증을 했다고 주장하지 않는다.

이 축은 자체 사례 대조만 수행했다. 이 파일 작성자가 자기 판단을 재검토한 것을 독립 검토로 부르지 않는다. 부모의 통합 및 별도 검토 결과는 최종 `RESEARCH.md`/`HANDOFF.md`에서 확인한다.
