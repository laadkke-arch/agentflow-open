# 외부 표준·전거 비교 — AF-RES-079

판독자: `standards_evidence` 도구 에이전트. 자연·대조 사건의 첫 판정 파일은 열지 않았다. 이 비교의 분모는 **실제 외부 이력 2건/2자리**이며 자연 8자리나 대조 3자리와 합산하지 않는다. 원문 계보는 **7건 산입, 추가 직접 열람 1건 미산입, 접근 실패 5건**이다. 근거 행은 [sources.jsonl](sources.jsonl), 데이터는 [external-records.json](external-records.json), 현재 GET 영수증은 [http-receipts.jsonl](http-receipts.jsonl)에 있다.

## 직접 연 두 이력

| 기록 | 원 등록부와 발행자의 변경 설명 | 수신자 역확인 | 수선에 옮길 규칙 | 아직 확인하지 않은 것 |
| --- | --- | --- | --- | --- |
| EXT01 · IANA `mo → ro` | [현재 등록부](https://www.iana.org/assignments/language-subtag-registry/language-subtag-registry) File-Date 2026-11-18, `Type=language/Subtag=mo`: 폐기일 2008-11-22와 단일 `ro` 선호값. [수신 ro 등록 신청](https://www.iana.org/assignments/lang-subtags-templates/ro.txt) 2008-11-25: 원 표준의 2008-11-03 폐기와 명칭 이전을 설명한다. STD-S01/S07. | 같은 등록부의 ro 레코드가 존재하며 옛 명칭을 함께 가진다. | 원 ID·옛 인용은 보존하고, namespace와 시행일을 갖춘 단일 방향 선호값을 추가한다. ISO639-3의 `mol/ron`와 IANA의 `mo/ro`를 섞지 않는다. | 원 ISO639-2 결정표 본문과 당시 HTTP 이동 이력. |
| EXT02 · IANA `bhk → {fbl,lbl,rbl,ubl}` | [bhk 등록 신청](https://www.iana.org/assignments/lang-subtags-templates/bhk.txt)은 원 표준의 2010-01-20 분할을 명시한다. 현재 등록부에는 2010-03-11 폐기와 네 후속 코드 참조가 있고 단일 선호값은 없다. STD-S01/S06. | 네 수신 레코드 모두 존재하며 Added=2010-03-11, Macrolanguage=bik이다. | 네 관계를 보존한다. 옛 자료의 내용이나 지역 등 구별 근거가 없으면 한 목적지로 자동 수선하지 않는다. | 특정 옛 bhk 자료가 네 코드 중 어디에 해당하는지, 링크된 SIL 결정 PDF의 원문. |

## 실제로 찾은 반례와 한계

1. **문서 파일명이 맞아도 사건의 판이 다를 수 있다.** [mo.txt](https://www.iana.org/assignments/lang-subtags-templates/mo.txt)는 2008-07-23의 앞선 명칭 보강 신청이다. 11월 폐기의 근거로 사용하면 잘못이다. 이 문서는 반례로 읽었고 최소 원저작 수에는 보수적으로 넣지 않았다(STD-S08).
2. **폐기와 단일 대체는 다르다.** [RFC5646 §3.1.6–3.1.7·3.4·4.5](https://www.rfc-editor.org/rfc/rfc5646.html#section-3.1.6)는 선호값 없는 폐기에 대체 매핑을 부여하지 않는다. 일부 region 선호값은 옛 값과 정확히 같은 의미가 아닐 수 있다. 바뀌지 않는 키와 갱신 가능한 관계를 분리하는 원칙은 가져올 수 있으나, 소프트웨어 행동의 동일성은 별도 근거가 필요하다(STD-S02).
3. **네트워크 주소 동등성과 원 기능 절 동등성은 다른 검사다.** [RFC3986 §3.5·6.1](https://www.rfc-editor.org/rfc/rfc3986.html#section-3.5)은 fragment를 역참조 전에 분리한다. [RFC8141 §3](https://www.rfc-editor.org/rfc/rfc8141.html#section-3)에서는 URN 동등성 비교 시 fragment가 제외된다. 이 규칙을 원 기능 절의 보존 판정에 그대로 사용하면 부분 대상이 달라진 것을 놓칠 수 있다. resolver의 주소 매핑 갱신도 필요하다(STD-S03/S04).
4. **옛 근거를 보존하는 것과 잘못된 이름을 유효한 별칭으로 승인하는 것은 구분해야 한다.** [LC NACO FAQ Q3·12·17·20](https://www.loc.gov/aba/pcc/naco/personnamefaq.html)은 중복 취소 시 유용한 근거를 이관하고, 구별 정보가 없으면 전거 생성을 보류할 수 있게 한다. Q12는 실제로 사용하던 이전 이름과 오기 수정을 구분한다. 오류로 확인된 문자열은 감사 이력에 남겨도 활성 별칭으로 만들 필요는 없다. 이 문서는 실제 개별 전거 합병 사례로 세지 않았다(STD-S05).

## 소프트웨어에 옮길 범위

재사용 가능한 기록 요소는 `old_namespace/id`, `new_namespace/id[]`, 관계 종류·방향, 선언 발행자, 선언일·적용판, 옛 근거, 새 근거, 현재 관측시각, 보류 이유다. 명칭·위치 변경과 분할·대체를 한 관계로 압축하지 않아야 한다. 관계를 새로 추가해도 옛 인용을 새 문서의 주장으로 덮어쓰지 않는다.

표준의 선호값이나 전거의 병합 규칙으로는 소프트웨어의 import 가능 여부, 입력 순서·자료형, 정보 손실, 쓰기 기능, 오류 조건을 알 수 없다. 그 부분은 해당 판의 구현·공급자 시험 또는 직접 실행이 필요하다. EXT02의 최소 재개 입력은 옛 자료 하나를 네 후속 범위 중 하나와 연결하는 구별 근거다. EXT01에서 표준 발행자의 원 결정 자체를 추가로 요구한다면 접근에 실패한 ISO639-2 변경표의 해당 행을 확보해야 한다.

## 실행·접근 경계

웹 도구로 RFC 3개·등록부·등록 신청 3개·LC FAQ의 지목 절을 직접 읽었다. 셸 GET에서 IANA·RFC 본문은 200을 관측했고 주소의 redirect chain은 비어 있었다. LC FAQ는 웹 본문 열람에 성공했지만 셸은 403이었다. MARC 682는 웹 429/셸 403으로 실패했으며 내용을 인용하지 않았다. SIL 두 코드와 retirement 표도 403으로 실패하여 산입하지 않았다. 현재 응답으로 과거의 redirect를 추정하지 않았다.

읽은 표준을 소프트웨어에 적용하는 것은 본 연구의 설계 추론이다. 위에서 확인한 것은 해당 원문이 실제로 선언한 관계와 규칙까지다.
