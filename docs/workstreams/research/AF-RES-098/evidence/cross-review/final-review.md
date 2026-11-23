# ④ 결과 초안에 대한 별도 AI 검토

검토자 `/root/cross_domain`. 사람 검토가 아니다. MP·PY·GG의 모집/예측 후 판별, root가 작성한 교정·집계·추천 표는 **다른 작성자의 결과에 대한 별도 AI 교차검토**다. 본인이 작성한 Q6의 Cole EPUB·Data Citation Corpus를 RESULT가 옮긴 부분은 **자기 점검**으로만 다루며 독립 검토라고 하지 않는다.

검토 범위는 아직 커밋되지 않은 단계 ④의 `RESULT.md`, `SELF_CHECK.md`, root `lineage.csv`, `predictions.csv`, `sources.jsonl`, `evidence/counts.json` 및 프로젝트 audit/영수증이다. 검토 시 git HEAD와 파일별 SHA는 [final-review.json](final-review.json)에 기록했다. 이 검토는 뒤에 실행할 계약·cloud_check나 GitHub 결과판 재열람을 대신하지 않는다.

## 결론과 실제로 고친 두 항목

**아래 두 정정을 작업 트리에서 확인한 뒤, 이번 범위의 내용 검토를 통과로 판정한다.** 고정 12자리·사전 6예측·P/U/G 결론과 추천 대상은 바뀌지 않는다. 재현 문서·검사 영수증·최종 인계 등 완료 절차는 아직 별도다.

| 발견한 불일치 | 직접 확인한 근거 | 작업자가 반영한 정정 |
|---|---|---|
| 동일 주 본문 중복 산입 | MP2 양판 `<article class="bd-article" role="main">` 전체가 **10,598B, SHA256 `36228f1b3a2a2e745bfe6d9d3d0743a1d8dfb569369006bbb2f51026dce8a393`**로 동일했다. PY에서는 wrapper 차이만 있는 같은 본문을 합쳤지만 MP2 새 본문은 산입돼 있었다. MP1도 실행시간 자동 표기만 달랐다. | 두 MP 새 본문의 경로·전체 SHA·판별 자리는 유지하고 자료 수만 보수적으로 제외. **164 원장 행/104 고유/20 본문 → 164/102/18**. 주 선정 사례만의 고유 본문은 **8**이며, 전체 실제 읽은 본문 **18**과 혼동하지 않게 SELF_CHECK를 정정했다. |
| 협업 전체의 첫 새 본문/그림 시각 | 종전 19:46:29는 Matplotlib 요청에 해당한다. CPython 새 HTML은 **19:46:14.413029Z**, 새 PNG는 **19:46:14.414533Z**로 더 빨랐다. GG까지 포함한 세 프로젝트의 실제 본문/PNG 영수증을 비교했다. | RESULT·SELF_CHECK·checkpoints에 CPython의 정확한 최소 시각과 정정 사유를 반영했다. 두 시각 모두 봉인 커밋 **19:45:38Z 뒤**이므로 예측 선후 결론은 유지된다. |

자료 수 정정은 원래 읽지 않은 자료를 추가하거나 사례를 교체하는 방식으로 해결하지 않았다. 기존 읽은 자료에 더 보수적인 같은 저작 기준을 적용한 것이다.

### 본문 중복의 정확한 근거

| 대상 | 이전판 main article | 다음판 main article | 비교 |
|---|---|---|---|
| MP1 | L1019–1063, 8,975B, SHA256 `4e5a0d78f371fbdfc083084fbf27f55bc6da7f36bd54df288c3ea38759791e6d` | 같은 행 범위, 8,976B, SHA256 `874cf09b02dfc1cd4b70087c8b13150084240ccbef3015bf0220a0afe7ff9ffd` | 차이는 `sphx-glr-timing`의 7.524→10.212초뿐. 해당 자동 생성 문단을 제거하면 바이트 동일. 실행시간이 실제 자원별 생성 job의 증명이 되지는 않는다. |
| MP2 | L1019–1093, 10,598B, SHA256 `36228f1b3a2a2e745bfe6d9d3d0743a1d8dfb569369006bbb2f51026dce8a393` | 같은 행 범위·길이·SHA | main article 전체 바이트 동일. |

