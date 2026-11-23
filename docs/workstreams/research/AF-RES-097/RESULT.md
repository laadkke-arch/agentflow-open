| 사건과 사용자판 | 원 요구와 필수 관측값 | 원 입력 주소·지문 | 두 후보와 고정 절 | 연구판·미확인 |
| --- | --- | --- | --- | --- |
| #5593 · Ubuntu 18.04 / Python 3.7 / Pillow 8.3.0 또는 8.3.1. Gist는 8.3.1 고정. [본문](https://github.com/python-pillow/Pillow/issues/5593#issue-939528731) | 본문은 mode `RGBA`를 요구한다. 입력은 `P`, RGB 팔레트, 투명 index 0. 연구는 네 채널과 index별 alpha 0/255도 확인한다. 좌표별 RGB 수치는 진단용. | [원 ZIP](https://codeload.github.com/gist/d98a4b54fb409bc8f745d169df0196fc/zip/7389968dec0ac74f493d28ccd0f5f7b00e7ca8de) · `indexed_with_transparency.png` 304B · SHA-256 `a4fa91aa20ae6115d4c5520d11fc8e2f1a52a4d3df53860175a51eaa94ce12be` | [기본 convert() 분기](https://github.com/python-pillow/Pillow/blob/51591a80a4e14543ea8cbe93026db5e79354b8c4/src/PIL/Image.py#L915-L924) / [명시 RGBA 분기](https://github.com/python-pillow/Pillow/blob/51591a80a4e14543ea8cbe93026db5e79354b8c4/src/PIL/Image.py#L1008-L1017) | 공식 Linux cp39 wheels 8.2.0/8.3.0/8.3.1에서 실행. 작성자 cp37 runtime·초기 본문 전 버전 미확인. |
| #5595 · Arch Linux / Python 3.9 / Pillow 8.3.0+. [본문](https://github.com/python-pillow/Pillow/issues/5595#issue-940162920) | `getpalette()[:len(p)] == p` 및 RGBRGB 색별 순서 선호. 번호 1·빨강은 화면 예시를 진단하는 관측. | [원 배열·생성식](https://github.com/python-pillow/Pillow/issues/5595#issue-940162920) · P 100×100 index 1 · literal SHA-256 `3d188159bb897e885f2910b00dff302d0b284f9c0daa7a012bcd347cd88831af` | [ImagePalette.getdata](https://github.com/python-pillow/Pillow/blob/51591a80a4e14543ea8cbe93026db5e79354b8c4/src/PIL/ImagePalette.py#L39-L83)를 부착 / [raw RGB 부착 절](https://github.com/python-pillow/Pillow/blob/51591a80a4e14543ea8cbe93026db5e79354b8c4/src/PIL/Image.py#L1749-L1776) | 8.2.0/8.3.0/8.3.1의 fresh 각 두 번. 작성자의 Arch 설치 및 초기 본문 전 버전 미확인. |

