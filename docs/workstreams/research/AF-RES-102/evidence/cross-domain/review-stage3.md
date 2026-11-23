# Stage 3 독립 AI 검토

**판정: 주 표본 8쌍의 U=YES와 G=미확인은 직접 근거에 맞는다. 신규 자료 수에서는 AF-RES-098과 겹치는 GG 5행을 제외해야 한다. root가 이 조정을 채택했으며 최종 병합판 적용 여부는 후속 검토 대상으로 남긴다.**

검토자는 두 프로젝트 작성자·root와 별도인 `/root/cross_domain` AI 에이전트다. 자기 작성 Q7은 독립 검토하지 않았다. 사람 검토도 아니다. 검토 시점의 입력 파일과 직접 읽은 캐시·영수증 **경로 및 SHA-256**, 재계산한 표, 상속 자료의 정확한 ID·URL·지문은 [review-stage3.json](review-stage3.json)에 있다. 작성 중 파일이 바뀌어도 이번 판정 대상을 구별하도록 입력 바이트를 먼저 고정했다.

## 주 판독·반환 검증

| 별도 확인 | 결과와 한계 |
|---|---|
| 16개 실제 판 자리의 절 경계 | 별도 HTMLParser로 재계산. GG는 `ref-examples` 제목을 담는 div의 끝, MP는 해당 section의 일치하는 닫힘 경계까지 확인. 선언 범위와 일치 |
| 첫 설명 자원·대체 표현 | 모든 주 절에서 첫 img의 src, MP의 2x srcset, base·picture·source·script·SVG·object·embed·iframe·canvas·data URI를 다시 확인. 첫 자원에 연결된 실제 PNG **24개**의 해시·형식·크기·Git blob이 고정 발행 tree와 모두 일치 |
| P와 U | payload의 발행 포함과 정확 절의 참조를 별도로 확인. 주 표본에서는 legacy 경로도 남고 실제 첫 자원과 같지만, 두 필드의 정의를 합치지 않음 |
| 목적의 계속 사용 | 아래 사례별 판독으로 확인. 이름·해시 일치만으로 U를 판정하지 않음 |
| G | 실제 16자리 모두 미확인 유지가 타당. 실행·출력 digest의 직접 연결이 없으며, 빈 job 검색 결과는 생성하지 않았다는 증거가 아님 |
| 읽기용 MP 링크 | root HTTP 영수증에서 전체 HTML 4/4 바이트 불일치를 실패로 보존. 이후 같은 정확 절의 텍스트·모든 img 속성 4/4 일치와 src·2x payload **8/8** 고정판 일치를 따로 확인. 브라우저 실행을 입증하지 않음 |

검토자는 24개 payload를 독립적으로 바이트·형식·tree 대조했다. 그중 **MP-C1 양판 및 GG-C2 양판의 네 이미지는 직접 표시해 보았다.** 나머지 그림을 별도로 모두 눈으로 보았다고 주장하지 않는다. 모든 주 사례의 본문·대응 소스와 첫 참조는 직접 다시 읽었다.

| 사례 | 의미 판독 |
|---|---|
| GG-G1 `expansion` | `mtcars` cylinder 빈도 막대의 아래 여백 0·위 여백 0.1 설정이 양판 첫 예제에 유지됨 |
| GG-G2 `geom_count` | 첫 그림은 양판 모두 `geom_point` 비교 기준 산점도. 두 번째 `geom_count` 결과로 논리 단위를 바꾸지 않음 |
| GG-C1 `annotation_custom` | 빈 패널에 무한 범위의 `roundrectGrob`를 넣는 첫 목적이 유지됨 |
| GG-C2 `geom_histogram` | 첫 코드는 양판 모두 `diamonds` carat의 기본 30-bin histogram. 실제 PNG의 axes와 histogram 목적을 확인했으며 숫자 출력 전체가 같다고 주장하지 않음 |
| MP-G1 `demo_imagegrid_aspect` | 동일 배포 소스와 실제 절·첫 그림·2x 참조가 ImageGrid aspect 목적의 계속 사용을 뒷받침함 |
| MP-G2 `demo_colorbar_with_axes_divider` | 동일 배포 소스의 right/top colorbar와 눈금 배치 목적이 계속됨 |
| MP-C1 `demo_axes_hbox_divider` | 동일 높이를 맞추는 HBox 목적 유지. 옛 그림 안 설명 상자가 새 본문으로 이동했고 두 번째 VBox 그림이 추가됨. 제목·앵커 변경은 예제 삭제가 아님 |
| MP-C2 `inset_locator_demo` | 첫 inset_axes의 절대·상대 크기·loc·borderpad 목적 유지. docstring을 제외한 실행 AST도 양판 같음 |

MP-C1의 옛 `#hboxdivider-demo`는 새 전체 HTML의 ID 목록에 없고 실제 `#hboxdivider-and-vboxdivider-demo`가 있다. 공통 생성 source anchor도 남아 있다. 저자 변경 commit `8ecd60dc48e8767282656c8633415fda1be8beeb`의 해당 파일 patch를 직접 읽어 HBox 코드의 유지·정리와 VBox 추가를 확인했다. 그 commit의 **author date는 2022-09-11, committer date는 2022-10-17**이다. 원장의 10월 17일을 원저자 작성 시각으로 표시하지 않아야 한다.

## 봉인 순서

원격 2단계 검증 경계는 **2026-11-23 22:07:47.803 UTC**다. 응답 완료 시각만 보지 않고 수집 코드의 UTC 의미와 영수증을 함께 읽었다.

