# Stage 1 독립 AI 검토

**판정: 일반층 선정과 봉인에 중단 사유를 찾지 못했다. 최종 자료 수의 상속 사건 처리와 빈 경로 해석에 후속 주의가 필요하다.**

검토자는 두 주 프로젝트의 작성자·root와 별도인 `/root/cross_domain` AI 에이전트다. 자기 작성물인 Q7은 검토하지 않았다. 이것은 사람 검토가 아니다. 입력 지문·UTC·상세 판정은 [review-stage1.json](review-stage1.json)에 있다. 새 ggplot2/Matplotlib tree·본문·자원·CI는 열지 않았다.

| 독립 확인 | 결과 |
|---|---|
| stage1 봉인 파일 지문 | **21/21 일치**. 예비 메시지의 22파일 언급은 수동 계수 오기이며 실제 seal의 항목 수는 21이다. |
| 공식 옛 tree와 frame의 접두범위 | GG 195 reference HTML 중 앞 68경로, MP 608 gallery HTML 중 앞 47경로가 frame과 정확히 같음 |
| 처음 40 적격과 해시 선정 | 양쪽 각 40적격. UTF-8 SHA-256 **80개 모두 재계산 일치**, 일반층 각 첫 2개 일치 |
| 대응 source path/blob | 기록된 비어 있지 않은 모든 경로의 blob이 옛 tree에 일치 |
| 첫 그림·배제 페이지 | 별도 HTMLParser로 옛 파일만 읽어 첫 scoped img 경로와 frame 대조. 제외한 Examples 영역의 img/picture/svg/canvas/object 대체 표현도 살폈으며 불일치 없음 |
| 선행 노출 | 원장의 새 판 접근은 release/tag/publication metadata에 한정돼 있음. 이 기록 안에서 새 본문·그림·개별 CI 접근 증거는 발견하지 못함 |
| 자동 스캔의 자료 최소량 산입 | GG 66 body 원장 행 중 일반 2개만 산입. MP도 일반 body 2개만 산입. 원장에 자동 적격성 스캔을 자세히 읽은 본문으로 부풀린 흔적 없음 |

## 의미 판독에서 확인한 점

`geom_count.html`의 첫 설명 그림은 **일반 `geom_point` 산점도**다. 옛 본문 L214–216이 이를 보여 주고 실제 `geom_count` 그림은 L218–220의 두 번째 그림이다. 작성자의 “비교 기준 산점도” 목적은 정확하며, 후속 판독에서 페이지 이름 때문에 두 번째 그림의 역할로 바꾸지 않아야 한다. `expansion.html` 첫 그림은 L123–127의 막대 아래 0·위 10% 여백 예제다.

Matplotlib의 선택 그림은 각각 정확한 제목 절 바로 안 L1027/L1032에 있고 src와 srcset이 함께 있다. 두 번째 단계가 끝난 뒤 2x 표현까지 추적할 대상임을 확인했다. 이 검토에서는 새 판이나 이미지 실물을 추가로 열지 않았다.

Matplotlib 3.6.3 release tag와 HTML이 표시하는 docs revision은 서로 다르다. `editions.json`은 tag `c23ccdde…`와 docs revision `655f616e…`를 보존하고 발행본의 실제 Download Python 경로를 source로 삼는다. tag 소스로 발행본 소스를 몰래 대신하지 않은 점을 확인했다.

## 세 가지 후속 주의

| 항목 | 직접 확인한 문제·범위 | 필요한 처리 |
|---|---|---|
| **R1: 상속 사건의 자료 수 처리 차이** | MP 원장 `MP-new-release`, `MP-new-pub-metadata-com`은 AF-RES-098과 같은 3.7.0 release/publication 사건인데 countable=true다. GG의 상속 3.5.0 release/publication은 false다. | 최종 합산 원장에서 두 MP 상속 사건을 보수적으로 제외하고 이유를 남기는 것을 권한다. 이미 봉인된 stage1 원장은 수정할 필요가 없다. 표본 선택에는 영향 없다. |
| **R2: 빈 경로는 삭제 증거가 아님** | MP `rain.html`, `unchained.html`은 적격이나 source_path가 공백이다. inline 그림 12개는 external relative asset path가 없다. | stage2에서 공백을 다음 tree의 부재로 취급하지 않는다. 해당 경로 규칙은 미확인으로 남기고, A/C층 자리를 억지로 채우지 않는다. |
| **R3: C층의 source 단위 차이** | MP는 생성된 `_downloads/<digest>/…py`, GG는 `man/*.Rd`를 비교한다. MP의 이전 다운로드 경로가 없어짐은 저자 소스 삭제와 동일하지 않다. | C층 신호를 “배포된 source 경로/blob 변경”으로 설명한다. 논리 예제 삭제·후계·목적 변경은 봉인 뒤 새 본문·대응 소스로 따로 판독한다. |

검토 범위는 기존 증거에 대한 별도 읽기·재계산이다. 모든 작업자의 보존되지 않은 도구 호출까지 감시했다고 주장하지 않는다. stage2 이후 선택·U/G 판정·최종 혼동표와 최소 자료 수는 이 검토의 대상이 아니다.