| 주 실행 · 사건·판·호출·반복 | 원 입력 SHA·새 프로세스 | 종료값·단계 | 실제 값 | 기대와 차이 | 원 출력·미실시 |
| --- | --- | --- | --- | --- | --- |
| #5593 · 8.2.0 · `convert()` · 1 | `a4fa91aa20ae…` · PID 1575 | 0 · 관측 | RGBA(4) · RGB 검정/흰색/검정 · α `0/255/255` | RGBA와 원 alpha 충족 | [stdout](evidence/experiment/5593-8.2.0-default-1.stdout.json) |
| #5593 · 8.2.0 · `convert()` · 2 | `a4fa91aa20ae…` · PID 1576 | 0 · 관측 | RGBA(4) · RGB 검정/흰색/검정 · α `0/255/255` | RGBA와 원 alpha 충족 | [stdout](evidence/experiment/5593-8.2.0-default-2.stdout.json) |
| #5593 · 8.2.0 · `convert('RGBA')` · 1 | `a4fa91aa20ae…` · PID 1577 | 0 · 관측 | RGBA(4) · RGB 검정/흰색/검정 · α `0/255/255` | RGBA와 원 alpha 충족 | [stdout](evidence/experiment/5593-8.2.0-rgba-1.stdout.json) |
| #5593 · 8.2.0 · `convert('RGBA')` · 2 | `a4fa91aa20ae…` · PID 1578 | 0 · 관측 | RGBA(4) · RGB 검정/흰색/검정 · α `0/255/255` | RGBA와 원 alpha 충족 | [stdout](evidence/experiment/5593-8.2.0-rgba-2.stdout.json) |
| #5593 · 8.3.0 · `convert()` · 1 | `a4fa91aa20ae…` · PID 1579 | 0 · 관측 | RGB(3) · RGB 검정/흰색/검정 · α `∅/∅/∅` · 색 키 `(0, 0, 0)` | mode·alpha 불일치 | [stdout](evidence/experiment/5593-8.3.0-default-1.stdout.json) |
| #5593 · 8.3.0 · `convert()` · 2 | `a4fa91aa20ae…` · PID 1580 | 0 · 관측 | RGB(3) · RGB 검정/흰색/검정 · α `∅/∅/∅` · 색 키 `(0, 0, 0)` | mode·alpha 불일치 | [stdout](evidence/experiment/5593-8.3.0-default-2.stdout.json) |
| #5593 · 8.3.0 · `convert('RGBA')` · 1 | `a4fa91aa20ae…` · PID 1581 | 0 · 관측 | RGBA(4) · RGB 검정/흰색/검정 · α `0/255/255` | RGBA와 원 alpha 충족 | [stdout](evidence/experiment/5593-8.3.0-rgba-1.stdout.json) |
| #5593 · 8.3.0 · `convert('RGBA')` · 2 | `a4fa91aa20ae…` · PID 1582 | 0 · 관측 | RGBA(4) · RGB 검정/흰색/검정 · α `0/255/255` | RGBA와 원 alpha 충족 | [stdout](evidence/experiment/5593-8.3.0-rgba-2.stdout.json) |
| #5593 · 8.3.1 · `convert()` · 1 | `a4fa91aa20ae…` · PID 1583 | 0 · 관측 | RGB(3) · RGB 검정/흰색/검정 · α `∅/∅/∅` · 색 키 `(0, 0, 0)` | mode·alpha 불일치 | [stdout](evidence/experiment/5593-8.3.1-default-1.stdout.json) |
| #5593 · 8.3.1 · `convert()` · 2 | `a4fa91aa20ae…` · PID 1584 | 0 · 관측 | RGB(3) · RGB 검정/흰색/검정 · α `∅/∅/∅` · 색 키 `(0, 0, 0)` | mode·alpha 불일치 | [stdout](evidence/experiment/5593-8.3.1-default-2.stdout.json) |
| #5593 · 8.3.1 · `convert('RGBA')` · 1 | `a4fa91aa20ae…` · PID 1585 | 0 · 관측 | RGBA(4) · RGB 검정/흰색/검정 · α `0/255/255` | RGBA와 원 alpha 충족 | [stdout](evidence/experiment/5593-8.3.1-rgba-1.stdout.json) |
| #5593 · 8.3.1 · `convert('RGBA')` · 2 | `a4fa91aa20ae…` · PID 1586 | 0 · 관측 | RGBA(4) · RGB 검정/흰색/검정 · α `0/255/255` | RGBA와 원 alpha 충족 | [stdout](evidence/experiment/5593-8.3.1-rgba-2.stdout.json) |
| #5595 · 8.2.0 · `object` · 1 | `3d188159bb89…` · PID 1587 | 0 · 관측 | `[0, 255, 0, 0, 0, 255, 0, 0, 0]` · index 1 · RGB `(0, 0, 255)` | p의 offset 1 · 0→255 | [stdout](evidence/experiment/5595-8.2.0-object-1.stdout.json) |
| #5595 · 8.2.0 · `object` · 2 | `3d188159bb89…` · PID 1588 | 0 · 관측 | `[0, 255, 0, 0, 0, 255, 0, 0, 0]` · index 1 · RGB `(0, 0, 255)` | p의 offset 1 · 0→255 | [stdout](evidence/experiment/5595-8.2.0-object-2.stdout.json) |
| #5595 · 8.2.0 · `raw` · 1 | `3d188159bb89…` · PID 1589 | 0 · 관측 | `[0, 0, 0, 255, 0, 0, 0, 255, 0]` · index 1 · RGB `(255, 0, 0)` | p 일치 | [stdout](evidence/experiment/5595-8.2.0-raw-1.stdout.json) |
| #5595 · 8.2.0 · `raw` · 2 | `3d188159bb89…` · PID 1590 | 0 · 관측 | `[0, 0, 0, 255, 0, 0, 0, 255, 0]` · index 1 · RGB `(255, 0, 0)` | p 일치 | [stdout](evidence/experiment/5595-8.2.0-raw-2.stdout.json) |
| #5595 · 8.3.0 · `object` · 1 | `3d188159bb89…` · PID 1591 | 0 · 관측 | `[0, 0, 0, 255, 0, 0, 0, 255, 0]` · index 1 · RGB `(255, 0, 0)` | p 일치 | [stdout](evidence/experiment/5595-8.3.0-object-1.stdout.json) |
| #5595 · 8.3.0 · `object` · 2 | `3d188159bb89…` · PID 1592 | 0 · 관측 | `[0, 0, 0, 255, 0, 0, 0, 255, 0]` · index 1 · RGB `(255, 0, 0)` | p 일치 | [stdout](evidence/experiment/5595-8.3.0-object-2.stdout.json) |
| #5595 · 8.3.0 · `raw` · 1 | `3d188159bb89…` · PID 1593 | 0 · 관측 | `[0, 0, 0, 255, 0, 0, 0, 255, 0]` · index 1 · RGB `(255, 0, 0)` | p 일치 | [stdout](evidence/experiment/5595-8.3.0-raw-1.stdout.json) |
| #5595 · 8.3.0 · `raw` · 2 | `3d188159bb89…` · PID 1594 | 0 · 관측 | `[0, 0, 0, 255, 0, 0, 0, 255, 0]` · index 1 · RGB `(255, 0, 0)` | p 일치 | [stdout](evidence/experiment/5595-8.3.0-raw-2.stdout.json) |
| #5595 · 8.3.1 · `object` · 1 | `3d188159bb89…` · PID 1595 | 0 · 관측 | `[0, 0, 0, 255, 0, 0, 0, 255, 0]` · index 1 · RGB `(255, 0, 0)` | p 일치 | [stdout](evidence/experiment/5595-8.3.1-object-1.stdout.json) |
| #5595 · 8.3.1 · `object` · 2 | `3d188159bb89…` · PID 1596 | 0 · 관측 | `[0, 0, 0, 255, 0, 0, 0, 255, 0]` · index 1 · RGB `(255, 0, 0)` | p 일치 | [stdout](evidence/experiment/5595-8.3.1-object-2.stdout.json) |
| #5595 · 8.3.1 · `raw` · 1 | `3d188159bb89…` · PID 1597 | 0 · 관측 | `[0, 0, 0, 255, 0, 0, 0, 255, 0]` · index 1 · RGB `(255, 0, 0)` | p 일치 | [stdout](evidence/experiment/5595-8.3.1-raw-1.stdout.json) |
| #5595 · 8.3.1 · `raw` · 2 | `3d188159bb89…` · PID 1598 | 0 · 관측 | `[0, 0, 0, 255, 0, 0, 0, 255, 0]` · index 1 · RGB `(255, 0, 0)` | p 일치 | [stdout](evidence/experiment/5595-8.3.1-raw-2.stdout.json) |

