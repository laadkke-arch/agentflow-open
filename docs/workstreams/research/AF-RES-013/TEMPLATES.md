# 계열별 입력 절·비교 절·도입 이력

본문과 저장소 이력을 직접 열어 확인했다. 아래 날짜는 명시한 Git 작성·통합 사건의 날짜다. 특히 저장소의 최초 커밋 날짜를 인터넷에 처음 공개된 날짜로 확대하지 않는다. 원문 URL·확인 범위·한계는 각 사례 조사자의 sources와 통합 sources에 연결한다.

| 계열 | 결정 전 입력으로 허용한 범위 | 관측 정답을 추출한 비교 절 | 템플릿·절차의 이력 | 이번 표본에 미치는 영향 |
|---|---|---|---|---|
| Rust RFC | Summary의 목적 문장, Motivation. 해법·선례명·링크 제거 | Alternatives, Drawbacks / alternatives. 본문에 반영 안 된 리뷰는 별도 pool | [최초 template](https://raw.githubusercontent.com/rust-lang/rfcs/14ca6f655066058b886eac1dcc4017af0d22c2f5/0000-template.md), 2014-03-10에 Alternatives 존재. [2017-07-19](https://raw.githubusercontent.com/rust-lang/rfcs/4a3f5c5570b4ae5940aa0c4d0d62b4e79aabeeb1/0000-template.md)에 Rationale and Alternatives로 변경. Prior art는 [2018-02-12 작성판](https://raw.githubusercontent.com/rust-lang/rfcs/f08f881847850d5d587e3504088a11fad766e51b/0000-template.md), [2018-02-27 통합판](https://raw.githubusercontent.com/rust-lang/rfcs/a488ca0263dc4e8ee495ef9b6ca0d9d5d7fbc790/0000-template.md)으로 확인 | 선정8개는 모두2014년으로 명시 Prior art 유도절보다 이르다. 내부 문법·명명 대안이 많은 표본을 현대 RFC의 인용 관행 전체로 일반화할 수 없다. |
| Python PEP | 초기판의 Abstract/Introduction/Motivation/Rationale/Goals/Non-goals 중 문제만 분리할 수 있는 문단 | Rationale의 명시 비교, Alternatives, Rejected Ideas, Open Issues의 구별되는 대안. 일반 참고문헌은 제외 | [PEP1 내용 지침](https://raw.githubusercontent.com/python/peps/86fcb76ff6763002f89de3309de9de83cac21ba7/pep-0001.txt)은 2000-07-25부터 관련 대안·다른 언어 선례·반대 의견을 Rationale에 요구. [PEP12 초기판](https://raw.githubusercontent.com/python/peps/9ca8e6bba0d828c067d3c101fe204a74584e275e/pep-0012.txt)은 2002-08-26의 형식 안내. [2019-03-08판](https://raw.githubusercontent.com/python/peps/8e7b03ab1da7c26ff75cf152e075bebe96f567a1/pep-0012.rst)에 Rejected Ideas 등 실제 절 골격 추가; [이전 파일 판](https://raw.githubusercontent.com/python/peps/d69b083262d844a70735f6a9ef889acc0e2a8867/pep-0012.rst)에는 없음 | 오래된 PEP는 Rationale 안에 문제와 대안이 함께 있다. 제목 기준의 자동 절 절단만으로 입력을 만들 수 없다. Python9개에는 2000년 문서와2017년 초안/2023년 대체 결정을 함께 포함하므로 사건·판을 별도 보존한다. |
| Swift Evolution | Introduction/Motivation의 문제·기존 어려움 문단 | Alternatives considered. 수락 리뷰에만 있는 대안은 별도 pool | [root template d444b1f8](https://raw.githubusercontent.com/swiftlang/swift-evolution/d444b1f8b827e759d6c18c9b0246cb882d8f16a1/0000-template.md)의 작성/committer 시각은 2015-11-03이며 부모 없음. 최초 저장소 판부터 Introduction, Motivation, Proposed solution, Detailed design, Alternatives considered 분리 | 초기 일부 제안은 최초 복구 판부터 Accepted여서 제외했다. 수락 공고일과 문서 Status 변경일은 다를 수 있어 둘을 섞지 않았다. |
| Kubernetes KEP | Summary/Background/Motivation/Goals/Non-Goals. 구 design-proposals 원문이면 대응하는 문제 문단 | Alternatives / Considered alternatives / Alternatives and further reading 중 실제 비교 대상 | [최초 템플릿 제안 e99752b8](https://api.github.com/repos/kubernetes/community/commits/e99752b8f06125ce5b9dbc6e7eba4f108ab9f32a)에 Alternatives 존재(작성2017-08-31, committer2017-09-26). [독립 복사용 파일 b01d0a7c](https://api.github.com/repos/kubernetes/community/commits/b01d0a7c1564fe0562d99b32608c4dd84136840d), 2017-09-26. [Goals/Non-Goals 독립 절 추가 1f9a673a](https://api.github.com/repos/kubernetes/community/commits/1f9a673ae08e7767f1f5198dbb0b2ae588f00032), 작성11월13일/committer11월14일. 현재 경로의2020년 생성은 최초 도입이 아님 | 6개 중3개는 enhancements로 옮기기 전 community의 실제 결정판으로 되돌아갔다. 저장소 이전/KEP 편입을 최초 설계 수락으로 세지 않았다. |

## 방법과 원장

- Rust: `evidence/cases-rust/TEMPLATE.md`, `template-history.json`, `sources.json`. path history38개 중36개의 heading을 확인했지만, heading 검사만 한 판은 본문 열람 최소수에 넣지 않는다.
- Python·Swift: `evidence/cases-ps/sources.json`의 PS-T 계열, `SEARCH_LOG.json`, history metadata. 현행 [PEP1](https://peps.python.org/pep-0001/)·[PEP12](https://peps.python.org/pep-0012/)도 직접 읽어 역사판과 구별했다.
- KEP: `evidence/methods/TEMPLATE_KEP.md`와 M17–M21, `evidence/cases-kep/OBSERVATIONS.md`. 템플릿 지침과 실제로 채워진 사례는 별개다.
- root 재검증: `evidence/TEMPLATE_VERIFICATION.json`은 Swift root/PEP1 대안 지침/PEP12 절 추가의 작성·committer 날짜와 부모를 다시 읽은 기록이다.

## 정답원으로서 확인한 한계

**절이 있다는 것과 외부 선행 사례가 있다는 것은 다르다.** Rust의 명명 후보, Swift의 구문 선택, KEP의 자체 API 구성은 독립적인 비교 항목이지만 세상에 존재하는 제품·논문의 고유 식별자는 아니다. 각 항목에 structural_design과 external_entity를 따로 기록한다.

**내용은 리뷰와 함께 바뀐다.** SE0022의 initializer 대안은 수락 리뷰에서 기각되고 본문에 반영됐지만, 암묵 변환과 `.selector` 멤버는 수락 토론에만 있다. 이 둘은 primary 본문 분모에 몰래 더하지 않고 review pool로 보존했다. Rust RFC123의 Sync 제안과 Clojure atom 명명 비유도 같은 방식으로 구분했다.

**현재판의 문제 절이 처음 문제와 같다는 보장은 없다.** PEP642 토론에는 게시물과 Abstract·Motivation을 수정했다는 기록이 있다(M26). 본 연구는 이 경고에 따라 각 사례의 수락 전 판을 따로 고정하고 요약했으며, 최종 해법·대안명을 제거했다. 이 요약도 연구자의 변환이다.

**날짜와 인용의 설명도 틀릴 수 있다.** K0383의 현행 회고 날짜와 원 PR 병합 날짜가 다르고, K0127은 한 댓글을 설명한 문장과 실제 댓글의 권고가 맞지 않는다. PEP435가 회고한 PEP354의 기각 연도도 최초 초안·상태 변경 이력과 맞지 않는다. 정답 항목의 기록 여부와 그 설명의 사실성을 동일시하지 않았다.

## 한계

네 계열을 실용적인 정답원으로 구성할 수 있음을 확인한 것이며 Go·TC39·IETF·공개 ADR 계열의 전체 품질을 평가한 결과는 아니다. Git 이관 전의 외부 초안과 모든 리뷰 수정 경로를 복원하지 못한 경우는 각 사례에 남겼다. Rust5개의 역사적 merge object가404여서, 그 사례는 복구한 수락 전 PR head와 공식 병합 시각을 분리해 사용한다. 템플릿 지침이 저자의 실제 탐색 범위·노력·효용을 입증하지 않는다.
