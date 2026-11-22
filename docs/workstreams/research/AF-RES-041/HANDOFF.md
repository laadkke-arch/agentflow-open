# AF-RES-041 · 최종 인계

## 고정 결과와 상태

**결과 SHA: `d610d7b16836c2cadff60edcd46cd394dc220ed6`**

조사·반증·산출물 작성과 네 묶음의 원격 커밋을 마쳤다. **엄격 최초안 인과 완결0/2, 기존 코드로 옮겨도 동일 다섯 접점을 요구한 완결0/2, 같은 기능의 변경·반영2/2**다. 미확인은 인과가 없었다는 판정이 아니다. 정확 제공 원판과 최초 독서→같은 선택 변경의 연결은 후속 조사 대상으로 남긴다.

- 저장소: `laadkke-arch/agentflow-open`
- 작업 브랜치: `work/research-af-res-041`
- 유일한 수정 경로: `docs/workstreams/research/AF-RES-041/`
- 실제 시작 통합 SHA: `333e83c9a46b0c005d22efcccbb5a055b27e904e`
- 계획 당시 SHA: `785880f7b7c380dd49e0e4e6e6d90715a9b27838`
- 고정 의존 입력: `AF-RES-037@68c45d2fb4482850d6a3c29826c43a45ea1dc407`
- 작업 환경·확인 가능한 모델·할당 역할은 `manifest.json`에 기록했다. 요청 역할은 web-pro이며 확인 가능한 세션 표시는 GPT-6 Astra Pro다. 별도 웹 UI 모델 선택은 미확인이다.
- 마지막 세션 점검: **2026-11-23 05:46:16 KST** (`2026-11-22T20:46:16.678783+00:00`), passed.

## 먼저 읽을 파일과 필수 표 위치