| 사용자 목적·판 | 반환 링크와 확인할 절 | 판정 | 반례 | 바로 답할 근거·확인할 조건 |
| --- | --- | --- | --- | --- |
| #5593 · RGBA+원 투명도 · 8.2.0 | [명시 RGBA 분기](https://github.com/python-pillow/Pillow/blob/e0e353c0ef7516979a9aedce3792596649ce4433/src/PIL/Image.py#L990-L999) | 양쪽 일치 | tRNS 없는 P, 또는 먼저 로드한 Hopper에 transparency 설정. | 원 PNG를 fresh open하며 RGBA/원 alpha 목표가 이미 명시됐다. |
| #5593 · RGBA+원 투명도 · 8.3.0 | [명시 RGBA 분기](https://github.com/python-pillow/Pillow/blob/51591a80a4e14543ea8cbe93026db5e79354b8c4/src/PIL/Image.py#L1008-L1017) · [기본 convert() 분기](https://github.com/python-pillow/Pillow/blob/51591a80a4e14543ea8cbe93026db5e79354b8c4/src/PIL/Image.py#L915-L924) | 한쪽만 충족 · 명시 RGBA | 두 검정을 RGB 키로 승격하면 불투명 index 1도 사라진다. | RGBA·index별 투명도 목적이면 명시 호출을 바로 제시한다. |
| #5593 · RGBA+원 투명도 · 8.3.1 | [명시 RGBA 분기](https://github.com/python-pillow/Pillow/blob/92933b86574b9c80764bf52c357ed29e1ef53382/src/PIL/Image.py#L1008-L1017) · [기본 convert() 분기](https://github.com/python-pillow/Pillow/blob/92933b86574b9c80764bf52c357ed29e1ef53382/src/PIL/Image.py#L915-L924) | 한쪽만 충족 · 명시 RGBA | 두 검정을 RGB 키로 승격하면 불투명 index 1도 사라진다. | RGBA·index별 투명도 목적이면 명시 호출을 바로 제시한다. |
| #5595 · 원 p·RGBRGB 판독 · 8.2.0 | [raw RGB 부착 절](https://github.com/python-pillow/Pillow/blob/e0e353c0ef7516979a9aedce3792596649ce4433/src/PIL/Image.py#L1692-L1720) · [ImagePalette.getdata](https://github.com/python-pillow/Pillow/blob/e0e353c0ef7516979a9aedce3792596649ce4433/src/PIL/ImagePalette.py#L39-L83) | 한쪽만 충족 · raw | 객체가 원 p를 평면 배열로 읽어 index 1은 파랑. | RGBRGB가 이미 명시됐다. dirty 재실현은 별도 조건이다. |
| #5595 · 원 p·RGBRGB 판독 · 8.3.0 | [raw RGB 부착 절](https://github.com/python-pillow/Pillow/blob/51591a80a4e14543ea8cbe93026db5e79354b8c4/src/PIL/Image.py#L1749-L1776) | 양쪽 일치 | 같은 p의 다른 버전 8.2.0에서 객체가 다르다. | fresh P의 저장 전 배열·번호·RGB가 같다. 호환 안내에는 raw를 대표한다. |
| #5595 · 원 p·RGBRGB 판독 · 8.3.1 | [raw RGB 부착 절](https://github.com/python-pillow/Pillow/blob/92933b86574b9c80764bf52c357ed29e1ef53382/src/PIL/Image.py#L1749-L1776) | 양쪽 일치 | `size` 제거 이후의 객체 호출은 별도 검증 범위. | fresh P의 저장 전 배열·번호·RGB가 같다. 호환 안내에는 raw를 대표한다. |

