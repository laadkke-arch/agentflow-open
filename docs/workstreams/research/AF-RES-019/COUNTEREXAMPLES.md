# 반례 검토 원장

| 반례 탐색 | 쓴 질의·자료 | 확인한 내용 | 적용 한계 |
| --- | --- | --- | --- |
| 활동은 정상이나 이유가 사라짐 | Firefox Send 영구 종료 공지와 B03의 Git 12개월 경보. Directus 같은 날 공지와 ESLint 9 제거 PR도 확인. | B03은 기간 중 계산된 신호 10종이 각각 임계값을 넘지 않았다. 영구 종료 공지는 2020-09-17이었다. C07도 11종에 양성이 없었다. A07의 T−1개월 11종은 정상이나 CLA가 21일, 매니페스트가 1일 전에 경보했다. | 파이어폭스의 임시 서비스 중지가 여름에 이미 있었다. Git만 정상인 사례다. 미관측 레지스트리 이력을 정상으로 간주하지 않았다. |
| 경보와 1년 이상 이유 유지 | C-E02 Less의 T−12부터 T+365, Apache 계열과 배포 유지. C-A07 Keystone README의 유지 모드 대상 버전을 고정판 세 개에서 확인. | Less는 커밋 정체·태그 길이가 경보했지만 2025-07-24에도 동일 CSS 전처리 목적이 문서상 지속됐다. Keystone 6의 MIT 조건은 지속됐고 공지 표현은 별 저장소의 Keystone 5를 가리켰다. | 실행 호환이나 장기 새 사용자의 품질은 미측정이다. C-A07의 태그는 별도로 경보했다. |
| 긴 기간의 공지를 요청 시 발견 | 2017-07-25 Adobe Flash 발표와 EOL FAQ, B04 요청 365일 위상 재생. | 지원 종료까지 1,255일이었다. 시작일이 공지보다 2년 이상 뒤인 재생에서도 모든 표본 위상에서 요청 시 시행 전 확인했다. | 재요청이 없는 이용자는 포함하지 않았다. 런타임 차단은 2021-01-12이므로 적용 범위에 따라 날짜가 다르다. |
| deprecated 뒤에도 기존 의존이 남고 대체가 어려움 | request 유지자 이슈 #3142, npm의 126판 표시, npm 다운로드 GET, Cypress 포크, Python 폐기 연구의 대체 조사. | 기존 판 및 Cypress 목적의 포크는 남았다. request 담당자가 2019년 기존 npm 코드·교육 자료에서의 큰 노출을 설명했다. 원 개발자는 모든 사용법을 대신하는 단일 구현을 지정하지 않았다. | 현재 대규모 이용은 npm 다운로드 호스트 CONNECT 403으로 미확인이다. 포크가 있어 모든 적용에 대체가 없다는 명제도 미확인이다. |
| 재번복 또는 후속 포크 | Redis 7.4 LICENSE 및 8.0 공지, Elasticsearch AGPL, Google kaniko archive와 Chainguard 포크. | Redis 8.0은 공개 소스 옵션 AGPLv3를 더했다. kaniko 기존 주소는 읽기 전용이고 포크가 계속 배포할 의사를 밝혔다. | 라이선스 선택지 추가는 7.4 전환을 소급 무효화하지 않는다. 포크 호환과 지원 범위는 따로 시험해야 한다. |

## 직접 자료와 재개 입력

- B03 Firefox Send 공지. [게시물](https://blog.mozilla.org/en/uncategorized/update-on-firefox-send-and-firefox-notes/)
- A07 Directus와 C-A07의 버전 범위. [v10 릴리스](https://github.com/directus/directus/releases/tag/v10.0.0) · [2022 고정판](https://github.com/keystonejs/keystone/blob/3bb1a53434b86e8a6294cff01a8699c36dd5df5a/README.md#L36) · [2023 고정판](https://github.com/keystonejs/keystone/blob/818b0b61a1367c39fdc4d2b91f69fe8a4a157adc/README.md#L57) · [2024 고정판](https://github.com/keystonejs/keystone/blob/a9d1d222657a1ee14cf3d03a0fdee64f046764bf/README.md#L58)
- E01 기존 이용과 대체. [완전 폐기](https://raw.githubusercontent.com/request/request/master/README.md) · [관리자 이슈](https://github.com/request/request/issues/3142) · [Cypress 포크](https://github.com/cypress-io/request)
- 재번복. [Redis 8.0](https://github.com/redis/redis/releases/tag/8.0.0) · [Elastic FAQ](https://www.elastic.co/pricing/faq/licensing) · [kaniko 원본](https://github.com/GoogleContainerTools/kaniko) · [유지 승계 공지](https://www.chainguard.dev/unchained/fork-yeah-were-bringing-kaniko-back)
- C04 알려진 나쁜 후보. [SciPy 1.12 코드](https://raw.githubusercontent.com/scipy/scipy/v1.12.0/scipy/linalg/_special_matrices.py) · [SciPy 1.13 코드](https://raw.githubusercontent.com/scipy/scipy/v1.13.0/scipy/linalg/_special_matrices.py)

공개 통계 접근이 허용된 환경에서 사용할 입력이다.

```sh
curl --fail --silent --show-error --max-time 20 'https://api.npmjs.org/downloads/point/last-week/request'
```

현재 다운로드의 한 주와 역사적 의존성 또는 드롭인 대체의 존재는 다른 자료를 요구한다. 다운로드 창·분모와 대체 호환성 시험을 각각 보존한다.