| 파일 | 위치·용도 |
| --- | --- |
| [RESULT.md](https://github.com/laadkke-arch/agentflow-open/blob/d610d7b16836c2cadff60edcd46cd394dc220ed6/docs/workstreams/research/AF-RES-041/RESULT.md) | 표1은3–8행(두 사건×최초안/코드4행), 표2는10–13행(조작·반례2행), 마지막 약점표는96–100행(정확히3행). 그 사이에 Q1–Q7, 경쟁 설명, 적용 실패 조건이 있다. |
| [sources.jsonl](https://github.com/laadkke-arch/agentflow-open/blob/d610d7b16836c2cadff60edcd46cd394dc220ed6/docs/workstreams/research/AF-RES-041/sources.jsonl) | 113개 열람 범위·재열람·실패 기록. 고유 산입29저작. URL·판·위치·관측·한계·중복·산입을 구분한다. |
| [judgments.csv](https://github.com/laadkke-arch/agentflow-open/blob/d610d7b16836c2cadff60edcd46cd394dc220ed6/docs/workstreams/research/AF-RES-041/judgments.csv) / [cards.md](https://github.com/laadkke-arch/agentflow-open/blob/d610d7b16836c2cadff60edcd46cd394dc220ed6/docs/workstreams/research/AF-RES-041/cards.md) | 네 판독과 두 카드. 엄격 author_link와 포괄적 author_citation을 분리했다. 카드마다 두 링크·용도·실패 조건·누락 접점이 있다. |
| [SELF_CHECK.md](https://github.com/laadkke-arch/agentflow-open/blob/d610d7b16836c2cadff60edcd46cd394dc220ed6/docs/workstreams/research/AF-RES-041/SELF_CHECK.md) | Q1–Q7 근거·반증·미확인·뒤집을 조건. 같은 작업의 자체 재판독이라고 표시했다. |
| [acceptance-evidence.json](https://github.com/laadkke-arch/agentflow-open/blob/d610d7b16836c2cadff60edcd46cd394dc220ed6/docs/workstreams/research/AF-RES-041/evidence/acceptance-evidence.json) | 49개 관측 수용 조건의 met·확인 단위·분자/분모·파일/행·미충족 이유·최소 재개 자료. 결과 고정 뒤 절차는 이 인계서로 닫는다. |
| frame.csv / chronology.csv / mechanisms.csv | 각각43개 탐색 경로,36개 시간 사건,18개 기능·조작 비교. 기능 행은 사례 분모를 늘리지 않는다. |

## 판단을 바꾼 관측

**B01:** 1996 원문 p248에 이미 Multiple Master 폭 축과 문단 줄바꿈을 결합하는 제안이 있었다. 1997을 최초 남은 제안으로 두지 않았다. Thành2000 p38의 hz 영감과 구현 정보 부재는 같은 진술에 공존한다. 0.12h/0.14f의 정적 소스,2000 level1/2 설명,2001 사용법과 저장 출력은 기능 반영을 뒷받침한다. 그러나 첫 hz 독서와 그 뒤 동일 최초 선택의 변경은 미확인이다. 1996 제안 자체가 첫 독서 전이었다는 증거가 나오면 그 구체적 선택도 원안 후보가 될 수 있다.

**B03:** 0.0.1부터 MusiXTeX 선택을 확인했고 0.1 계열의 단계적 전환을 분리했다. 0.1.22→0.1.23에서는 같은 flat의 본보기 귀속이 Schubert에서 Müller로 바뀌고 함수와 매개변수가 재작성된다. 오른쪽 extent w#9/12→.8 interline#, 왼쪽 extent b#0→1.2 stafflinethickness#, crook_fatness1/4→1/3은 소스 값이며 인쇄 잉크폭 실측이 아니다. 같은 배포 경계의 공변경이지 실제 편집 시각의 동시성을 입증한 것도 아니다. sharp의 수평 획 끝 미채택은 일반 특징에 관한 당대 진술이며 특정 Schubert 원판에서 직접 확인한 거부 사례로 확대하지 않았다.

**원판과 반례:** URW1993의 공인1997 번역 관계를 확인했지만 영어 책자 전체는 미확보·미열람이다. Zapf 원문은 확인한 Nottingham/NTNU 주소의 본문 접근에 실패했다. Karow2015의1992 표기와1993 서지가 엇갈려 원본 간기 확인이 필요하다. Schubert는1988 Dürr 판 계열·BA5635/BA5527 후보와2008쇄 관계까지 좁혔지만 저자 사용판은 미확인이다. 현행 Müller 견본과 후대 Schubert raster를1997 본보기로 대체하지 않았다.

## 충족과 미충족

| 확인 단위 | 결과 |
| --- | --- |
| 고유 외부 1차 저작 최소22 및 단일 배당 | **충족:29**. 인쇄4·악보4·수신10(B01=6/B03=4)·독립 발행/기관4·반례6·추가1. 서로 다른22개만으로도 필수 배당을 충족하는 보수 목록이 있다. |
| 동일 릴리스·번역·미러 중복 제한 | **충족**. 같은 배포의 여러 파일, 중간 배포, 반복·실패·검색 스니펫은 추가 산입하지 않았다. 두 LilyPond 릴리스를 한 진화 계통으로 합쳐도28저작·수신9(B01=6/B03=3). |
| 원장·표·분모·카드·재검산 | **충족**. 검산36항목 통과. CSV4개는 원문 문자열과 일치. 첫 표4행·둘째표2행·마지막약점3행, 카드2개×2링크, 분모2+2를 확인했다. |
| Q1–Q7 정확 위치 재판독 | **수행**. RESULT 초안 뒤 핵심 URL9개를 다시 열어 모두HTTP200·본문을 확인했다. 고유 저작 수에는 추가하지 않았다. 자체 점검이다. |
| 정확한 제공 영어 원판·저자 사용 악보판 | **미충족/미확인**. 번역·서지·현재 견본은 확보했으나 정확 원판의 빈 칸을 대체하지 않는다. |
| 최초 독서→같은 최초 선택 변경의 완결 연결 | **미충족/미확인**. 엄격 최초안0/2와 엄격 코드0/2. 인과 부재의 증명은 아니다. |
| B03 특정 본보기의 같은 glyph와 미채택 특징의 직접 쌍 | **미충족/미확인**. 일반 sharp 특징을 의도적으로 무시한 주석은 확인했으나 정확 사용판과의 쌍은 닫히지 않았다. |
| 역사 프로그램 재실행·당시 동일 입력 출력 재현 | **범위 제외, 실행하지 않음**. 정적 소스·저자 보고·저장 출력 관측을 구분했다. |
| 첫 노출·현재 탐색기의 회수 가능성 | **미확인**. 관측하지 않은 검색 성능이나 일반 채택률을 만들지 않았다. |

수용 JSON의 역사 접점 met=false는 위 미확인을 뜻한다. 그 파일의 `post_commit_conditions` 네 항목은 결과를 커밋하기 전 스냅샷이어서 미실시로 남아 있다. 실제 결과 고정·원격 재열람·세션 점검은 아래 기록으로 완료를 확인하며, 이 파일만 마지막 별도 커밋으로 인계한다. 이를 역사 접점이 충족됐다는 뜻으로 바꾸지 않는다.

## 원격 커밋 묶음

| 묶음 | 원격 SHA | 고정한 범위 |
| --- | --- | --- |
| ① 사전 범위·규칙 | `2021e2f236d56073125d940fafe158d2e6ea5c70` | manifest·SCOPE. 실제 커밋20:08:15UTC가 산입 원문 첫 열람보다 앞선다. |
| ② 판별표·원장·변경 전 | `ec22461ac03b7d7d6cc11a34db0b474dcb23fcd5` | 정확판 후보·원장·원안/기존 코드의 구분. 병행 조사 중 얻은 초기 보강도 보존. |
| ③ 당대 기록·반영·반례 | `45b4aa76809cf023d82a3f286b5eb0041d6c1656` | 정적 코드·조작 비교·연대·독립 반례·통합 CSV. |
| ④ 판정·카드·수용 | `d610d7b16836c2cadff60edcd46cd394dc220ed6` | RESULT·네 판독·두 카드·SELF_CHECK·49조건 수용 원장·최종 원문 재개봉·36항목 검산. |

위 네 묶음은 작업 브랜치의 선형 원격 커밋이다. 후속 수정은 같은 소유 경로 안에만 있고, 기준·사례 분모는 유지했다. 임시 범주 배당과 ED020 산입 제외, 변수 해석 정밀화는 amendments.md와 이전 커밋에 보존했다. dot-control.json은 수정하지 않았다.

## 고정 SHA 재열람

`d610d7b16836c2cadff60edcd46cd394dc220ed6`의 두 파일을 GitHub에서 다시 받아 작업 중 고정한 본문 전체와 대조했다. 확인 시각은 2026-11-22 20:44:54 UTC이다.

| 파일 | 원격 blob SHA | SHA256 | 대조 |
| --- | --- | --- | --- |
| RESULT.md | `61fa01b99ca01af9fa45e96ef74553714ffb3393` | `d5518e6e46838198b5e479d7b566e72a4a308e2a4973acf738b7858e9f5fee44` | 본문 전체 일치 |
| evidence/acceptance-evidence.json | `845065d357c79530d9a1b97a57ba384e5e4b3365` | `c888f7bbe0cfee53edf291df558218471156dadc3bb3b617122e1aa40a8a7672` | 본문 전체 일치 |

RESULT의 첫 표 헤더·마지막 W3행과 수용 JSON의49조건·고유29저작도 고정 파일에서 확인했다. SCOPE v1은 blob `d6ad4b3d8a709749c7cf8c3fc862f2923776fc04`로 그대로다.

## 실제 세션 점검

실행 위치는 저장소 루트, checkout은 결과 SHA다. 입력 manifest와 의존 SHA는 위에 적은 고정본이다.

```sh
python -B -m workbench.session check docs/workstreams/research/AF-RES-041/manifest.json --fetch
```

명령은 exit0으로 끝났다. 아래는 실제 출력의 핵심 필드다. changed_paths 배열55개는 모두 이 작업의 소유 경로에 있었고, 배열의 개수만 요약했다.

```json
{
  "status": "passed",
  "task_id": "af-res-041",
  "freshness": "remote_checked",
  "checked_at": "2026-11-22T20:46:16.678783+00:00",
  "checked_out_commit": "d610d7b16836c2cadff60edcd46cd394dc220ed6",
  "task_base_commit": "333e83c9a46b0c005d22efcccbb5a055b27e904e",
  "integration_commit": "7c49b9bcaf458cd410b7c12b1ce7d03bb5eaebc7",
  "scope_base_commit": "333e83c9a46b0c005d22efcccbb5a055b27e904e",
  "contract_sha256": "19f08ce67f7b9d1914ccf214ac68112f3cefc68c95855c4aac0bbbd3393cd8bc",
  "changed_paths_count": 55,
  "outside_paths": [],
  "unmerged_paths": [],
  "errors": [],
  "boundary": "Git contract and ownership checks; not a new AI chat or product verification",
  "exit_code": 0
}
```

초기20:45:03 점검도 통과했다. 원격 커밋을 가져온 뒤 줄 끝을 정규화했던 CSV6개의 Git stat 상태가 변경으로 표시됐으나, 각 파일의 로컬 바이트와 고정 HEAD 바이트가 완전히 같고 diff도 없음을 확인했다. 같은 바이트를 인덱스에 반영해 상태를 정리했고, 작업트리가 깨끗한 결과 SHA에서 위 명령을 다시 실행해 통과했다. 결과 내용을 바꾸거나 추가 결과 커밋을 만들지 않았다.

이 검사는 Git 계약·소유 범위·의존 신선도 확인이며 제품 동작이나 역사 인과를 검증한 결과가 아니다. 검사 시 최신 통합 SHA는 `7c49b9bcaf458cd410b7c12b1ce7d03bb5eaebc7`였고 계약 fingerprint는 유지됐다.

## 바로 재개할 때의 입력과 명령

기록 형식은 저장소 루트에서 다음 한 명령으로 다시 검사할 수 있다. 이미 커밋된 sources·CSV·table-data·RESULT·SELF_CHECK가 입력이다.

```sh
python -B docs/workstreams/research/AF-RES-041/evidence/validate.py
```

핵심 공개 원문을 다시 받는 정적 명령은 아래다. 입력 URL·tar 멤버·페이지가 스크립트에 고정돼 있고, 결과에는 실제 HTTP상태·시각·해시가 남는다. 이 명령은 역사 프로그램을 빌드하거나 실행하지 않는다.

```sh
"$CODEX_PRIMARY_RUNTIME_PYTHON" -B docs/workstreams/research/AF-RES-041/evidence/reopen-key-sources.py
```

정확 원판의 재개에는 자동 실행으로 대신할 수 없는 입력이 남는다. URW는 Google Books `Ox4jywAACAAJ`의1993·38쪽 레코드에 대응하는 표제·간기 및1992 표기와의 판 관계가 첫 자료다. Zapf는 EPODD6(3)283–288의 원 발행 PDF다. Schubert는 BA5527 IV/14b pp196–218 또는 BA5635의1997 이전 인쇄본, Müller는 FH6064/6065의1997 이전 간기와 flat/double-sharp 쪽이다. IMSLP 후보1014719·1035533은 본문 경로를 시도했으나 접근이 막혔다. 정확한 제공 원본 URL이 확보되지 않은 경우는 미확인으로 두었으며 가짜 실행 주소를 만들지 않았다.

그 다음 최소 행동은 같은 원판을 더 많이 모으는 것이 아니라, 그 판과 구체적 코드 변경을 연결하는 당대 메일·패치 설명을 한 건 찾는 것이다. 수량 조건은 이미 충족했으므로 일반 지침을 추가하는 것만으로 카드 강도를 올리지 않는다.

**색인 제안:** AF-RES-041 | pdfTeX·LilyPond: 영감/출처 명명과 같은 기능 반영은 확인, 최초안·정확판의 인과는 미확인 | 최초안0/2·코드엄격0/2 | RESULT.md·cards.md | 다음 접점은 URW1992/1993 원판과1997 Müller flat 패치 연결.

| 중요한 불일치·약점 | 영향받는 판단과 근거 URL·행 | 다음 최소 조사·첫 자료 | 결과가 달라지는 조건 |
| --- | --- | --- | --- |
| W1 · B01의 영어 원판·1992/1993 판 관계와 최초 독서→최초안 변경 연결이 없음 | [Thành2000 p38·pp117–118](https://www.tug.org/tugboat/tb21-4/tb69thanh.pdf), [1996 p248](https://tug.org/TUGboat/tb17-3/tb52sojk.pdf), [Karow1997 p34](https://www.numdam.org/item/CG_1997___27_34_0.pdf). B01-I의 exact_donor·author_link·change_same_baseline이 **미확인**. | URW Hamburg1993 영어 책자 및 Zapf EPODD6(3)283–288 원판. 이어 1996 제안 전후 Thành/Sojka/Zlatuška 메일·노트에서 첫 독서와 선택 변경을 한 기록으로 연결. | 원판의 규칙과 날짜 있는 사전 대안·독서·동일 선택 변경이 연결되면 최초안 판정을 재검토. 기능 코드만 더 발견되면 상향하지 않음. |
| W2 · B03 사용 악보의 정확 판·쪽과 명시적 변경 이유가 없음 | [0.1.22 L2–5,119–167](https://lilypond.org/download/sources/v0.1/lilypond-0.1.22.tar.gz), [0.1.23 L2–5,114–205](https://lilypond.org/download/sources/v0.1/lilypond-0.1.23.tar.gz), [BA5635 서문 III](https://www.barenreiter.co.uk/prefaces/9790006493296_Innenansicht.pdf). 같은 flat 변화는 참이나 exact_donor·엄격 author_link는 **미확인**. | 1997 이전 BA5635 또는 BA5527 IV/14b pp196–218의 간기·판면, Müller FH6064/6065의 간기와 flat/double-sharp 쪽. 첫 연결 자료는 0.1.22→0.1.23 패치 설명·작성자 메일. | 저자 사용본과 해당 glyph·수정 규칙이 함께 특정되면 코드 인과를 재검토. 최초안 상향에는 별도 사전 설계 기록도 필요. |
| W3 · 보존 코드·후대 저장 출력·현대 견본은 당시 동일 실행을 보장하지 않음 | [Vieth2007 slide11](https://tug.org/~vieth/papers/bachotex2007/tex-history-talk.pdf), [LilyPond2003 Fig5](https://lilypond.gitlab.io/static-files/media/xivcim.pdf), [Fok README L18–46](https://sources.debian.org/src/lilypond/2.24.1-2/debian/README.Debian/). 버전 진본성·동일 출력·형상 보존 범위가 제한됨. | 당시 배포 해시/서명과 같은 입력·font·설정을 포함한 보관 출력. B01은0.14f, B03은0.1.22/23의 해당 flat 표본을 먼저 요청·확인. 역사 실행은 이번 범위 밖. | 인증된 배포·동일 입력 짝이 확보되면 반영 범위를 강화. 출력 불일치가 확인되면 해당 기능 반영 주장부터 축소하되 영감 진술과 혼동하지 않음. |