## 분모와 적용 범위

| 검산 항목 | 실측·비교 | 분모와 제외 |
| --- | --- | --- |
| 주 실행 | **24/24 관측**, 실행 결원 0. #5593 12/12, #5595 12/12 | 2사건×3판×2후보×2반복. 원 PNG 12개와 원 literal의 새 P 12개. 연구자 실행 24, 작성자·유지관리자 실행 0. |
| 반복 일치 | **12/12** | 관측 payload 전체 비교. UTC·PID·런타임 경로 등 실행 식별자를 제외한 값. 원 PNG 각 child는 새로 열고 새 p는 각 child가 할당. |
| 사건×판의 판정 | **양쪽 일치 3/6, 한쪽만 충족 3/6, 양쪽 미충족 0/6, 미확인 0/6** | 두 반복의 관측·일치 후 채점. #5593 8.2.0과 #5595 8.3.0·8.3.1만 두 링크를 해당 목적 기준으로 대체 가능. |
| 환경 교정 | **주 6/6**, 후대 8.4.0 보조 2/2 | 각 판의 독립된 양성/음성 P PNG 쓰기·새로 열기. 설치 결손 0/3. `PIL`, `Image.py`, `ImagePalette.py`, `_imaging` 실제 파일과 wheel 내부 바이트도 대조. |
| 보조 실행 | **53/53 시도**. 출력 47, 입력 모드 거절 6 | 작은 PNG 30, #5595 저장 재열기 6, RGB 입력 거절 6, 같은 객체 순차 2, RGB→RGBA 재승격 3, Hopper 4, 후대판 원 PNG 2. 주 실행에 합산하지 않는다. |
| 공개 보고형 근거 | #5593 작성자 implicit RGB, 다른 댓글의 LA 보고. #5595 작성자 객체 경로 색 설명·raw 수용, 유지관리자 순차 원 비교 | 연구자 주 실행 24/24의 일부가 아니다. 비슷한 당시 출력은 #5595의 두 판 순차 연구자 대조 2/2와 비교한다. |
| 직접 연 외부 원문 | **40개** | 이슈 2, 릴리스·변경 11, 고정 구현·시험·입력 13, PNG 규격·독립 시험 4, Arrow 3, GDAL 7. 원장 61행 중 21행은 이슈 댓글·중복·접근 실패 등으로 제외. 동일 저작 계보의 수를 독립 실험 수로 해석하지 않는다. |

