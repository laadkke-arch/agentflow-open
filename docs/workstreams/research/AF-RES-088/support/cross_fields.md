# Q7 타 분야 대조: 판 식별과 조건 식별

이 파일은 AF-RES-088의 Stack Overflow 모집·32쌍 분모와 분리된 목적 표집 대조다. **IETF 초안 두 사건, 학술 프리프린트 두 사건 모두 원판·다음판·후속 인용을 직접 열었다.** 같은 논문의 HTML/PDF/메타데이터는 독립 사건으로 중복 계산하지 않았다. 본문의 비교용 질문은 연구자가 만든 probe이며 실제 사용자가 했던 요청으로 간주하지 않는다. 문서 판독만 수행했고 프로토콜 구현·모델 학습·물리 계산은 실행하지 않았다.

## 사건과 인용 사슬

| 사건 | 원판 → 다음판·시점 | 직접 비교한 위치·관측 | 후속 인용 원문·시점 | 같은 답을 지지하는 반례 / 달라지는 조건 |
| --- | --- | --- | --- | --- |
| CF-I1 · QUIC 전송 초안 | [transport-27](https://www.ietf.org/archive/id/draft-ietf-quic-transport-27.html), 2020-02-21, 만료 2020-08-24 → [transport-28](https://www.ietf.org/archive/id/draft-ietf-quic-transport-28.html), 2020-05-20, 만료 2020-11-21 | §14: 두 판 모두 클라이언트 Initial 포함 UDP datagram payload를 적어도 1200바이트로 확장한다. 다음판은 peer의 최대 UDP payload 조건을 추가 설명한다. §18.2의 0x03 이름은 max_packet_size에서 max_udp_payload_size로 바뀐다. -28 변경기록에는 max_udp_datagram_size라는 중간 명칭도 남아 있으므로 본문 절을 우선한다. | [ATSSS overview-00](https://datatracker.ietf.org/doc/html/draft-bonaventure-quic-atsss-overview-00), 표지 2020-05-30, 참고문헌의 I-D.ietf-quic-transport는 -28과 May 2020을 명시. 본문 §6의 connection migration 논의가 이 참조를 사용한다. | “Initial 최소 payload가 1200인가”는 양판에서 같은 답. “1200 초과를 허용할 때 무슨 전제를 붙이는가”는 -28에서 path뿐 아니라 peer 지원이 명시되어 안내가 구체화된다. 후속 문헌의 -28 명시는 실제 구현판·실험 성공 증거가 아니다. [CF-S01–03] |
| CF-I2 · TLS 1.3 초안 | [tls13-27](https://datatracker.ietf.org/doc/html/draft-ietf-tls-tls13-27), 2018-03-18, 만료 2018-09-19 → [tls13-28](https://datatracker.ietf.org/doc/html/draft-ietf-tls-tls13-28), 2018-03-20, 만료 2018-09-21 | §4.2.11의 binder 검증 실패 시 handshake 중단 규칙은 두 판에 있다. -27 Appendix E.6은 Static RSA 공격, -28 E.6은 새 PSK Identity Exposure이고 Static RSA는 E.7로 이동한다. -28 §1.2도 새 노출 절 추가를 기록한다. | [rfc8447bis-00](https://www.ietf.org/archive/id/draft-ietf-tls-rfc8447bis-00.html), 2022-03-29, §20.1은 -28, 2018-03-20과 판 지정 URL을 명시한다. 같은 참고문헌에 최종 RFC8446도 별도로 존재한다. | “binder가 틀리면 중단하는가”는 양판 같은 답. “PSK와 인증서 인증을 모두 받는 서버의 identity 확인 공격을 어디서 설명하는가”는 -28 E.6을 지정해야 한다. 같은 E.6 번호만으로 절 정체성이 유지되지 않는다. 이는 새 취약점 발생시점의 측정이 아니라 문서 근거의 추가다. [CF-S04–06] |
| CF-A1 · Transformer 프리프린트 | [1706.03762v1 PDF](https://arxiv.org/pdf/1706.03762v1), 2017-06-12 17:57:34Z → [v2 PDF](https://arxiv.org/pdf/1706.03762v2), 2017-06-19 16:49:45Z | PDF abstract의 EN-FR 결과는 v1 41.0/3.5일, v2 41.2/4.5일. v2 §6.1은 41.17 및 embedding 비공유·d_ff=8192를 쓰지만 같은 PDF Table 2의 big EN-FR 셀은 41.0이다. HTML 본문에서도 이 불일치를 확인했다. v2 abs 메타데이터에는 41.0/3.5일이 남아 있다. | [BERT 1810.04805v1](https://arxiv.org/html/1810.04805v1), 2018-10-11, §3.1은 Vaswani et al.의 Transformer encoder 구현을 근거로 들고, 참고문헌은 NIPS 2017 출판본을 지시한다. arXiv v1/v2 선택은 명시하지 않는다. | “재귀 없이 attention 중심 구조인가”는 양판 같은 답. “EN-FR 보고 점수가 41.1 이상인가”는 v1에서 반박, v2에서는 위치에 따라 상충하므로 보류해야 한다. v2 하나를 고정해도 내부 위치·표현 형식이 빠지면 정답 판정이 닫히지 않는다. BERT의 후속 사용을 특정 preprint판 실사용 증거로 올리지 않는다. [CF-S07–12] |
| CF-A2 · Kalb–Ramond 중력 프리프린트 | [2401.14452v1](https://arxiv.org/html/2401.14452v1), 2024-01-25 19:00:00Z → [v2](https://arxiv.org/html/2401.14452v2), 2025-10-29 10:21:29Z | v1 §VI.2는 amplitude birefringence와 GWTC-3 기반 한계를 제시한다. v2 §V 식(30)–(32)는 최저차수에서 phase 효과만 남는다고 쓰고 §VI.2가 사라진다. [현재 abstract 메타데이터](https://arxiv.org/abs/2401.14452)의 저자 comment는 amplitude 오류 수정과 결과 갱신, 출판판 erratum 진행 중임을 명시한다. | [Relativistic interacting fluids 2406.01412v1](https://arxiv.org/html/2406.01412v1), 2024-06-03, §II의 pseudovector/패리티 위반 문장에서 [69]를 사용하고 참고문헌 [69]는 2401.14452로만 쓴다. v2보다 앞선 공개판이다. | “이 모델 계열이 parity-violating coupling을 논의하는가”는 양판 같은 답. “이 간단한 모델의 amplitude birefringence 한계를 쓸 수 있는가”는 v1 문서 주장에 비해 v2가 직접 반박한다. 그러나 후속 fluid 논문의 실제 인용 주장은 넓은 parity 위반이므로 그 논문까지 오류라고 판정할 근거는 없다. [CF-S13–16] |

## 세 보관 방식의 실제 차이

| 사건·관점 | 현재 주소만 | 판 지정 주소+시점 | 판+조건 위치+후보 근거를 함께 저장 |
| --- | --- | --- | --- |
| CF-I1 · 질문자/구현자 | “QUIC 문서”만 재방문하면 당시 최소 크기와 당시 parameter 명칭을 복원하기 어렵다. | -27과 -28을 다시 열 수 있으며 만료일도 분리된다. | “클라이언트 Initial/UDP payload/1200”을 §14에 연결하면 같은 답인 조건과 추가되는 peer 지원 조건을 나눌 수 있다. |
| CF-I2 · 편집자 | 초안명과 E.6만 저장하면 절 이동을 놓친다. | -27 E.6과 -28 E.6의 서로 다른 제목을 복원한다. | binder 검증 규칙은 §4.2.11, 새 identity 공격 설명은 -28 E.6이라는 별도 claim으로 보존한다. 되물을 값은 서버가 PSK만 받는지 인증서 방식도 받는지다. |
| CF-A1 · 링크 검색기 | 일반 arXiv 주소나 메타데이터만으로 v2 본문의 숫자를 대신할 위험이 있다. | v2 PDF를 다시 열어도 어떤 결과 칸을 채점했는지 모르면 상충을 해결하지 못한다. | 구조적 추천은 유지하고, EN-FR 수치 문턱은 abstract/§6.1/Table 2를 모두 연결하여 보류한다. 필요한 추가 자료는 해당 run의 평가 출력·checkpoint와 저자 정정이다. |
| CF-A2 · 질문자/편집자 | versionless 인용을 현재 v2로 풀면 2024년의 인용자가 2025년 정정까지 읽었다고 오인할 수 있다. | v1과 v2 및 후속 문헌 v1 시점을 저장하면 가능한 독서 범위를 좁힌다. | 실제로 인용한 claim이 parity 위반인지 amplitude 한계인지까지 저장해야 정정의 전파 대상이 갈린다. 전자는 두 판에서 지지되고 후자는 정정된다. |

이 비교에서 세 번째 방식이 더 많이 저장하는 이유는 문서 전체 복제에 있지 않다. **문서 ID, 판 ID, 표현 형식, 조건의 위치, 판독 시점, 판단의 범위**를 남겨 같은 링크가 지지하는 서로 다른 주장을 분리하기 위해서다. 후보 매뉴얼판은 본 조사에서는 jq/Pandoc 고정 태그에 해당하고, 이 대조에서는 문서의 고정 초안/프리프린트판에 해당한다. 두 분야의 효과 크기를 Stack Overflow 수정 빈도로 환산하지 않는다.

[arXiv 공식 version 정책](https://info.arxiv.org/help/versions.html)은 공개된 판을 역사 기록으로 보존하고 번호 없는 abstract 주소는 최신판을 보여 주며, 특정 판은 vX를 붙여 인용하도록 설명한다. 다만 제출 time stamp는 제출 버튼을 누른 시각으로 설명되어 있다. 이를 즉시 공개 시각, 인용자가 실제 읽은 시각 또는 파일을 실행한 시각과 같다고 간주하지 않는다. [CF-S17]

## 자가검산과 반례 탐색

1. **“모든 수정은 권고를 바꾼다”에 대한 반례:** QUIC 1200바이트 규칙과 TLS binder 검증 규칙을 다음판에서 다시 읽었다. 둘 다 유지된다. Transformer의 attention 구조, Kalb–Ramond의 일반적 패리티 위반 주장도 유지된다. 변경 여부는 문서 단위가 아닌 조건 단위다.
2. **“판 번호만 있으면 정답이 정해진다”에 대한 반례:** Attention v2의 abstract·§6.1·Table 2 숫자를 PDF와 HTML에서 대조했다. 같은 판 안의 상충이 남는다. 서로 다른 표현 형식을 같은 바이트로 취급하지 않는다.
3. **“오류가 정정되면 모든 후속 인용도 틀렸다”에 대한 반례:** 2406.01412v1의 실제 인용 문장은 parity violation이다. 정정된 amplitude 한계를 인용한 것으로 바꾸어 읽지 않는다.
4. **“후속 인용은 실제 실험/환경 확인이다”에 대한 반례:** IETF의 version-pinned reference는 문헌 인용, BERT의 구현 설명은 해당 저자의 서술, physics 논문의 인용은 논문 근거다. 여기서는 프로토콜 패킷 기록, BERT 학습 산출물, 새 물리 관측값을 보지 않았다.
5. **시간·표현 형식 주의:** Kalb–Ramond HTML에는 본문 렌더링 날짜와 arXiv 판 날짜가 다르게 나타난다. 판 식별은 페이지의 v1/v2 식별과 submission history를 사용했으며 HTML 본문 인쇄일을 최초 제출일로 사용하지 않았다. 렌더링 변화만으로 의미 변경을 판정하지 않았다.
6. **다른 경로의 음성 결과:** quic-tls-13의 TLS13 참고문헌은 예상했던 tls13-28이 아니라 -21이었다. 이를 -28 후속 인용으로 세지 않고, 실제 -28을 인용하는 rfc8447bis-00으로 교체했다. Adam 메타데이터와 여러 검색 결과는 탐색만 했으며 이 네 사건의 필수 원자료 수에 넣지 않았다.

## 완료 범위와 최소 후속 확인

- 타 분야 비교 사건: IETF 2/2, 학술 2/2.
- 원판/다음판/후속 인용 사슬: 4/4.
- 보존된 판 쌍: 4/4. 모두 원문 본문을 직접 열었으며 검색 결과 요약으로 대체하지 않았다.
- 직접 읽은 기록은 sources_cross_fields.jsonl 17행이다. 그중 동일 저작의 HTML/PDF/metadata 재표현 4행을 보수적으로 제외하면 원자료 단위 13개, 독립 저작 9개다. 비교 사건 자체의 독립성은 4개다. 전체 연구 sources 집계에서 같은 URL/저작을 다시 중복 합산하지 않는다.
- 여기서 원 사용자 실사용판과 도움/시간 절감 인과효과는 측정하지 않았다. 논문·초안의 주장 또는 후속 저자의 인용과 구별했다.
- 다음 최소 확인: Attention 수치의 저자 정정·평가 run을 확인하면 수치 문턱 보류가 풀린다. Kalb–Ramond의 출판 erratum 본문·DOI를 확인하면 “진행 중”이라는 메타데이터 수준을 출판 정정 수준으로 올릴 수 있다. 판별 조건이 동일한 본문 revision이 확보되면 두 분야 비교를 쌍별 코드로 확장할 수 있지만 본 연구의 SO 분모에는 넣지 않는다.
