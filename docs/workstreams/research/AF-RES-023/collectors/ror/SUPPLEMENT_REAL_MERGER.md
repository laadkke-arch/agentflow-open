# 실제 기관 합병과 카탈로그 반영은 서로 다른 사건이다

이 보강은 본 core 6개 및 기존 supplement 2개와 분리한다. 시스템당 최대 8개 산입을 넘기지 않기 위해 `events.jsonl`에 추가하지 않았으며 아래 자료는 `supplement-sources.json`에서 `counted=false`다.

## ROR-X1 · PPS + LIAFA → IRIF

| 층 | 직접 읽은 근거 | 관측 |
|---|---|---|
| 현실 연구조직 합병 | ROR-X03: [대학 UFR 공식 소개](https://www.informatique.u-paris.fr/ufr/presentation_ufr), Recherche L136–147, 수정표시2025-10-15 | LIAFA와 PPS가 **2016-01-01** 합쳐져 IRIF가 생겼다고 설명한다. |
| ROR 편집 요청 | ROR-X01: [#43488](https://github.com/ror-community/ror-updates/issues/43488), 2026-10-30 | PPS `046p9e825` inactive 및 IRIF `02krdtz55` successor를 제안한다. |
| 고정된 변경파일 | ROR-X02: [rc-v2.16 PPS](https://github.com/ror-community/ror-updates/blob/baffbf2b52cf09acd3dc29ef808d91c4a1aca278/rc-v2.16/updates/046p9e825.json), admin.last_modified2026-11-19 | inactive와 IRIF successor가 기록되고 옛 PPS 이름·사이트·외부IDs가 남는다. |
| 배포 진술 | [#43488 comment7034410094](https://github.com/ror-community/ror-updates/issues/43488#issuecomment-7034410094), issue 종료2026-11-20 | 발행자가 releasev2.16 반영을 알린다. 전체 배포 dump 검증은 아니다. |

현실 합병일과 카탈로그 편집일 사이에 약 10년의 차이가 있다. 이를 “ROR가 2016년부터 wrong redirect였다” 또는 “10년간 이용자 피해가 있었다”로 바꿀 근거는 없다. 직접 본 것은 2016년 현실 합병을 설명하는 기관 원문과 2026년 해당 ROR 변경이다. 그 사이 모든 ROR판을 읽지는 않았다.

대학 원문의 연구목표는 합병한 기관의 기능을 설명하지만, 옛 PPS 논문의 소속기관을 IRIF로 소급 고쳐야 한다는 지시는 아니다. ROR-S01의 역사적 소속보존 원칙과 결합하면, 현재 연구접촉의 후계와 과거 논문의 당시 소속은 서로 다른 정답일 수 있다. 이것은 연구자의 적용 해석이다.

#43488이 링크한 IRIF 자체 소개는 web에서 restricted URL로 열리지 않았다. 이어서 검색으로 찾은 별도 공식 대학 도메인의 자료를 직접 열었다. 접근제어 우회나 로그인은 하지 않았다. 실제 열람한 문서는 대학 UFR 소개이며 법적 합병 공고 자체는 미확인이다.

## ROR-X2 · IMiF 합병 설명은 있으나 카탈로그 반영은 보류

[ROR #159](https://github.com/ror-community/ror-updates/issues/159)는 2021-05-06 생성됐고 열람 시 open이었다. 본문은 2020-10-01 ITE `02khfkr46`와 ITME `03jp3w522`의 합병으로 새 IMiF가 생겼다고 설명한다. [큐레이터 댓글833873504](https://github.com/ror-community/ror-updates/issues/159#issuecomment-833873504)은 merge/redirect를 처리할 기능이 생기면 진행하겠다고 썼다. 현기관 [공식 홈페이지](https://imif.lukasiewicz.gov.pl/)를 열었으나 합병일을 증명하는 절은 해당 페이지에서 확인하지 못했다.

따라서 이 요청은 “합병 성공”으로 채점할 수 없다. 요청에 현실 합병을 설명한 문장이 있어도 현재 카탈로그가 두 옛 ID를 어디로 보냈는지는 별도 수정판이 필요하다. 당시 기능 부재 진술을 2026년 현재 ROR 전체 기능의 한계로 일반화하지 않는다.

## ROR-X3 · Rockwell Collins의 중간 successor 표현 문제

[ROR #13357](https://github.com/ror-community/ror-updates/issues/13357)은 2024-08-12 만들어졌고 열람 시 open이었다. 요청은 2018년 UTC의 Rockwell Collins 인수와 Collins Aerospace 형성, 2020년 RTX 산하 관계를 별개 시점으로 서술한다. 요청에 따르면 Rockwell Collins `025vwbe15`의 successor는 당시 RTX `0354t7b78`를 가리키지만, inactive successor 제한을 풀면 Collins Aerospace `04k67r158`로 고쳐야 한다.

이 자료는 현실 인수·중간 조직·상위 회사 관계를 한 successor 값에 압축할 때 이력이 손실될 수 있다는 **요청자의 문제 제기**다. 수정파일, 당시 전체 dump, 원 회사의 인수공고를 읽지 못했으므로 실제 반영된 정정 또는 관측된 손실로 채점하지 않는다.

## 최소 재개 입력

- ROR-X1: PPS의 inactive 전 full dump와 LIAFA측 ID·변경파일, 과거 PPS 논문 한 건 및 소비자의 현재 인용을 추가한다.
- ROR-X2: #159의 후속 issue/PR 또는 현재 전체 dump에서 옛 두 ID와 IMiF를 찾아 구현 여부를 확인한다.
- ROR-X3: #13357 후속 change request와 실제 2018/2020 회사 공고를 직접 연 뒤 successor chain을 시간순으로 비교한다.

