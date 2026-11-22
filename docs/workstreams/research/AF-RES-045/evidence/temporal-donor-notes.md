# 시간·영상 분야 제공 원문 판독 — 결말 개봉 전

담당: 같은 모델의 병렬 조사 문맥 `temporal_donors`. 독립 외부 판독 또는 사람 검토가 아니다. 이 담당자는 수신 이슈의 댓글·종료 사건·해결 PR·후속 시험을 열지 않았다. 표본 담당자가 전달한 최초 요구 요약만으로 아래 대응을 검토했다. 원문별 판·열람 시각·해시·실패는 `temporal-donor-sources.jsonl`에 있다.

## 산입

고유 제공 저작 4개(TD01–TD04), 독립 비교 저작 2개(TC01–TC02)를 직접 읽었다. 제공 중 시간 경계 작업은 Avid·Adobe·Netflix 3개다. Apple의 색 마스크·구간 선택은 같은 매뉴얼 한 저작이며, 후자는 추가 산입하지 않는다. Smith의 본문·부절·서지 안내도 한 저작이다. `minimum_count=true`만 세면 6이다. 전문 전체를 완독했다는 뜻이 아니라 기록한 절·쪽의 의미를 직접 확인했다는 뜻이다.

| ID | 판과 직접 근거 | 적절한 쓰임 | 배당 |
| --- | --- | --- | --- |
| TD01 | [Avid Release 9.0, 1999](https://resources.avid.com/SupportFiles/attach/MCGS.PDF), p82 `Using Frame Offset`, p106 I/O tracking | 선택 경계의 프레임 포함 관례와 시간코드 읽기 비교 | 제공·영화 편집 시간 |
| TD02 | [Adobe CS6, 2013-02](https://help.adobe.com/archive/en/premiere-pro/cs6/premiere_pro_reference.pdf), PDF p43·152·289–290 / printed39·148·285–286 | 프레임과 표본의 정밀도 차이; 동일 IN/OUT의 의미; 자산 색 레이블 | 제공·영화 편집 시간 |
| TD03 | [Netflix timing](https://partnerhelp.netflixstudios.com/hc/en-us/articles/360051554394-Timed-Text-Style-Guide-Subtitle-Timing-Guidelines), Introduction·§1·§2·§5 | 읽기 편의를 위해 경계를 이동하는 근접 반례 | 제공·방송/스트리밍 자막 시간 |
| TD04 | [Apple color masks](https://support.apple.com/en-lamr/guide/final-cut-pro/vera699eacc8/mac), 3D Softness step5·HSL softness; [range selection](https://support.apple.com/guide/final-cut-pro/select-ranges-ver28cca92/mac), browser range | 영상 색 범위의 확장·부드러움과 선택 테두리. 현재 적용 진단 | 제공·영상 후반 편집 |
| TC01 | [W3C fixed 2012 Recommendation](https://www.w3.org/TR/2012/REC-media-frags-20120925/), §4.2.1·§6.2.2·§7.4 | 같은 경계 숫자가 다른 프로토콜 의미를 갖는 반례 | 독립 비교 |
| TC02 | [Smith rectangular window](https://ccrma.stanford.edu/~jos/sasp/Rectangular_Window.html), [Side Lobes](https://ccrma.stanford.edu/~jos/sasp/Rectangular_Window_Side_Lobes.html), [author citation](https://ccrma.stanford.edu/~jos/sasp/sasp-citation.html) | 시간·주파수 단위를 교환하면 보존 조건이 달라지는 반례 | 독립 비교·수신측 인접 DSP |

## 봉인할 예측에 전달한 판단

### AUD01 / #407 — 숫자 출력을 같게 둔 두 API는 가를 수 없다

요구는 현재 선택 시작·끝을 스크립트에서 읽기다. 전용 `GetTime`과 기존 일반 선택 속성 접근 모두 정상 `(1.25, 2.5)`와 커서 `(1.25, 1.25)`를 돌려주게 설계할 수 있다. Avid의 시간코드 표시와 W3C의 명시적 구간 표기는 어느 명령 이름을 택할지 정하지 않는다. 두 후보가 같은 숫자를 예측한다면 판별 성공으로 세지 않는다. 새 조회 명령 이름은 작성자가 이미 제안한 것이므로 외부 원리가 새로 발견한 선택도 아니다.

동일 IN/OUT 프레임의 길이를 한 프레임으로 세는 Adobe 관례와 W3C 반개구간을 구분한다. **W3C는 `a=b`를 유효한 빈 재생으로 처리하지 않는다. §6.2.2는 오류인 구간 인수를 무시하도록 권고한다.** 따라서 이 규칙 전체를 커서 조회에 옮기면 오히려 필요한 커서 상태를 버릴 수 있다. 단위 반전 사고실험은 25fps의 한 프레임과 48kHz의 한 표본, 각각 0.04초와 약 0.000020833초다. 이는 산술이며 해당 프로그램 실행 측정이 아니다.

### AUD02 / #511 — 선택 표시와 콘텐츠 색을 분리하는 제3안

표본 담당자가 전한 원문은 클립마다 직접 고르는 전경·배경 색과 선택 표시를 다룬다. Adobe의 자산 색 레이블과 Apple의 선택 테두리는 동시에 적용할 수 있는 채널이다. 어느 쪽도 임의 RGB 유지(A)와 자동 대비 변경(B) 사이의 정확한 우열을 지정하지 않는다. 흑백과 같은 색 전경/배경 입력은 연구자가 추가한 판별 입력이다. 대비 보장은 별도 읽기 목적이고, 원래 색 보존과 충돌할 수 있다. 현재 Apple 예시를 2020년 요구자가 알았던 설계로 기록하지 않는다.

### AUD03 / #644 — 색 마스크와 주파수 마스크의 닮음은 조건부

Apple 원문의 softness는 주변 색을 선택 범위에 추가한다. 이 성질을 주파수에 옮기면 hard mask(A)와 주변 bin으로 번지는 feather(B)가 내부 tone에서는 함께 변화를 예측하고, 선택 바깥 경계 tone에서는 갈릴 수 있다. 그러나 이는 **연구자의 대응 가설**이다. color/HSL 좌표는 주파수축이 아니며, 주파수 smoothing·창·bin 반올림·재합성 계약을 먼저 특정해야 한다. 고정한 상한 바로 밖이라는 말만으로 2001Hz를 판별 입력으로 삼지 말고, 실제 상한 bin 다음 bin과 필요한 허용오차를 명시해야 한다.

원 요구자가 이미 Adobe Audition을 예로 들었다는 표본 담당자의 보고는 보존한다. 그 인접 오디오 도구가 새 타 분야 발견은 아니다. Smith의 수학은 잘못된 대응을 거르는 비교 근거이며 Audacity 코드 출력의 대체물도 아니다.

## 분야 구분과 뒤집히는 보존 조건

| 주 사용자·목표 | 조작 대상 | 수신 설계에 보존할 수 있는 것 | 잘못 옮기면 잃는 것 |
| --- | --- | --- | --- |
| 영화 편집자·선택한 샷 길이 | 개별 영상 프레임과 오디오 표본 | 단위·포함 여부를 표시하는 습관 | 커서 상태, 프레임 사이의 음향 경계 |
| 자막 작성자·읽기와 장면 동기 | 텍스트의 표시 시간 | 경계 변경에 목적·예외를 붙이는 규칙 | 정확한 오디오 선택 범위 |
| 영상 색보정 담당·시각적 색 분리 | 색 공간의 마스크 | hard/soft 범위 차이의 설명 | 주파수 bin과 변환의 물리적 의미 |
| 신호 분석자·주파수 해석 | 표본창과 스펙트럼 | 변환 및 허용오차의 명시 | 영상의 독립 픽셀처럼 취급하는 잘못된 독립성 |

영화 편집 소프트웨어와 오디오 편집 소프트웨어는 넓게 보면 같은 미디어 후반 작업의 인접 도구다. 이 사실을 유지한다. Netflix 자막 편집은 읽기·방송 편성 관점의 제공 규칙이고, W3C는 웹 미디어 구현 규약이다. 서로 다른 이름이나 회사라는 이유만으로 모두 먼 분야라고 세지 않는다.

비용·정밀도 제약을 제거해도 무조건 같은 추천이 되지는 않는다. 렌더링 비용을 없애면 부드러운 효과와 hard 경계를 선택적으로 제공할 여지는 커지지만, 어떤 구간을 보존해야 하는지는 여전히 목적·API가 정한다. 반대로 샘플 정밀도를 프레임 정밀도로 축소하면 정상 입력이 같아도 짧은 음성 경계에서 결과가 달라질 수 있다.

## 시점과 탐색 원장

1. 첫 병렬 검색(2026-11-22 22:03 UTC): `site.helpx.adobe.com premiere pro trim audio sample units frame boundaries`, Apple range selection, Avid inclusive IN/OUT, BBC subtitle shot-change gaps. 처음 보인 Apple range·Avid 공식 PDF·Netflix 항목을 출처 후보로 기록했다. BBC 검색의 미러들은 최소수에 넣지 않았다.
2. 공식성 보강 검색: Adobe 원문 경로, BBC GitHub, Apple slide edits, W3C `end exclusive`. W3C 고정 2012판과 Avid1999판을 선택했다. Adobe 옛 HTML은 2026 링크/연결 문서로 리다이렉트해 과거판 증거로 쓰지 않고 공식 CS6 보관 PDF로 이동했다.
3. 요구 선정 통보 뒤: Apple `color mask softness selection yellow border role colors`와 공식 Premiere sample-point 문구를 검색했다. Apple mask를 #644의 근접 후보, 범위 테두리를 #511의 제3안으로 삼았다. 현재판이라는 한계가 있다.
4. 직접 읽은 실패 경로는 TF01–TF08이다. Apple 웹 도구429 뒤 보통 HTTP GET은200이었다. Avid는 웹 본문 성공, 이후 셸403이었다. 실패를 성공으로 지우거나 중복 산입하지 않았다.
5. Netflix의 [공식 article metadata](https://partnerhelp.netflixstudios.com/api/v2/help_center/en-us/articles/360051554394.json)는 생성2020-07-27, 편집2025-07-04, 갱신2026-10-01을 각각 반환했다. 현행 문장을 2020 원판으로 부르지 않는다. Apple의 정확한 최초 공개일·과거판은 미확인이다. Smith는 저자 서지에서2011온라인판을 명시하지만 현재 바이트만 확인했다.

## 미확인과 최소 후속 확인

제공 원리의 수신 프로젝트 내 기존 참조 여부는 이 담당자가 검색하지 않았다. 원리 존재·당대 가용성과 실제 작성자 독서·채택을 분리한다. 어떤 후보도 후속 시험을 보지 않고 역사적 성공으로 승격하지 않았다. 다음 최소 자료는 더 많은 일반 매뉴얼이 아니라, 봉인한 조작·입력과 같은 수신측 결정·시험의 판이다. 특히 AUD01은 동일 숫자 출력만으로 유일 지지를 판정할 수 없고, AUD03은 선택 밖 bin과 허용오차를 고정한 시험이 있어야 한다.