원 색과 alpha를 읽는 순서는 0번 `(29,24)` → 불투명 2번 `(0,0)` → 같은 검정인 불투명 1번 `(75,53)`이다. ∅는 alpha 채널이 없다는 관측이다. RGB 검정은 `(0,0,0)`, 흰색은 `(255,255,255)`다. `object`는 `ImagePalette.ImagePalette(mode='RGB', palette=p, size=len(p))`를 만들고 `image.putpalette(palette)`를 호출한다. `raw`는 `image.putpalette(p, rawmode='RGB')`다. `p`와 각 좌표의 원 청크·해시는 [inputs.json](inputs.json), 프로세스·명령·stderr의 바이트는 [runs.jsonl](runs.jsonl)과 [실행 영수증](evidence/experiment/execution.json), 재계산은 [reconciliation.json](evidence/reconciliation.json)에 있다.

세 공식 CPython 3.9 Linux x86_64 wheels의 SHA-256 모두 PyPI 파일 목록과 일치했다. 고정 태그 `Image.py` 바이트 또한 각 wheel의 실제 로드 파일과 일치했다. 8.3.1에서 같은 구간을 보아도 별도 배포 wheel/코어와 새 실행을 사용했다. 8.4.0은 #5594의 후대 분기를 비교하려고 추가했다. Ubuntu 18.04/Python 3.7과 Arch 시스템 설치는 원 보고의 조건이며 이 환경에서 재연하지 않았다. `uv`의 `/home/agent/.local/bin` 링크 경고 이후 절대 경로의 CPython 3.9.23을 사용했다. [환경 및 지문](environment.json) [원 wheel 설치 출력](evidence/install)

## #5593의 원인과 후대 회귀

