# 표시 정책 봉인 (전수 신규 판정 전)

- 랭킹 봉인: 54fe5f5ce891e787a8ee4e87dfc9bfc8fe6c9809. 조사 8자리/표시 3자리 동일. 양점 순서에 맞춰 원문과 카드 원절(직접 읽거나 선행 고정판의 원절 원장 재사용)을 대조했다. 지지 불충분을 공석으로 남겼다. 한 절을 여러 셀에서 공유했으므로 logical_inspection은 **셀당 논리적 절 대조 수**이지 실제 독립 웹 클릭 횟수가 아니다. 물리 소요시간·셀별 독립 열람은 미측정. 독립 판독자 없음.
- C-P1-07만 K22/L에서 S04를 1번 표시한다. 첫 본문의 forward 구현 및 모델에 입력하여 예측값을 얻는 요구를 근거로 한다. 원시 문자열→최종 감성 라벨 전체를 제공하는 카드라는 의미가 아니다. 선행 답변 노출이 있는 교정층이므로 신규 효과와 분리한다.
- 다른 셀의 양점 카드는 보류: 파일 부재, 텐서 조작과 목표의 불일치, 이미 실행된 코드/로그, 상태 적재와 저장/제출의 혼동을 구분했다. 전수 22카드 기준은 아직 신규 표로 작성하지 않았다. 138의 기존 교정 정답은 이미 노출되어 블라인드 독립 시험이 아니다.

```json
{
  "new_neutral|K16|L": {
    "q": 6,
    "scanned": 16,
    "display": 0,
    "empty": 18
  },
  "new_neutral|K22|L": {
    "q": 6,
    "scanned": 17,
    "display": 0,
    "empty": 18
  },
  "new_neutral|K16|R": {
    "q": 6,
    "scanned": 0,
    "display": 0,
    "empty": 18
  },
  "new_neutral|K22|R": {
    "q": 6,
    "scanned": 0,
    "display": 0,
    "empty": 18
  },
  "calibration|K16|L": {
    "q": 5,
    "scanned": 23,
    "display": 0,
    "empty": 15
  },
  "calibration|K22|L": {
    "q": 5,
    "scanned": 25,
    "display": 1,
    "empty": 14
  },
  "calibration|K16|R": {
    "q": 5,
    "scanned": 4,
    "display": 0,
    "empty": 15
  },
  "calibration|K22|R": {
    "q": 5,
    "scanned": 4,
    "display": 0,
    "empty": 15
  }
}
```