| 프로젝트 | 가장 빠른 새 의미 자료 요청 시작 | 검토한 관련 영수증 | 경계 이전·동시 요청 |
|---|---|---:|---:|
| GG | **22:08:32.363481**, `expansion` 본문. 해당 응답 완료 22:08:38.731253 | 74 | 0 |
| MP | **22:08:40.563576**, `demo_imagegrid_aspect` 본문. fetch의 `utc`는 urlopen 이전 기록 | 83 | 0 |

GG audit의 `first_new_body_utc=22:08:38.727319`는 가장 빠른 응답 완료다. 요청 시작과 다른 지표이며 둘 다 원격 봉인 뒤다. 별도 연구자의 이 검토는 네트워크 요청을 새로 하지 않았다. 보존되지 않은 행동까지 감시했다는 주장은 하지 않는다.

## 보조 탐색과 반례

GG 20개와 MP 20개의 보조 사례 ID·페이지는 각각 2단계에 고정한 순서와 정확히 일치한다. 주 혼동표에는 넣지 않았다. 모집틀 첫 40개 밖을 조사한 결과로 확대하지 않는다.

`GG-S13 coord_flip`의 사전 목적은 **다이아몬드 가격 boxplot의 수평 배치**다. 새 첫 블록은 aesthetics를 바꾸는 권장 방식으로 이 목적을 계속 충족한다. 옛 `coord_flip()` 기법을 찾는 독자는 새 Examples **L145–149의 두 번째 블록**을 봐야 한다. 저자 설명이 같은 plot을 만드는 관계를 명시한다. 실제 새 첫·둘째 PNG의 SHA-256은 같지만 두 코드 기법은 다르다. 옛 경로는 남아 있고 양판 PNG 바이트는 달라졌으므로 이를 정확한 유형② 또는③으로 세면 안 된다. 보고서의 유형④·근접 사례 구분은 타당하다.

## 혼동표와 분모

예측 CSV와 **새 판 U 한 자리씩만** 결합해 독립 재계산했다. 옛 판 자리나 보조 예제를 분모에 넣지 않았다.

| 프로젝트·층 | TP | FP | FN | TN | 유보 | 공석 | 실제 양성 | 실제 음성 | FNR | FPR |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| GG 일반 | 2 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0/2 | 산출 불가 0/0 |
| GG 옛 자원 없음 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 산출 불가 0/0 | 산출 불가 0/0 |
| GG 경로 잔류·소스 변경 | 2 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0/2 | 산출 불가 0/0 |
| MP 일반 | 2 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0/2 | 산출 불가 0/0 |
| MP 옛 자원 없음 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 산출 불가 0/0 | 산출 불가 0/0 |
| MP 경로 잔류·소스 변경 | 2 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0/2 | 산출 불가 0/0 |

C층은 경로 잔류라는 선정 조건 때문에 예측 YES만 나온다. 그 층의 FNR 0/2는 없어진 경로의 후계를 얼마나 놓치는지 평가하지 못한다. 전체 사이트의 일반 링크 오류율로 합산할 수 없다. MP 별도 `counts.json`은 이 검토 시점에 없었으므로 작성자의 `audit.main_summary`와 위 독립 계산을 사용했다. root 최종 counts는 후속 확인 대상이다.

## 필요한 자료 수 조정

AF-RES-098 결과 commit `846aa7b644bda67ef2551c3f4fb1ec6f5de9484d`의 sources 원장을 직접 열어 대조했다. 현재 GG `countable=true` 5행은 다음과 겹친다. 정확한 원주소·고정주소·양쪽 지문은 JSON의 `inherited_source_exclusions`에 모두 기록했다.

| 현재 ID | 098 ID | 대조 결과 | 최종 처리 |
|---|---|---|---|
| GG-S3-126 | GG-OLD-WORKFLOW | 같은 `pkgdown.yaml` 저작의 다른 판 | 신규 최소량 제외 |
| GG-S3-143 | DEPLOY-ACTION-4-4-1 | 같은 deploy action README의 다른 판 | 신규 최소량 제외 |
| GG-S3-145 | PKGDOWN-2.0.7-build_R | 같은 pkgdown `R/build.R` 저작의 다른 판 | 신규 최소량 제외 |
| GG-S3-146 | PKGDOWN-2.0.7-build-github | **바이트 지문까지 동일** | 신규 최소량 제외 |
| GG-S3-147 | PKGDOWN-2.0.7-build-reference_R | **바이트 지문까지 동일** | 신규 최소량 제외 |

root가 5개 모두 제외하는 보수 처리를 채택했다. 작성자 원장 GG57은 당시 기록으로 보존하고 최종 병합에서 **GG52 + MP54 = 두 프로젝트106개**로 조정한다. 두 프로젝트의 범주 합은 본문46·자원45·발행/변경/릴리스/규칙15다. 이 검토는 Q7을 독립 검토하지 않으므로 Q7의 5개를 독립 검증한 총수로 표시하지 않는다. MP의 상속 3.7.0 release/publication, 재사용 animate_decay/bayes_update 및 doc/conf.py 등이 제외된 것은 확인했다.

최종 `RESULT.md`, root `counts.json`, 병합 `sources.jsonl`/`source-reconciliation.json`, `SELF_CHECK.md`, 실행 검사 및 고정 결과판 재열람은 이 시점의 대상이 아니다. 후속 고정판에서 위 조정과 최종 표의 연결을 확인해야 한다.
