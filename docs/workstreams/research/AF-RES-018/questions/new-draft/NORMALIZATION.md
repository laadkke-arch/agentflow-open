# 새 질문 원문 확보와 해시 정규화

## 동결 자료와 실행 입력의 구별

`new-questions.json`은 부모 작업자가 질문 묶음 커밋 `fe8ad7f20ff387801d0e6af97c9c98f90e3fc081`에서 동결했다. 이 디렉터리의 질문 해시는 수집 단계 정규화에 해당한다. 부모의 `questions.generate.text_of`가 산출하는 실행 입력 해시는 별도로 검증되며, 두 함수가 다르면 해시가 같을 필요가 없다. 답변·필수 조건 코딩·whole/part/I5·gold는 A/P 질문 입력으로 보내지 않는다.

SE 9개는 revision_number=1과 revision_guid를 직접 확인했다. 현재 페이지를 읽었다는 이유만으로 최초판으로 승격하지 않았다. HN 10개와 GitHub 1개는 현재 질문 본문 및 게시 시각을 확인했지만 초기 이력을 복원하지 못했으므로 **요약 실행 입력**이다.

## Stack Exchange와 Hacker News

수집 해시 함수 `se_v1_html_tag_regex_then_html_unescape_preserve_whitespace`는 다음과 같다. HN API의 HTML 질문에도 같은 함수를 사용했다.

```python
import hashlib, html, re

def text_of_collection(body_html):
    return html.unescape(re.sub('<[^>]+>', ' ', body_html or ''))

text = text_of_collection(body_html)
text_sha256 = hashlib.sha256(text.encode('utf-8')).hexdigest()
html_sha256 = hashlib.sha256((body_html or '').encode('utf-8')).hexdigest()
word_count = len(text.split())
```

이 함수는 공백을 합치지 않는다. 제목은 저장하지 않으며 해시에 포함하지 않는다. 단어 수는 언어학적 단어 분할이 아니라 Python 공백 분할이다. 본문은 메모리에서 읽고 해시·개수·요약만 기록했다. 일부 개정 이벤트는 본문을 포함하지 않아 빈 문자열 해시와 0단어가 기록된다. 그런 이벤트를 최초 질문 원문으로 사용하지 않는다.

SE 재현 입력은 각 행의 `revision_loader_url`이다. 예를 들어 N001의 GUID는 `4AAB8DFA-04DF-47AD-8734-FD8A7B38088D`이다. API 응답 중 해당 GUID, post_id, revision_number=1과 비어 있지 않은 body를 확인하고, 부모 실행 로더는 질문만 런타임에 출력한다. 사용자 본문을 파일에 저장하는 명령은 사용하지 않는다.

HN의 `https://hn.algolia.com/api/v1/items/<id>`에서는 루트 항목의 `text`만 질문 해시에 사용했다. `children`은 gold를 준비하는 작업자만 열람했다. 질문 날짜는 루트 `created_at`이며, 답글 날짜나 마지막 갱신일로 대체하지 않는다. OP 여부는 메모리에서 작성자를 비교해 boolean만 기록했다.

## GitHub Discussions

수집 함수명은 `gh_v1_first_td_js-comment-body_regex_then_html_tag_regex_html_unescape_preserve_whitespace`이다.

```python
body_html = re.search(
    r'<td\s+class="[^"]*js-comment-body[^>]*>(.*?)</td>',
    page_html, re.S
).group(1)
body_text = html.unescape(re.sub('<[^>]+>', ' ', body_html))
```

첫 질문 본문만 해시했다. 날짜는 정상 공개 HTML의 첫 질문 `relative-time` 요소에 있는 절대 `datetime`과 본문 게시일을 대조했다. 이 절대 시각은 `2026-07-02T19:18:55Z`이며, 접근 시각은 `2026-11-21T04:02:08.300129+00:00`이다. 현재 질문 307단어, text SHA-256은 `dbfa37d8461562923b610b21fba8b2e7265268ef4d6c1607405d0d0b10d74323`이다. 이전 수정 이력이 없으므로 질문 시점 판이라고 주장하지 않는다.

## Reddit 보조 표본

웹 열람 도구에서 현재 본문과 답글을 직접 읽었고, 질문 줄만 메모리에서 정규화해 해시했다. 검색 도구는 절대 게시일을 표시했으나 직접 열린 페이지는 상대 시각 중심이었다. 정상 HTML 200 응답 7개는 본문·날짜 메타데이터가 없는 bootstrap이었다. JSON 경로 403 이후 재시도하거나 우회하지 않았다. 따라서 7개 모두 본 표본에서 제외하고 `supplementary-reddit-questions.json`에 보존했다.

## 한계

HTML 정규화는 플랫폼 DOM 변경에 취약하다. HN/GitHub 현재 본문은 게시 시점 이후 변경됐을 수 있다. 접근 시각을 먼저 측정한 API/HTML 요청은 정확한 시각을 남겼고, 앞선 웹 도구 호출은 정확한 초가 남아 있지 않아 세션 시작~기록 시점 구간으로만 적었다. 이 구간을 정확한 열람 초로 사용하지 않는다.