원 PNG의 20,000픽셀 중 index 0/1/2는 7,221/199/12,580개다. `PLTE`는 검정·검정·흰색, 짧은 `tRNS=[0]` 뒤의 alpha는 규격상 255다. 별도 같은 바이트의 witness에서 입력 index를 읽었고, 변환 대상은 헤더만 읽은 상태에서 호출했다. 소스 이미지의 번호 배열은 각 실행 전후 같았다. 8.2.0의 P PNG에서 `load()` 뒤 팔레트 모드는 `RGBA`로 바뀌지만 8.3.0·8.3.1에서는 `RGB`다. 8.3.x의 명시 `RGBA` 분기는 투명 번호 0에 alpha를 부여한다. 주 실행에서 8.2.0과 명시 RGBA의 성공 결과는 전체 픽셀에서 alpha 0의 7,221개와 alpha 255의 12,779개로 일치했다. [PNG palette와 transparency](https://www.w3.org/TR/2025/REC-png-3-20250624/#11tRNS) [8.2.0 load](https://github.com/python-pillow/Pillow/blob/e0e353c0ef7516979a9aedce3792596649ce4433/src/PIL/Image.py#L821-L838) [8.3.0 load 변경](https://github.com/python-pillow/Pillow/commit/804183c2489242251fdd9858b6e781ceefb08c8b)

8.3.0·8.3.1에서 기본 RGB를 `convert('RGBA')`로 다시 변환하면 검정 색 키로 인해 원래 불투명한 199개 index 1도 alpha 0이 된다. 투명 픽셀은 7,221→7,420개이고 흰색은 12,580개 그대로다. 출력에 alpha 채널만 추가하는 보정은 이 원본의 의미를 복구하지 못한다. [재승격 8.3.0](evidence/experiment/promotion-5593-8.3.0-default-1.stdout.json) [재승격 8.3.1](evidence/experiment/promotion-5593-8.3.1-default-1.stdout.json) [RGB 색 키 C 분기](https://github.com/python-pillow/Pillow/blob/51591a80a4e14543ea8cbe93026db5e79354b8c4/src/libImaging/Convert.c#L1643-L1704)

| 같은 조건을 비교할 원천과 입력 | 8.2.0 | 8.3.0·8.3.1 | 수정 이후 8.4.0 관측 |
| --- | --- | --- | --- |
| Gist 원 P PNG, 로드 시 이미 `tRNS=0` | `load`가 palette.mode를 RGBA로 실현. 기본도 RGBA. | palette.mode가 RGB라 기본 `RGB`. explicit은 세 판에서 RGBA. | 기본과 명시 모두 RGBA, alpha 0/255 수량은 주 RGBA와 동일. [기본 결과](evidence/experiment/postfix-5593-8.4.0-default-1.stdout.json) [명시 결과](evidence/experiment/postfix-5593-8.4.0-rgba-1.stdout.json) |
| 고정 Hopper PPM → `P`의 copy, 기본 두 번 뒤 `info['transparency']=0` | `RGB → RGB → RGB`, 원 PNG와 갈린다. metadata가 palette 실현 뒤 추가된다. | `RGB → RGB → RGB`, 원 PNG의 기본과 같은 mode. | `RGB → RGB → RGBA`, 0번 971픽셀·나머지 15,413. 연구자가 원 시험 순서를 재생한 결과. [8.2.0](evidence/experiment/hopper-5593-8.2.0-upstream-sequence-1.stdout.json) [8.4.0](evidence/experiment/hopper-5593-8.4.0-upstream-sequence-1.stdout.json) |

수정 PR #5594의 `test_default`는 Hopper 결과의 mode와 크기를 확인한다. 원 PNG 및 명시 RGBA 비교는 이 연구의 별도 실행이다. #5606은 다른 댓글의 LA/PA 경로를 처리한다. 이 변경, 원 Gist의 수정 내역, 8.4.0 원 wheels와 연구 실행은 각각 범위가 다르다. [#5594 원 시험](https://github.com/python-pillow/Pillow/blob/fdfa9e8521a0b9436a6324f652c323a2e3a0b21e/Tests/test_image_convert.py#L41-L53) [helper 원 입력](https://github.com/python-pillow/Pillow/blob/fdfa9e8521a0b9436a6324f652c323a2e3a0b21e/Tests/helper.py#L242-L262) [#5606 변경](https://github.com/python-pillow/Pillow/pull/5606) [8.4.0 고정 분기](https://github.com/python-pillow/Pillow/blob/40e7ff622669550733b26f14dc817fb72e096250/src/PIL/Image.py#L915-L925)

## #5595의 순차 부착과 저장

객체 경로의 8.2.0 non-raw `getdata()`는 RGB 평면을 뜻하는 `RGB;L`을 내고, 8.3.0에서는 `RGB`로 바뀐다. raw 배열 기본 rawmode는 세 판에서 `RGB`다. 8.2.0 객체 결과의 원 p 대비 처음 다른 위치는 0-based offset 1 (`0 → 255`)이다. 당시 공개 배열과의 첫 차이는 없었다. `8.3.0+`라는 과거 보고와 별도로 8.3.1에서도 해당 p의 결과를 관측했다. [8.2.0 getdata](https://github.com/python-pillow/Pillow/blob/e0e353c0ef7516979a9aedce3792596649ce4433/src/PIL/ImagePalette.py#L62-L83) [dirty reload 변경](https://github.com/python-pillow/Pillow/commit/1ee30ded0b672c8e8862720ec1dc71825db8ca81) [#5599 문서 수정 및 추가 변경](https://github.com/python-pillow/Pillow/pull/5599)

| 독립 대조 | 8.2.0 | 8.3.0 | 8.3.1 |
| --- | --- | --- | --- |
| 같은 객체 `object → raw → dirty/load` | 변경 배열 → p → 변경 배열. dirty 후 getcolor 두 호출은 `IndexError`. [원 출력](evidence/experiment/sequential-5595-8.2.0-object-then-raw-1.stdout.json) | p → p → p. dirty 후 getcolor는 검정 0, 흰색 3. [원 출력](evidence/experiment/sequential-5595-8.3.0-object-then-raw-1.stdout.json) | 주 fresh 대상만 포함. 동일 객체 보조 비교는 8.2.0·8.3.0의 2행. |
| object PNG 재열기 | 2bit·PLTE 3개. 바뀐 배열/번호1/파랑 유지. [원 출력](evidence/experiment/roundtrip-5595-8.2.0-object-1.stdout.json) | p/번호1/빨강. [원 출력](evidence/experiment/roundtrip-5595-8.3.0-object-1.stdout.json) | p/번호1/빨강. [원 출력](evidence/experiment/roundtrip-5595-8.3.1-object-1.stdout.json) |
| raw PNG 재열기 | p/번호1/빨강. [원 출력](evidence/experiment/roundtrip-5595-8.2.0-raw-1.stdout.json) | p/번호1/빨강. [원 출력](evidence/experiment/roundtrip-5595-8.3.0-raw-1.stdout.json) | p/번호1/빨강. [원 출력](evidence/experiment/roundtrip-5595-8.3.1-raw-1.stdout.json) |

6개 PNG의 저장 전과 재열기 각각에서 기존의 9개 prefix·번호·RGB가 유지됐다. 저장 파일은 각 111B, no tRNS이고 p인 5개의 PNG bytes SHA가 같다. 원 쌍은 저장 전 기준이다. 유지관리자는 2021년 같은 객체에서 보고했고 원 작성자는 raw가 목적에 맞는다고 후속 응답했다. 이 연구에서 `Image.show()`나 외부 뷰어는 실행하지 않았다. 화면 색은 같은 이미지의 명시 RGB 픽셀로 대조했다. [유지관리자 실행](https://github.com/python-pillow/Pillow/issues/5595#issuecomment-877558030) [작성자의 raw 수용](https://github.com/python-pillow/Pillow/issues/5595#issuecomment-877853085)

## 같은 색·같은 번호·같은 호출이 갈리는 대조

| 구성 입력 | 겉보기/색 배열 | 원 번호·alpha 관측 | 판정이 갈리는 목적 |
| --- | --- | --- | --- |
| `used-trns` 작은 PNG, 실제 index 0 사용 | 세 판 모두 양쪽 RGB bytes 동일 | RGBA의 alpha 0 1개, 255 3개. 기본 8.2.0만 RGBA, 양 8.3.x 기본은 alpha 없음 | RGB 비교만으로 원 alpha와 mode를 충족했다고 보면 오병합. [8.3.1 명시](evidence/experiment/control-used-trns-8.3.1-rgba-1.stdout.json) |
| `no-trns` 작은 PNG | 세 판 모두 같은 RGB, 같은 원 PLTE, 기본 RGB와 명시 RGBA의 mode는 다름 | 실제 RGBA alpha 255만 4개. RGB에는 alpha와 색 키 둘 다 없었다. | 완전 불투명한 화면 픽셀이 목적이면 양쪽, 소비자가 RGBA를 요구하면 명시만. [기본](evidence/experiment/control-no-trns-8.3.1-default-1.stdout.json) [명시](evidence/experiment/control-no-trns-8.3.1-rgba-1.stdout.json) |
| `unused-trns` 작은 PNG, tRNS `[0]`, 실제 index 1·2만 사용 | 세 판 모두 같은 RGB, 8.3.x 기본에서 생성된 RGB 색 키에 해당하는 픽셀이 없다 | 명시 RGBA alpha 255만 4개. 기본 8.2.0도 RGBA 255만, 8.3.x는 alpha 채널 부재 | tRNS 존재만으로 실제 투명 픽셀·합성 차이를 선언하면 오분리. RGBA mode 요구에는 버전별 분기를 적용. [8.2.0](evidence/experiment/control-unused-trns-8.2.0-default-1.stdout.json) [8.3.1](evidence/experiment/control-unused-trns-8.3.1-default-1.stdout.json) |
| `duplicate-a`/`duplicate-b` 2bit P PNG | 동일 PLTE에서 index 1·2 모두 `(70,80,90)`. 두 입력·두 변환의 RGB sha 동일. RGBA 6픽셀은 전부 불투명. | x 배열을 `[1,2,3,1,2,3]`에서 `[2,1,3,2,1,3]`으로 바꾸면 index 1의 집합은 `{0,3}`→`{1,4}`. 변환 뒤 원 번호 선택은 미정의. | 렌더/팔레트 목록 소비는 동일, 클래스 번호 소비는 차이가 있다. [A](evidence/experiment/control-duplicate-a-8.3.1-rgba-1.stdout.json) [B](evidence/experiment/control-duplicate-b-8.3.1-rgba-1.stdout.json) |
| RGB에 palette 부착 | 양쪽 모두 ValueError `illegal image mode`. 3판×2호출, exit 2. | 출력 없음, `unsupported_call`에서 중단. | **양쪽 미충족** 3/3. 원 입력이나 수행 환경이 없어 실행이 없으면 **미확인**이다. [예시 stderr](evidence/experiment/rejected-5595-8.3.0-object-1.stderr.txt) |

Arrow의 값 decode와 정수 번호 선택, GDAL의 RGB 채널과 `ReadRaster()` 밴드 번호도 같은 구분이 필요하다. 각 도구의 작성자/화면/클래스 소비자 기준, 순서 그대로인 원 대조, 고정 원 시험 실행 방법은 [타 분야 비교](evidence/cross-domain.md)에 있다. Arrow·GDAL·libpng·Go의 해당 원 테스트는 읽었고 이번 연구에서 자체 빌드를 실행하지 않았다. Q1~Q7의 반례와 미확인, 자료별 UTC·판·근거는 [SELF_CHECK.md](SELF_CHECK.md) 및 [sources.jsonl](sources.jsonl). 이번 기록의 검산은 연구자의 자기 검토다.

| 가장 중요한 불일치·약점 | 다음에 열 자료 또는 실행할 입력 | 어떤 관측이면 결론을 바꿀지 |
| --- | --- | --- |
| 원 PNG는 단일 투명 인덱스 0 분기다. 색 키 재승격은 이미 불투명 199개를 잃었다. | 고정 8.3.0의 `pil123p.png` 및 2-bit `tRNS=[0,128]` 미니 PNG를 판별 fresh 호출로 실행한다. [다중 alpha 원 시험](https://github.com/python-pillow/Pillow/blob/51591a80a4e14543ea8cbe93026db5e79354b8c4/Tests/test_file_png.py#L220-L228) | 기본이 부분 alpha를 보존하거나 명시 RGBA가 잃는 판·입력이 있으면 단일 투명 입력 밖의 링크 규칙을 바꾼다. |
| #5595의 묶음은 제시한 p·RGB와 8.3.x의 두 판에서 관측했다. 8.2.0에서는 dirty 후 raw도 바뀐다. | 같은 p를 8.3.x의 dirty·save variants와 `size` 인자 제거판에서 fresh 두 경로로 재현한다. [size 변경 기록](https://github.com/python-pillow/Pillow/blob/40e7ff622669550733b26f14dc817fb72e096250/docs/releasenotes/8.4.0.rst) | 후보 한쪽만 p·RGB를 잃거나 constructor가 입력을 거절하면 해당 조작의 묶음을 해제한다. |
| 사용자 실제 환경과 초기 본문 전 이력, 타 분야 빌드 실행의 공백이 있다. | GitHub `userContentEdits`와 원 보고 환경의 바이트 고정 재실행을 확보하고 Arrow·GDAL의 원 번호 선택을 함께 확인한다. [재현 방법](reproduce.md) [타 분야 입력](evidence/cross-domain.md) | 초판이 다른 필수조건을 제시하거나 원 환경이 이 연구의 판별과 반대로 출력하면 사용자판 안내를 수정한다. 타 분야 선택 마스크의 실측이 계산과 다르면 일반화 범위를 다시 정한다. |
