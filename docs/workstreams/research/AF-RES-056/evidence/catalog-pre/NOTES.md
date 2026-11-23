# 공식 목록 사전 복원 기록

관측자: `/root/catalogs` 하위 작업자. 작성한 결과의 독립 검토자가 아니라 카탈로그 복원 담당이다.
이 담당자는 질문 표본·용어 대응을 작성하지 않았고, 구현 목적지·릴리스·실행시험·Bowtie 결과·W3C 구현 보고서를 열지 않았다. 목록 자료 자체에 실린 설명·지원판은 노출됐다.

## 고정판과 본표 입력

| 분야 | 발행 소스 고정판 | 원자료와 출력 | 범위 |
| --- | --- | --- | --- |
| JSON Schema | `1a415f9d36c34fe0eae271c05f86a459746ed00b` | [tooling-data.yaml](https://github.com/json-schema-org/website/blob/1a415f9d36c34fe0eae271c05f86a459746ed00b/data/tooling-data.yaml), `catalog-schema-expanded40.csv` | 원자료 282 tools, 기본 obsolete 제외 211 tools, 분류 중복을 유지한 펼친 게시 행 258, 앞40행/정확 Source URL40 |
| JSON-LD | `f9e9288d7c41db5643386effff1ff2a3fe820237` | [index.yaml](https://github.com/json-ld/json-ld.org/blob/f9e9288d7c41db5643386effff1ff2a3fe820237/index.yaml), `catalog-ld22.csv` | 게시22행/정확 URL22에서 소진. 40개를 만들려고 보고서/생태계 자료를 보충하지 않음 |

두 판은 2021–2024 사용자 요구 당시 카탈로그가 아니라 2026-11-23 확보한 현재 재탐색판이다. GitHub 소스의 commit은 확정했다. 실제 프로덕션 배포 commit은 별도 확인하지 못했다.

## 원순서와 고정 검색 필드

JSON Schema의 [기본 변환 상태](https://github.com/json-schema-org/website/blob/1a415f9d36c34fe0eae271c05f86a459746ed00b/pages/tools/hooks/useToolsTransform.tsx#L49-L61)는 빈 검색·이름 오름차순·toolingTypes 그룹·obsolete 제외·Bowtie 필터 끔이다. 같은 파일의 L242–278은 lowercased name의 JavaScript `localeCompare`, L289–358은 그룹순서를 정한다. 복원은 로컬 Node의 en-US 비교로 실행했고, 초기 렌더의 모든89행과 이름/언어/판/라이선스/헤딩이 일치했다.

본표는 `Load More`를 모두 펼친 발행순서의 첫40행이다. [행 렌더러](https://github.com/json-schema-org/website/blob/1a415f9d36c34fe0eae271c05f86a459746ed00b/pages/tools/components/ToolingTable.tsx#L159-L167)는 초기5행을 보여 준다. 초기5행/그룹만 이어붙인 40행은 원순서의 앞선 게시 항목을 누락하므로 본표로 쓰지 않는다. `catalog-schema-initial-viewport.csv`는 가시성 진단용89행이고, 본표40행을 보기 위해 필요한 목록 준비의 Load More는 한 그룹의1동작이다. 이 목록 준비를 공급자 원문 두 행동에 포함하지 않는 추상화는 루트의 SCOPE에서 별도 고정한다.

검색 대상은 이름·편집자가 명시한 별칭·초기 행에 노출되는 기능 분류/기능 필드다. 실제 명시 별칭은 두 목록 모두 없다. Schema의 분류 헤딩은 기능군을 나타내지만 개별 조건의 충족을 보증하지 않는다. 언어·dialect·license는 검색 동의어로 사용하지 않고 환경 제한의 원자료로만 보존했다. 모달에만 노출되는 description·notes·compliance·upstream 의존 정보는 검색에 넣지 않는다. 카탈로그 자체 검색은 이름만 대상으로 하는 Fuse 검색이며 이 과제의 정규화 L/V 실험과 동일한 검색기가 아니다.

JSON-LD는 [index.liquid L80–90](https://github.com/json-ld/json-ld.org/blob/f9e9288d7c41db5643386effff1ff2a3fe820237/index.liquid#L80-L90)의 카드순서와 각 카드 안 원배열 순서를 따른다. [카드 템플릿](https://github.com/json-ld/json-ld.org/blob/f9e9288d7c41db5643386effff1ff2a3fe820237/_includes/implementation-card.liquid)은 CLI를 언어 카드에서 제외한다. [개별 항목](https://github.com/json-ld/json-ld.org/blob/f9e9288d7c41db5643386effff1ff2a3fe820237/_includes/implementation-item.liquid)은 이름·규격판·일부WIP만 표시한다. 언어/CLI는 소속 분류이며 expand/compact/flatten 기능 필드가 아니다. 이 목록의 검색 입력은 결국 이름뿐이다. 기능 열 부재는 접근 실패가 아니다.

## URL과 행동 모델

Schema 항목은 클릭 시 상세 모달을 연다. [모달 L90–118](https://github.com/json-schema-org/website/blob/1a415f9d36c34fe0eae271c05f86a459746ed00b/pages/tools/components/ToolingDetailModal.tsx#L90-L118)에 Source가 먼저, Homepage가 뒤에 놓인다. 본표는 Source가 있으면 그 정확 URL, 없으면 Homepage를 대표 목적지로 삼는다. Source/Homepage를 서로 다른 독립 구현으로 세지 않는다. 이 데이터셋은 목록을 이미 펼쳐서 목적 링크를 알아낸 상황을 출발점으로 한다. 실제 웹사이트에서 모달까지 여는 사람의 클릭 비용과 공급자 원문 두 행동은 같지 않다.

JSON-LD는 각 항목의 repo href가 직접 링크다. trailing slash·대소문자·http/https를 임의 합치지 않았다. 정확 URL 중복 처리만 허용하며, 이름이나 저장소 소유자에서 동일 엔진을 추정하지 않았다. catalog의 upstream_declared가 빈 배열이면 미상이지 독립 엔진이 증명된 것이 아니다.

## 화면-소스 대조와 한계

`live-page-observation.json`은 직접 연 웹 페이지의 원문 위치와 초기 행을 저장한다. `live-source-comparison.json`은 Schema89/89행, LD22/22행의 순서와 해당 표시필드 일치·차이0을 기록한다. 실제 브라우저 클릭·모달 렌더·Load More 뒤 화면은 수행하지 않았으므로 소스로 복원한 펼친 순서로 보고한다. 이 검산은 공급자 기능 적합성이나 실행 성공을 뜻하지 않는다.

Schema 페이지 파서의 상단에는 0 Tools Found가 있지만 아래89행을 직접 읽었다. 이를 빈 카탈로그로 처리하지 않았다. `ToolingTable.tsx`의 useEffect에서 count를 갱신한다는 코드와도 일치하는 정적/동적 텍스트 차이다.

두 공식 목록 모두 복원 가능하므로 사전 지정한 Bowtie/W3C 구현 보고서 대체판을 사용하지 않았다. Bowtie 코드 endpoint 문자열과 보고서 링크의 존재만 확인했다. 외부 시험 성적은 노출되지 않았다. 목록의 포괄적 conforming 문구를 특정판·옵션·필수조건의 시험 통과로 올리지 않았다.

## 별도 편집 저작 배당

`sources.jsonl`의 필수 목록/별도 편집 규칙4저작 제안은 다음 네 가지다.

| 원장 | 저작 | 분리 이유와 한계 |
| --- | --- | --- |
| CAT002 | Schema 공식 목록 데이터+렌더러 | 같은 목록의 HTML/YAML/여러 컴포넌트는 전체1저작 |
| CAT006 | Schema Tooling Data Document의 독립 JSON Schema 계약 | 제출되는 데이터의 허용 키·필수값·분류 의미를 규정하는 별도 기계판독 규칙. 목록과 같은 편집 생태계라 독립 실험 증거는 아님 |
| CAT007 | Add/Modify Tooling 제출 양식 | 제출자에게 요구하는 필드·수정행위·설명을 정한 별도 편집 규칙. 계약과 공통 필드가 겹침을 공개 |
| CAT010 | JSON-LD 공식 목록+템플릿 | 웹/RDFa/YAML/템플릿은 전체1저작 |

별도 CONTRIBUTING 문서는 추가 맥락으로 읽었지만 필수4배당에 중복 산입하지 않는다. Schema CONTRIBUTING의 implementation 추가 경로는 현재 파일 tree와 불일치하므로 원순서 재현에는 현행 데이터·renderer만 썼다. JSON-LD CONTRIBUTING은 문서 특허·기여자 기록 안내이며 구현의 의미·별칭·분류 검증 규칙은 확인할 수 없다.

## 사전 작업 중 명확화 이력

초기에는 '화면의 처음 보이는40행'을 후보 해석으로 제안했다. 루트는 아직 L/V 매치·목적지 판정을 하지 않은 시점에 'Load More를 펼친 발행순서 첫40행'으로 고정하도록 지시했다. 이에 잠정 viewport40 CSV는 커밋 전에 제거했고, 초기 가시성89행만 별도 진단으로 보존했다. 표본/용어를 후보 결과에 맞춘 변경이 아니다. 이 카탈로그 담당자는 두 해석의 게시 데이터를 읽었지만 root에 후보명·순위를 전하지 않았고, 질문/용어 작성자는 독립 경로에서 작업했다.

소스 metadata의 description·compliance·지원판을 이 담당자가 읽을 수 있었음을 기록한다. root의 사전 용어표와 L/V 선택에 이 숨은 필드를 추가하지 않았다. 목적지 비노출과 카탈로그 metadata 비노출을 혼동하지 않는다.

## 재현과 남은 확인

```bash
python -B docs/workstreams/research/AF-RES-056/evidence/catalog-pre/reconstruct_catalogs.py
```

이 명령은 네트워크를 사용하지 않으며 고정 snapshot에서 CSV를 다시 만든다. 순위 질의·L/V 매칭·후보 기능 판정은 포함하지 않는다. 고정 파일 재열람의 blob SHA 일치는 `fixed-file-rechecks.json`에 보존했다. snapshot 텍스트는 줄끝을 LF로 정규화했으므로 원blob과 byte 동일함을 주장하지 않으며 원blob SHA를 provenance에 별도 기록했다.

남은 최소 확인은 (1) root가 사전 고정한8개 요구의 용어만 사용해 이 두 CSV에서 매칭, (2) 같은 Source-first 규칙으로 실제 도착 URL과500단어/정확 절 창을 기록, (3) 출력창·예산 밖 구현 진실·옵션·제품판을 분리하는 것이다.

