# AF-RES-052 반환 카드와 보류 기준

아래는 연구자가 작성한 **조건부 반환안**이다. 실제 독자가 채택한 수는 측정하지 않았다. 자연층 네 요구의 제목 매칭은 모두 빈 반환이며, D-M1은 본표에 넣지 않는 진단이다. 주소·용도·깨지는 조건을 생략하지 않고, 독립 구현 둘을 확인하지 못한 곳은 카드도 보류한다.

## 차이가 난 경로의 세 반환 형태

| 카드 ID·연결 원장 | 형태 | 설계자에게 보낼 한 줄 | 깨지는 조건·예산 |
| --- | --- | --- | --- |
| K-M1-1 · D-M1-B-P08 / ME-R4-C1 | 원문 한 개 | [remark-stringify 옵션](https://github.com/remarkjs/remark/blob/1146b3a274fc1f4607111e5d6607a3a769a0e89a/packages/remark-stringify/readme.md#L160-L167) — 현재판의 backtick·항상 fence 설정으로 C1을 확인; C2 언어·내용 보존은 이 창에서 미확인. | B의 그룹→원4번은 2동작; A/C는 3자리 밖. 원요청의 literal react-stringify10.0.2로 소급하면 깨진다. |
| K-M1-2 · ME-GOLD-C1/C2 | 보완 절 묶음 | [옵션](https://github.com/remarkjs/remark/blob/1146b3a274fc1f4607111e5d6607a3a769a0e89a/packages/remark-stringify/readme.md#L160-L167) + [handler](https://github.com/syntax-tree/mdast-util-to-markdown/blob/655f117443d99a08cb839765ff7489aa759f72d0/lib/handle/code.js#L20-L72) + [시험](https://github.com/syntax-tree/mdast-util-to-markdown/blob/655f117443d99a08cb839765ff7489aa759f72d0/test/index.js#L794-L979) — 명시한11.0.0/2.0.0·fences=true·backtick 조합의 두 조건을 D2로 연결한다. | 코드·시험은 현재 첫 두 href 경로 밖이다. 실제 설치·실행을 확인한 두 동작 완결 카드로 쓰지 않는다. |
| K-M1-3 · CE02 / ME-R6-C1/C2 | 독립 구현 둘 | **보류** — [원4 serializer](https://github.com/remarkjs/remark/tree/main/packages/remark-stringify)와 [원6 mdast](https://github.com/syntax-tree/mdast)는 각각 실행 부품과 자료 구조 명세이므로 두 대체 구현이 아니다. | 첫6 안의 별개 runtime과 동일판 두 조건 근거가 추가돼야 이 형식을 채택할 수 있다. |
| K-P1-1 · PY-E01 | 원문 한 개 | [bandersnatch 매뉴얼](https://bandersnatch.readthedocs.io/en/latest/) — 관측 머리글8.2.0의 미러링·명령 개요; 사전 사용자 목적과의 적격성은 미판정. | 현재판·개요만으로 과거 필터 조합이나 특정 S3 실행 성공을 보증하면 깨진다. |
| K-P1-2 · PY-E06/08/10 | 보완 절 묶음 | [S3 저장 장](https://bandersnatch.readthedocs.io/en/latest/storage_options.html) + [Compose 고정 소스](https://github.com/pypa/bandersnatch/blob/81a81eb894fa5a014298c04be2c956f620864648/src/bandersnatch_docker_compose/README.md) + [6.6.0 상호작용 보고](https://github.com/pypa/bandersnatch/issues/2059) — 저장·서빙 조합과 판별 한계를 함께 검토한다. | 원 Compose 도착은 실패했고 소스는 별도 획득이다. 보고의6.6.0과 현재8.2.0을 한 판의 성공·실패로 합치지 않는다. |
| K-P1-3 · CE01 / PY-E05/06 | 독립 구현 둘 | **보류** — [bandersnatch](https://github.com/pypa/bandersnatch)와 [AWS S3](https://aws.amazon.com/s3/)는 미러와 저장 서비스의 조합 후보이며, 사전 목적도 연결되지 않았다. | 별도 공급자2를 같은 목적의 독립 대안2로 세는 경우에 깨진다. |

## 빈 풀과 차이가 없는 자리에도 남기는 카드

| 카드 ID·자리 | 반환 상태 | 다음에 필요한 최소 입력 |
| --- | --- | --- |
| K-EMPTY-P-N1 | `P-N1`의 editable·data 조건과 고정 기능명사로 PY-LIST 제목/공식 별칭 무매치. 추천 URL 없음. | 해당 명사/별칭으로 실제 안내되는 발행 절. 일반 빌드 문서를 사후 끼우지 않는다. |
| K-EMPTY-P-N2 | `P-N2`의 README 메타데이터 두 조건에 고정 제목 무매치. setup.py 추가 금지를 만들어 후보를 거르지 않음. | 파일 기반 long_description과 content type을 함께 연결하는 공식 기능 절. |
| K-EMPTY-M-N1 | `M-N1` 자연풀은 빈칸. D-M1의 C1 양성을 이 자리에 옮기지 않음. | 같은 표집 규칙의 기능 절 및 원2022 첨부·패키지 식별. |
| K-EMPTY-M-N2 | `M-N2`의 두 HTML 문맥과 raw entity 조건에 제목 무매치. 유효 렌더링만으로 성공 판정 안 함. | 해당 raw 출력 방향을 명시하는 기능 절과 역사 tuple 근거. |
| K-EMPTY-P-S2 | 첫20 기능 절에서 엄격 C 충돌 자리 미충원. | 발행 목록에 다섯 필드가 모두 명시된 실제 충돌 및 뒤쪽 별개 URL. |
| K-EMPTY-M-S1/S2 | 다섯 편집 범주가 단일 처리 목적의 기능 절이 아니어서 두 자리 미충원. | 발행자가 기능별로 구성한 목록. Official 진단은 정원을 대체하지 않는다. |

## 독자 목적이 바뀌면 대표를 바꿔야 하는 이유

| 독자·질문 | 카드에 반드시 남길 정보 | 이번 조사에서 확인한 오답 |
| --- | --- | --- |
| 설계자 · 어떤 도구라도 이 출력을 만들면 됨 | 입력→출력 방향, 각각의 필수조건, 독립 구현 ID와 호환 조합 | parser, CLI, mdast 명세의 이름 수를 serializer 대안 수로 세기. |
| 사용자 문서 작성자 · 이 버전의 이 방향 | 제품판, 옵션 기본값, 같은 판의 예제·릴리스 충돌 | 2023년 기본값 변경을2022년 literal 패키지에 소급하기. |
| 패키지 유지보수자 · 두 부품을 함께 쓰는 법 | 의존 범위와 실제 설치판을 구별하고 연결·저장·서빙 절을 유지 | 그룹 대표를 눌러 이미 한 동작 쓴 뒤 형제를 여는 것을 총2동작으로 세기; 실제로는 대표→그룹→멤버3동작. |

## 다른 분야에서 같은 원칙을 반증해 보기

| 카드 ID | 한 줄 반환 | 깨지는 조건 |
| --- | --- | --- |
| K-X-1 · X03 | [Inter v3.19 variable 안내](https://github.com/rsms/inter/blob/5fa70f6e8c0ecad97544e19aba2d5062aa8c3e7a/misc/dist/variable.txt#L2-L16) — 한 원문에서 다축/단축 flavor와 이름만 다른 Inter V를 비교. | v4 optical size나 정확 설치 바이너리의 축 계약까지 요구하면 부족. |
| K-X-2 · X04 | [Inter v4 설치·파일](https://github.com/rsms/inter/blob/2ce9119398be143fa289c3e180824db1b7ed803e/misc/dist/help.txt#L13-L44) + [같은 판 CSS](https://github.com/rsms/inter/blob/2ce9119398be143fa289c3e180824db1b7ed803e/misc/dist/inter.css#L1-L20) — weight/optical size 및 upright/italic 파일 조합. | 실제 fvar·브라우저 동작은 미검사. 공개 family명과 내부 설치 이름을 같다고 가정하면 깨진다. |
| K-X-3 · X01/X02 | [1999 합창 track14](https://digital.library.unt.edu/ark:/67531/metadc84597/) + [2010 바리톤 track1](https://digital.library.unt.edu/ark:/67531/metadc89020/) — 같은 Foster 곡의 서로 다른 개별 연주 레코드. | 같은 편곡·음질·재생 접근성을 주장하려면 별도 자료 필요. 소프트웨어 대안 수에는 합산하지 않는다. |

이 제안으로 채택할 수 있는 것은 **확인한 조건·판·문서 역할을 카드에 표시하는 형식**이다. 상류 묶음을 모든 요구의 기본 반환으로 채택하거나 세 자리가 항상 충분하다고 결론낼 근거는 없다.
