# R6-B v2 판정 재구성

**동일 자동 독자의 재판독·재구성 문서이며, 기존 v2 판단은 변경되지 않았다.** 새 독자나 인간 실험, 독립 개발자 채택 관측이 아니다.

- 시작 UTC: `2026-11-24T05:14:56.433899+00:00`
- 종료 UTC: `2026-11-24T05:15:26.915945+00:00`
- 유일한 재판독 파일: `/workspace/scratch/7e9d1ab33296/agentflow-open/docs/workstreams/research/AF-RES-113/evidence/arms/B/R6-v2-packet.json`
- packet SHA256: `d68a2548fd2345d80fd3e5cde5da112aa10e8fd12bfde6a38a425d102d77774a` — 기존 지문과 일치.
- 전체 raw bytes `[0, 9582)`, 9422 Unicode codepoints를 표시하고 판독했다. 원글·공통절 1,262자·baseline·슬롯·명시적 추가 공석을 모두 읽었고 해시를 확인했다.
- 외부 열람 **0**, 검색 **0**, 프로젝트·시험 실행 **0**, Git 작업 **0**, cross-route exposure **false**.

## 판정

문자상 첫 목표 규칙에 따라 공통 시작점은 `skimage.color.lch2lab`로 정정된다. 공통절은 색공간 의미, `channel_axis`, 최소 3채널, 동일 출력 shape와 hue 단위를 추가로 지원한다. astronaut 예제의 왕복 패턴은 원글에 이미 알려져 있다. 문서는 dtype·decimal 4/7 수치 정확도·S390x 동작 또는 수정된 숫자 결과를 보장하지 않는다.

B 추가 슬롯은 **vacant_link**, 추가 텍스트와 그림은 없다. **새 선택 0, 새 시험 0, 추가 홉 적격 신규성 0**이다. 이 재구성에서 새 검사를 만들지 않았다.

## 원래 입력·보존조건·관측 한계

기존 구별 입력은 colorwheel → img_as_float → dtype 변환 → rgb2lab → lch2lab(lab2lch(lab))이며 float16/float32/float64로 매개화된다. `lab.dtype == _supported_float_type(dtype)`와 float32의 decimal 4·그외 decimal 7 왕복 assertion을 보존한다. dtype assertion은 rgb2lab 직후의 `lab`에 적용된다. 더 작은 실패 픽셀은 제공되지 않았고 실제 데이터나 build log를 열지 않았다.

6/411810 불일치, 최대 절대차 5117.8477, 최대 상대차 118.42903은 **원글의 보고값**이다. 본 독자의 측정이 아니다. 수정 구현이 없으므로 수정 후 출력이나 오차를 예측하지 않는다. shape·axis 계약을 만족하면서도 수치 오류를 낼 수 있어 공통 계약만으로 회귀 복구를 입증할 수 없다. 문서 0.26.0과 원글 0.19.3의 실제 구현도 확인하지 않았다.

## 핵심 정정·이견

최초 ambiguous-start 보류는 v2에서 lch2lab 대응으로 정정되었다. 추가 홉 신규성 0은 유지되고 사유는 vacant_start에서 **vacant_link**로 바뀐다. 정정 v2 baseline과 실질적 이견은 없다. 이 파일은 복구된 동일 packet에서 기존 결론을 재작성한 문서이며 이전 판정 파일의 byte 단위 복원이라고 주장하지 않는다. root 공통 분석, 다른 arm, 외부 자료, receipt와 recovery 보고서는 이번 재구성에서 읽지 않았다.
