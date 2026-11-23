# AF-RES-088 — 플랫폼·판 식별 대조

이 파일은 Q1·Q2·Q3·Q6의 플랫폼 근거다. jq/Pandoc 모집 질문·후속판·답은 읽지 않았다. 부모 작업자의 R0 사전 판정을 대신하거나 독립 판독 점수로 사용하지 않는다. 직접 열람은 2026-11-23 14:47–14:50 UTC, 마지막 확인 시계는 14:50:45 UTC다. 자료 22행은 **독립 저작·사건 8개**로 묶었다. API 문서의 여러 페이지, 한 질문의 이력·답·API를 독립 사건으로 불리지 않았다. `sources_platform.jsonl`의 시각은 배치 열람 종료 기록이며 정확한 개별 요청 시작 시각은 보존하지 못했다.

## 1. 첫판의 명칭과 식별

적절한 명칭은 **가장 이른 확인 가능한 공개 본문판**이다. `creation_date`가 같은 revision1을 찾았다는 사실은 최초 게시 직후 바이트의 별도 캡처가 아니다. 공식 revision schema 자체가 여러 편집이 한 revision으로 합쳐질 수 있다고 설명한다. 역사 정책판도 작성자의 일부 5분 내 변경이 첫 revision에 포함될 수 있다고 말한다. [PL01](https://api.stackexchange.com/docs/types/revision), [PL09](https://meta.stackexchange.com/revisions/21789/26).

2022-05-13 정책판은 2024 모집 기간 이전의 근거다. 해당 판은 최소10평판의 grace 편집, 타인 편집·댓글·답변·질문 닫힘에 따른 종료와 롤백 예외를 적는다. 이력 API에서 판26의 GUID `A5391373-9327-46A6-BB23-83BFE68902DC`, UTC `2022-05-13T21:16:22Z`, 편집자 Catija/user_id284336을 확인했다. body SHA256은 `54c24d93e96ea275dd6e277f2419629965636ae61037f633a9b249528505a06d`다. 현재 프로필 평판으로 당시 grace 자격을 추론해서는 안 된다. [PL20](https://api.stackexchange.com/2.3/posts/21789/revisions?site=meta.stackexchange&pagesize=100&filter=%216X_1Q338%29I5q6Nn_).

R0 식별에는 site·post_id·revision_guid·revision_number·creation_date·user·표현 형식과 본문 fingerprint를 함께 둔다. 질문의 최초 생성 시각과 본문 revision의 시각을 각각 둔다. 제목·태그·본문·롤백·보호/닫힘 등의 비편집 사건은 별도 코드로 둔다. 본문 필드가 없다는 것은 본문이 빈 문자열이라는 뜻이 아니다. 본문판을 시간순으로 재구성하고 제목-only나 tag-only 행에서는 앞 본문판을 유지한다. 각 행의 필드 부재는 먼저 필터가 해당 필드를 요청했는지 확인한 뒤 해석한다.

## 2. 필터·표현·페이지를 어떻게 고정하는가

공식 문서에 따르면 `withbody`는 기본 필터에 `*.body`를 더한다. 실제 Meta21788 조회에서는 `last_body`가 빠졌다. `body`는 HTML이며 safe/unsafe 필터에서 바뀌지 않는다. 현재 `question`에는 `body_markdown`이 있지만 `revision` 필드 목록에는 없다. 따라서 current-question Markdown과 historical-revision HTML의 hash 차이를 요구 변화로 세지 않는다. [PL04](https://api.stackexchange.com/docs/filters), [PL07](https://api.stackexchange.com/docs/types/question).

생성하고 실제 반환 필드를 확인한 revision 필터는 다음과 같다. 인증·유료 API를 사용하지 않았다.

```text
filter=!6X_1Q338)I5q6Nn_
base=none
unsafe=false
include=.backoff;.error_id;.error_message;.error_name;.has_more;.items;.quota_max;.quota_remaining;revision.body;revision.comment;revision.content_license;revision.creation_date;revision.is_rollback;revision.last_body;revision.last_tags;revision.last_title;revision.post_id;revision.post_type;revision.revision_guid;revision.revision_number;revision.revision_type;revision.set_community_wiki;revision.tags;revision.title;revision.user;shallow_user.display_name;shallow_user.link;shallow_user.user_id;shallow_user.user_type
```

공식 paging 규칙은 page1부터, pagesize 최대100, `has_more` 확인이다. Meta21788은12행, Meta17038은47행, Meta302285는5행, 정책 answer21789는30행이며 모두 pagesize100에서 `has_more=false`를 직접 확인했다. 보호·닫힘 같은 비본문 이벤트도 이 수에 들어간다. API 응답은 이 대조들에서 최근→과거였다. endpoint 문서의 보장으로 확대하지 않는다. [PL05](https://api.stackexchange.com/docs/paging), [PL17](https://stackapps.com/questions/8331/are-the-revisions-returned-by-posts-ids-revisions-guaranteed-to-be-returned-i).

API ordering에 관한2019년 원 조사도 역순 반환을 관측했지만 명문 보장은 못 찾았다. 그러므로 원 응답 순서·페이지 경계·has_more를 보존하고, 판 번호와 시각을 함께 검사한다. `creation_date`만으로 동시각 행을 합치지 않는다. 제안편집과 개선편집이 같은 시각을 가져 HTML과 Markdown이 서로 다른 판으로 선택된 실제 버그를 담당자가 고친 기록이 있다. 이것은 과거 수정된 사례이며 이번 API 오류를 관측한 것은 아니다. [PL18](https://stackapps.com/questions/8184/questions-returns-wrong-markdown-when-a-suggested-edit-is-improved).

모집 `/questions?sort=creation&order=asc&tagged=...`는 조회 시점 질문 객체의 태그 집합에 대한 목록으로 표시한다. API는 creation 정렬과 tagged의 AND 조건을 문서화하지만 과거 게시 당시 태그로 필터링한다고 약속하지 않는다. 초기 태그는 별도 revision1에서 검토하고, 삭제된 질문·나중에 태그가 제거된 질문까지 모집했다고 주장하지 않는다. 동일 생성 시각은 질문 ID로 로컬 순서를 고정하되 서버 원순서도 남긴다. [PL06](https://api.stackexchange.com/docs/questions).

## 3. 실제 제목-only 대조: Meta302285

이 사건은 jq/Pandoc 모집과 분리된 대조다. [공개 이력](https://meta.stackexchange.com/posts/302285/revisions), [API](https://api.stackexchange.com/2.3/posts/302285/revisions?site=meta.stackexchange&pagesize=100&filter=%216X_1Q338%29I5q6Nn_)을 모두 읽었다.

| 판 | GUID | UTC | 편집 주체·내용 | 본문 판별 |
| --- | --- | --- | --- | --- |
| 1 | 1120AD3B-C6C3-49FC-A58C-093926CDCDAF | 2017-10-19T09:25:48Z | insertusernamehere/user_id190341, 보존된 첫판 | body 있음 |
| 2 | 6A41C240-C97B-42B2-8FA8-4DE629C70B76 | 2017-10-19T10:11:14Z | 같은 작성자, 제목에서 `Code snippets`를 `Some parts of code snippets`로 한정 | title/last_title 있음; body/last_body 없음 |
| 3 | BF8D0170-67C0-40FD-BCE3-039C1FA032C1 | 2017-10-19T15:21:46Z | 같은 작성자, 본문 보충 | last_body가 판1.body와 같음 |
| 4 | 0F3BD445-0EC0-4854-B23E-D4BEF2A3206D | 2017-10-20T08:11:31Z | 같은 작성자, 도입부 축약 | 별도 본문 수정 |

판1.body와 판3.last_body의 동일 SHA256은 `2f8c1a39c33b5a3242038b4777829bc3b274e0913348f99db592255b74115c03`이다. 판2는 제목 변화이며 본문 수정층의 자격 근거로 쓰면 안 된다. 그렇다고 모든 제목 변화가 의미 없다고 주장하지 않는다. 제목까지 조건 출처로 삼는 계약이라면 제목의 범위 한정도 별도 의미 코드로 다뤄야 한다.

질문 `creation_date=1508405148`은 판1 시각과 일치한다. 그러나 게시 직후 별도 캡처를 확보하지 않았으므로 엄격 최초 게시 바이트는 **미확인**이다. [PL22](https://api.stackexchange.com/2.3/questions/17038;302285?site=meta.stackexchange).

## 4. 실제 롤백·표현-only 대조: Meta17038

[질문과 설명](https://meta.stackexchange.com/questions/17038/what-is-a-rollback), [공개 이력](https://meta.stackexchange.com/posts/17038/revisions), [전체 API](https://api.stackexchange.com/2.3/posts/17038/revisions?site=meta.stackexchange&pagesize=100&filter=%216X_1Q338%29I5q6Nn_)을 읽었다. 1–3판은 실제 타인 편집과 작성자 롤백의 순서다.

| 판 | GUID | UTC | 편집 주체 | 관측 |
| --- | --- | --- | --- | --- |
| 1 | 4351BDD6-20CB-4ED5-8E62-E4B335D7DF6C | 2009-08-24T18:46:24Z | Andrei Rînea/user_id1796 | 보존된 첫 본문 |
| 2 | 77297697-26E8-4226-87BC-50A638E99C6E | 2009-08-24T18:48:32Z | Welbog/user_id52443 | 롤백 시연용 문구 추가 |
| 3 | 8D3D6C5D-F7B6-4BB2-BA5F-7B6D77EF2C93 | 2009-08-24T18:50:20Z | Andrei Rînea/user_id1796 | is_rollback=true, 판1 본문 복구 |

판1·3의 HTML SHA256은 `761f45c2422c02922f9472626ba75379aeb256ec072bf1352790c4bb41c1a152`로 같다. 판2는 `4f5094e659d9dca9fb56df1b30ce41760fcdff15b9100add7d4f9282a3e09143`다. 롤백은 원래 시각의 판을 다시 쓰는 사건이 아니라 새 시각·GUID를 가진 사건이다. 질문 `creation_date=1251139584`가 판1과 일치하지만 최초 게시 바이트의 동시대 캡처는 확보하지 않았다.

같은 질문의 후반 이력은 **본문 지문 변화가 의미 변화와 일치하지 않는** 반례다.

| 판 | GUID | UTC | 종류 | 본문 지문 그룹 |
| --- | --- | --- | --- | --- |
| 34 | 674F96A4-822D-493B-986D-C4F0B395623A | 2019-09-23T17:05:51Z | 판32로 rollback | A |
| 35 | 92985F26-0253-416F-B2F2-AC8B848DACA6 | 2020-06-03T13:30:57Z | Community의 Commonmark migration | B |
| 36 | CAC760D4-4B24-4400-9DBE-3FA4EDB9E322 | 2020-06-24T18:13:28Z | 판34로 rollback | A |
| 37 | 2B5BEFFB-379A-4E48-89DD-9757822C81E5 | 2020-06-24T18:19:09Z | 판35로 rollback | B |

A의 HTML SHA256은 `027cfece353878ed41a9259f8aa4224716fc275bdaf568ad46fb40ed6f59a906`, B는 `ad2fcf0f5c72518af1adafc11c45307cc51706399fed58421e4dcf97bf117623`이다. 아래의 보조 텍스트 정규화 hash는 네 판 모두 `3009150f8b729e5a8bdf3ad92fe167a03978e8745d11312a17d77676fb372edb`였다. 직접 본문을 읽으면 인용 블록 경계가 달라지고 롤백 의미를 묻는 요구는 유지된다. 정규화 hash는 의미 판독의 보조이며 태그·링크·코드 의미를 지우므로 일반 의미동일 판정기로 쓰면 안 된다.

```python
import re, html, hashlib
text = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', body))).strip()
text_sha256 = hashlib.sha256(text.encode()).hexdigest()
html_sha256 = hashlib.sha256(body.encode()).hexdigest()
```

## 5. 채택·실사용판·효과의 근거 수준

공식 Help는 채택을 질문자의 개인적 선택으로 설명하며 완전한 최종 해결 선언으로 삼지 않는다. 따라서 다음은 각각 별도 열이어야 한다. [PL10](https://stackoverflow.com/help/accepted-answer).

| 관측 | 지지하는 것 | 추가로 필요한 것 |
| --- | --- | --- |
| 답변자가 코드·데모를 게시 | 답변자가 제안하거나 시연한 해법 | 질문자 실행·입출력·환경 기록 |
| 현재 accepted_answer_id | 조회 시점 선택된 답의 식별 | 당시 채택시각, 채택 변경 여부 |
| 질문자가 후속 입력·출력을 게시 | 그 발언이 보고하는 실행 결과 | 실제 프로그램판과 재현 가능 입력의 연결 |
| 프로그램판 번호를 말함 | 그 문구의 자기보고 | 해당 판으로 그 입력을 실행했다는 연결 |
| 답이 없거나 채택이 없음 | 확보 범위에서 응답/채택 미관측 | 삭제·외부 해결·미복귀 가능성; 실패나 무효과로 단정 금지 |

도움과 시간 절감의 인과효과는 이 표지만으로 측정되지 않는다. 또한 본문에 해법 이름이 추가된 순서를 알아도 그 답을 읽었기 때문에 수정했다는 인과는 별도 근거가 필요하다. 답 최초판·댓글·질문 수정시각·질문자 진술을 시간순으로 조인한 뒤에도 단순 선후와 명시적 자기보고를 구분한다.

## 6. 반례와 남은 한계

1. **생성시각 동일≠즉시 게시 바이트.** 302285·17038에서 시각 일치는 확인했으나 동시대 외부 캡처는 없다. 판단을 바꾸려면 해당 질문의 생성시각 직후 원문을 고정한 실제 보존본과 revision1의 바이트를 대조해야 한다.
2. **revision·hash 변화≠요구 변화.** 제목-only와 CommonMark/롤백의 실제 사건을 확인했다. 반대로 제목 한정이나 코드의 공백이 의미를 바꿀 수 있으므로 모든 표현 차이를 버리는 규칙도 틀린다. 필요한 입력은 같은 형식의 원문 두 판과 위치별 의미 대조다.
3. **채택≠실사용판·효과.** 공식 정책은 개인적 선택을 뒷받침한다. 실제 프로그램판·동일 입력·질문자 출력·시각이 연결된 후속 기록을 확보해야 실행과 결과에 대한 판정을 강화할 수 있다.

이 파일은 플랫폼 연구의 자체 검산이며 jq/Pandoc 8자리의 조건 판독이나 독립 이중 코딩이 아니다. API 문서의 현행 내용과 2019년 버그·2022년 정책·2017년 대조 사건은 각각의 시점에 한정했다. 모집 표본은 부모의 고정 원목록만 사용해야 한다.