위 비교에 사용한 원본 캐시는 각각 기존 원장의 전체 HTML SHA와 일치함을 먼저 검산했다. 두 이전판은 [발행판 410d838…의 MP1](https://raw.githubusercontent.com/matplotlib/matplotlib.github.com/410d8388303fab638bbedbd1d2eace0e5efb0de9/3.7.0/gallery/animation/animation_demo.html), [MP2](https://raw.githubusercontent.com/matplotlib/matplotlib.github.com/410d8388303fab638bbedbd1d2eace0e5efb0de9/3.7.0/gallery/animation/pause_resume.html), 다음판은 [발행판 dbd81bd…의 MP1](https://raw.githubusercontent.com/matplotlib/matplotlib.github.com/dbd81bd88621dbfee4c0da45e62a5aeb5722378c/3.7.1/gallery/animation/animation_demo.html), [MP2](https://raw.githubusercontent.com/matplotlib/matplotlib.github.com/dbd81bd88621dbfee4c0da45e62a5aeb5722378c/3.7.1/gallery/animation/pause_resume.html)다. 원문 전체를 검토 산출물에 복제하지 않았다.

ggplot2 홈페이지 양판도 같은 문제가 있는지 확인했다. main 영역은 8,285B→8,278B로 달랐으며 도움말의 실제 대상 URL이 `community.rstudio.com`에서 `forum.posit.co`로 바뀌었다. 이를 MP2의 wrapper만 다른 동일 본문과 혼동하지 않았다.

## 필수 세 표·12자리·분모의 대조

| 검사 | 관측 | 결과 |
|---|---|---|
| RESULT의 첫 세 표 | 모집/예측 **6행**, 판별 **12행**, 목적별 반환 **7행** | 순서·자리 수 일치 |
| 판별 표 ↔ root lineage | 12행의 case/version, 본문 URI, literal ref, payload URL·SHA·길이, 발행 기록 URL, P/U/G를 모두 비교 | 불일치 0 |
| root lineage ↔ 프로젝트 원 증거 | 12행 각각의 body SHA 및 payload URL·SHA·길이를 MP/PY/GG audit와 대조 | 12/12 일치 |
| 상대 URI 해석 | 모든 root lineage 행에서 base URI + literal reference가 기록된 payload URL과 일치 | 12/12 일치 |
| 사전 예측 ↔ 다음판 U | MP1/MP2/PY1/PY2/GG1/GG2의 YES와 실제 YES 대응 | 참 6, 확인 가능 분모 6 |
| 세 판정축 | P=YES 12/12, U=YES 12/12, G=UNKNOWN 12/12 | 표·CSV·counts의 값 일치 |
| SOURCE 집계 | 164행/102산입, 전체 같은 SHA의 산입 중복 0, 산입 행의 요구 구체 필드 빈칸 0 | 수정 집계와 일치 |
| Q별 자기 점검 | Q1~Q7 각각 1행에 답·실제 URL/절·반례 탐색·다음 최소 확인 존재 | 7/7 |
| 마지막 약점 표 | RESULT 마지막 콘텐츠가 정확히 세 데이터 행의 약점/다음 입력/결론 변경 조건 표 | 충족 |

독립 산술 재계산은 본문 **18**, 원 그림·데이터 payload **17**, 발행/빌드/목록 **48**, EPUB 규격·실물 **3**, 데이터 규칙·레코드 **6**을 확인했다. 주 선정 사례만의 본문은 **8**, 주 `src` payload는 **10**이다. 실제 읽은 선행 제외 예제 본문을 포함한 전체 18이 본문 최소 10을 충족한다. **주 선정 12판별 자리와 고유 저작 수가 다른 것**을 최종 문서가 명시한다.

이전 검토에서 지적했던 PY2 500×322 오기는 500×320으로 명시 정정돼 있고, GG의 빈 claim 세 행이 채워졌다. 같은 GG source/workflow·네 위치의 같은 정적 그림은 한 자료로 산입되며 빈 Actions 응답과 실패는 제외됐다. 원장 수는 확인했지만 그것을 102개의 독립 실험으로 부르지 않는 제한도 적절하다.

## 새 판 열람 시각을 세 프로젝트에서 재계산

| 프로젝트 | 최초 새 예제 HTML | 최초 새 PNG |
|---|---|---|
| CPython | 2026-11-23T19:46:14.413029Z · [logging.html](https://docs.python.org/release/3.12.1/howto/logging.html) | 19:46:14.414533Z · [logging_flow.png](https://docs.python.org/release/3.12.1/_images/logging_flow.png) |
| Matplotlib | 19:46:29.946119Z · dbd81bd…/3.7.1/gallery/animation/animation_demo.html | 19:46:35.788302Z · dbd81bd…/3.7.1/_images/sphx_glr_animation_demo_001.png |
| ggplot2 | 19:47:06.031369Z · 3ab6b4…/reference/aes.html | 19:47:06.035191Z · 3ab6b4…/reference/aes-1.png |

전체 URL과 영수증 UTC는 final-review.json에 있다. source R/.py, build rule, 태그·트리 조회를 이 ‘최초 실제 새 본문/PNG’ 비교에 섞지 않았다. 이는 남은 영수증에 대한 검토이고 미기록 사전 지식을 외부 맹검으로 배제한 실험은 아니다.

## 추천 링크와 교정 원문 재열람

이번 최종 검토는 광범위한 신규 조사를 반복하지 않고 의심이 남은 네 URL만 직접 다시 받았다. 네 응답 모두 200이며 이 재열람을 자료 최소 개수에 추가하지 않았다.

- **MP2 현재 표시용 주소:** [3.7.1 pause_resume 본문](https://matplotlib.org/3.7.1/gallery/animation/pause_resume.html)은 HTML 105,244B, SHA256 `8a8df90107b7185d88cc26e94b33916fdf9e1f17551b289119f237d548d98073`였다. 정확 anchor가 있으며 line 1077의 Download Python source href는 추천한 고정 `.py`의 상대 경로와 같다. live 페이지의 전체 SHA가 최초 발행 HTML과 같다고 주장하지 않았다.
- **MP2 고정 실행 입력:** [고정 `.py`](https://raw.githubusercontent.com/matplotlib/matplotlib.github.com/dbd81bd88621dbfee4c0da45e62a5aeb5722378c/3.7.1/_downloads/abf43385578cd8f5bfcc32069e27209f/pause_resume.py)는 1,694B, SHA256 `78db7b586deb6c8accc14ce400c52bc69379aeebf4c444d8adbae17b933fb188`로 기존 tag/download 대조와 일치한다. 프로그램은 실행하지 않았다.
- **asciicast 이전 절:** [a79eac…의 실제 articles 본문](https://raw.githubusercontent.com/r-lib/asciicast/a79eac83fa8ef967ff3d4da9bea1d646291cccb6/articles/asciicast-demo.html#using-svg-files)은 SHA256 `95e48e9722cfe55eea64adca4b9d0e062eba997355323c2b080aeb254bfecc94`다. enclosing div 범위는 L140–161, img 절대행은 **150·160**이다.
- **asciicast 다음 절:** [92fecb…의 실제 articles 본문](https://raw.githubusercontent.com/r-lib/asciicast/92fecbc0ce019cc03086d5fc3f5b9e1a788a84c1/articles/asciicast-demo.html#using-svg-files)은 SHA256 `c812426f5a97f8361e64a7a3beb8a35d5dde4bd2270b70dc1f1567080471ca0c`다. L169–209에서 img/script/inline SVG/data URI가 각각 **0**이다. 잘못된 index 주소가 아닌 실제 articles 주소가 반환 표에 들어 있다.

마지막 두 검사는 root의 수정 파서를 그대로 실행한 것이 아니라 별도 추출·HTMLParser 속성 판독으로 확인했다. 파서 내부 `offset`에 손대지 않았다. 두 고정판의 본문 SHA·절 경계·2/0 판정은 기존 증거와 일치한다. 페이지 전역의 모든 가능 동작 또는 사이트 전체의 이미지 부재를 주장하지 않는 한계도 적절하다.

PY 반환 본문·PNG, GG 역사적 본문·PNG, MP 발행자용 본문·PNG·배포 commit 주소는 12행 원 증거와 정확히 대응한다. raw GitHub HTML은 과거 렌더 사이트와 구별한다. Corpus content 주소는 향후 실제 다운로드에 필요한 입력으로 제시되고, 이미 ZIP을 전부 받았다는 주장으로 표시되지 않는다.

## 추론·범위의 검토

모든 주 예측이 양성이므로 실제 음성 분모 0이며 특이도·삭제/이름 변경 탐지 성능을 산출하지 않는 판단이 맞다. 상속 asciicast는 별도 교정 1사건이고 주 여섯 쌍에 합치지 않는다. 이름 변경·동일 바이트를 못 찾은 결과는 조사한 GG 1,285 경로와 PY 두 파일 이력에 한정돼 있다.

P/U를 긍정하고 G를 유보한 이유도 일관한다. 같은 해시, Software 문자열, 배포 commit, 빌드 규칙, 존재하는 캐시 기능을 특정 실행의 생성 증거로 바꾸지 않는다. MP의 PNG 메타데이터만 변경과 GG의 실제 픽셀 변경을 분리하고, 정적 참조/복사 규칙에 따른 재사용의 긍정과 생성 실행 미확인을 함께 보존한다. 실행할 개발자에게 `.py`를 주면서 런타임 동작 미검증을 유지하는 반환도 증거 범위에 맞다.

비용은 단계 ②의 3+1+3=**7 논리 접근**, 응답 바이트 합계 **14,522,038B**로 영수증에서 재계산했다. 주 검증 **28 URL**은 12본문+12주src+4srcset 주소이며 전체 요청 회차나 고유 저작 수가 아니다. 두 비용 단위를 사람 클릭·시간으로 환산하지 않는다.

후속 수정으로 첫 세 필수 표 뒤에 추가된 여섯 쌍별 예측/성패/비용 표도 다시 확인했다. MP1·MP2는 각각 HTML2+src2+srcset2=6, PY1·PY2·GG1·GG2는 각각 HTML2+PNG2=4여서 6+6+4+4+4+4=28이다. PY의 ZIP 두 개는 두 사례가 공유하며 28에 중복 합산하지 않는다. 이 추가 표로 첫 세 필수 표의 6/12/7행이나 마지막 정확히 세 약점 행은 바뀌지 않았다.

Q6 전재의 자기 점검에서는 EPUB container/OPF/XHTML/JPEG 관계, 두 패키지에서 이미지 9/9 동일, OPF modified와 발행일의 비동일성, Corpus 정확 버전 DOI와 concept의 실제 도착 차이가 원 보고서와 일치한다. 대용량 ZIP을 받지 않았고 MD5는 발행 목록 선언이라는 제한도 보존됐다. 이 문단은 독립 검증 판정을 늘리는 데 쓰지 않는다.

## 아직 별도로 완료할 절차

첫 검토 스냅샷 때 `reproduce.md`, `source-count-review.md`, `validation.json`은 연결돼 있으나 아직 없었다. 후속 확인에서 `source-count-review.md/json`과 `reproduce.md`가 생성됐고 직접 읽었다. 164/102·본문18·주본문8, 28 URL과 전체 접근 하한의 구별, 고정판/깨끗한 작업 사본의 검사, 읽기 전용 모드와 선택적 네트워크 재검사의 구별이 유지된다. 이 final-review 파일도 생성했다. 최종 스냅샷에서 RESULT/SELF_CHECK의 미작성 연결은 **검사 후 생성할 `validation.json`만** 남았다.

재현 문서의 최초 Corpus 명령에는 `md5sum --check` 실패 뒤 `wc -c` 성공으로 전체 종료값이 0이 될 수 있는 문제가 있었다. 이를 root에 알렸고 최종 문서에서 전체 다운로드/검사 예시를 `set -eu`가 있는 subshell로 감싸 curl·MD5 실패가 전파되도록 고친 것을 확인했다. 대용량 ZIP을 내려받거나 MD5를 실행한 것은 아니다. 이 작은 실행 입력 정정은 두 과학 데이터 레코드에 관한 현재의 미검증 판정을 바꾸지 않는다.

`validation.json`은 결과판 커밋 뒤에 실제 실행을 기록할 예정이므로 선기입하지 않는 것이 맞다. 검토 자체를 이유로 계약 검사나 원격 결과판 확인이 이미 끝났다고 표시하지 않는다.

결과판 커밋 후 실제 `check --fetch`·`cloud_check --fetch-contract --require-clean`의 대상 SHA·종료값·범위·개별 검사 skip 여부, GitHub의 필수 표·원 증거·재현 절차 재열람, 마지막 HANDOFF 단독 커밋이 필요하다. 이번 내용 검토가 기록한 두 정정은 반영됐으며, 해당 후속 실행 결과를 미리 통과 처리하지 않았다.
