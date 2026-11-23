# Q7 교차 분야 자료 — 별도 작성자 AI 검토

검토 시각: 2026-11-23T22:26:20.224042+00:00. 검토자 `/root/ggplot2`는 cross-domain 자료 작성자와 별도다. **독립 AI 내용 검토이며 사람 검토가 아니다.** 기존 수신 바이트를 별도 코드로 재검산했으며 새 네트워크 수신이나 역사적 실행 재현은 하지 않았다.

**판정: 핵심 P/U/G 구분과 보수적 자료 산입을 지지한다. 차단 문제 0건, 재현 명령 설명의 경미한 문구 문제 1건이다.** 검토 범위·입력 지문·실제 읽은 영수증은 [기계 판독 기록](review-cross-domain.json)에 있다.

## 판정과 독립 확인

| 검토 항목 | 별도로 확인한 사실 | 판단·한계 |
|---|---|---|
| EPUB 배포 포함 P | 공식 Trees 패키지의 보존 바이트 SHA-256과 HTTP 영수증 일치. ZIP 12멤버 지문 재계산; OPF manifest 9항목 모두 실제 멤버 존재, spine 3항목 | `cover.jpg` 포함 YES. 수록 사실은 titlepage 참조를 증명하지 않음 |
| EPUB 본문 U | `titlepage.xhtml#titlepage` L28–41은 canvas; L6–9는 네 스크립트. 세 XHTML·CSS·네 JS의 cover.jpg 문자 참조 0. tree.js의 canvas 선택과 Snake.js의 arc/fill을 직접 읽음 | 선택 본문의 JPEG 사용 NO는 지지. reader 책장·별도 표지 UI가 OPF cover-image를 쓸 가능성은 미확인으로 유지 |
| EPUB 실행·생성 G | source titlepage 1,375B와 ZIP 1,416B는 CRLF 41개 정규화 후 같고 OPF는 정확히 같은 바이트 | 변환 원인·당해 생성 실행·canvas 표시 미확인. 바이트 관계를 빌드 귀속으로 확대하지 않음 |
| Wheel P와 선언 | ZIP 19멤버/RECORD 19행, 비어 있지 않은 해시·크기 18/18 재계산 일치, 누락 0. 자체 RECORD 행은 공란. 두 entry-point 이름이 같은 `build.__main__:entrypoint`를 가리킴 | 선언된 함수 존재 YES. 한 console script·두 이름·한 고유 함수는 서로 다른 단위 |
| Wheel 실행·생성 | AST로 함수 L444–445를 읽었고 ZIP에 `pyproject-build` wrapper 파일이 없음을 확인 | 설치·호출·실제 빌드 생성은 모두 미확인. LICENSE 등 일반 RECORD 멤버를 실행 진입점으로 세지 않음 |

보존된 [EPUB 실물 영수증](../cross-domain/receipts/trees.epub.json), [wheel 실물 영수증](../cross-domain/receipts/build-1.2.2.post1-py3-none-any.whl.json), [EPUB 구조 원장](../cross-domain/trees-audit.json), [wheel 원장](../cross-domain/wheel-audit.json)을 대조했다. EPUB 부정 판단은 **저자가 지정한 해당 본문 참조 범위**에 한정된다. reader가 OPF 표지를 책장에 표시했다는 관측만으로 이 본문 판정을 뒤집지는 않는다.

## 자료 최소량 검토

| 분류 | 산입 ID | 보수적 개수 | 근거 |
|---|---|---:|---|
| EPUB | CD-E02, CD-E03 | 2 | 별도 Reading Systems 규격 1개와 새로운 Trees 실물 1개. 이미 사용한 EPUB core 규격·동일 release 사건·멤버/source 중복 제외 |
| Wheel | CD-W01, CD-W02, CD-W03 | 3 | wheel 형식 규격·entry-points 규격은 다른 규범 문서. 동일 source commit이어도 각각 다른 대상을 규정. 실물 wheel 1개 추가; HTML/RST·PyPI 메타데이터 중복 제외 |

[원장](../cross-domain/sources.jsonl) 16행 중 산입 5개를 재집계했고 다섯 지문이 서로 다름을 확인했다. 같은 바이트가 아니라고 독립 저작을 자동 인정한 것은 아니다. 규범 문서의 대상·계보와 실물의 저작 단위를 함께 보았다. EPUB 2·wheel 2 최소량은 이 범위에서 충족한다. 전체 작업 및 AF-RES-098와의 전역 중복 재검토는 root의 별도 검토 범위다. 이 검토 파일 자체는 새 외부 자료 수에 넣지 않는다.

## 경미한 문제와 권고

`cross-domain.md` L81은 analyze.py를 “읽기 전용 재검산”이라 부르지만, 같은 문단에서 audit를 다시 쓴다고 정확히 설명한다. 실제 코드 L36/L62/L122/L174/L176/L183도 audit·원장·집계 쓰기를 수행한다. “패키지 미실행 정적 재검산” 또는 “정적 재검산”으로 명칭을 바꾸고 별도 체크아웃 안내는 유지하는 것이 정확하다. 결론·분모·산입 수에는 영향이 없다. 원 작성 자료는 수정하지 않았다.

## 읽은 입력과 한계

| 입력 | SHA-256 |
|---|---|
| `audit.json` | `ff40e5e34540c5d49df7efcf7ccb34f830068ac9fca409927f8818b0ef210ebc` |
| `cross-domain.md` | `6f1bfb1a4eb0650e2bb3a6dbdc2eca215ab12111a1b5c7536a298afa30dfe43f` |
| `trees-audit.json` | `d12290299ce92f896fe9543c271bf41362f0ef9f6c54a854b87ec3211e2ba07c` |
| `wheel-audit.json` | `efd7aca5d440490226330d189ef380e8a6f4d89e9f69313ca9eebaa1a601c11b` |
| `sources.jsonl` | `5c7a68d914dec3fcf6314d343cad88123b87d75a136da73ce85c40b631076091` |
| `source-counts.json` | `8f822ad06d4ecf84a2ee3dc2293264df5735b601456a32e0af76debab993ac6e` |

여덟 영수증을 실제 읽고 대응 캐시 지문과 모두 일치함을 확인했다. Reading Systems §6.4, wheel 규격 L234–254, entry-points 규격 L10–15/L82–90/L126–154도 보존 원문으로 다시 읽었다. 원 작성자의 analyzer를 실행하지 않고 별도의 표준 라이브러리 코드로 ZIP/XML/CSV/AST 관계를 확인했다. 따라서 기존 audit를 다시 쓰지 않았다.

reader·JavaScript·EPUBCheck·wheel 설치/import/entrypoint 실행은 하지 않았다. 저자 그리기 코드와 정적 참조를 읽었지만 jQuery 전체의 모든 가능한 동적 경로를 형식 검증하지는 않았다. EPUB 3.0 실물에 대한 3.3 전체 적합성 인증도 아니다. 원 작성자의 cover 시각 판독은 이번 검토에서 재실행하지 않았다. 검토 완료 직전 여섯 원 입력의 해시가 시작 시 값과 같은 것을 확인했다.

다음 관측이 결론을 바꾼다: 해당 본문에서 cover.jpg로 이어지는 저자 지정/실행 경로, 이 wheel 지문에 연결된 설치·호출 영수증, 또는 산입한 다섯 자료 중 선행·동일 저작 중복을 입증하는 계보. 새 검토 파일 두 개만 작성하고 파일 수정을 종료한다.
