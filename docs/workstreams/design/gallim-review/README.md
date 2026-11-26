# 기존 갈림안 검증

`work/design-gallim` 고정판 `fc68f0d1`이 실제로 무엇을 잘하고 어디서 깨지는지 고정 입력으로 확인한 묶음이다. 전체 설계서가 아니다.

| 파일 | 내용 |
| --- | --- |
| [ASSESSMENT.md](ASSESSMENT.md) | 결론, 약속과 실제 동작, 공통 요청 R1 대입, 다섯 판단 문제, 부품 삭제 시험, 채택·수정·폐기 후보 |
| [SEALED_CASE.md](SEALED_CASE.md) · [sealed-case.json](sealed-case.json) | 새 구상을 읽기 전에 봉인한 평가 사례 EVAL-X1 (봉인 커밋 `afa3c285`) |
| [probes/](probes/) | 탐침 스크립트 10개와 출력. `sh probes/run.sh`로 다시 만든다 |
