# A10 뒤 RUN02 최종 좁은 재검토

확인 UTC: 2026-11-22T23:25:34.388593+00:00. 대상 RESULT SHA256: `07ce5a039ae9a257ac57aa38900af6c1b26527ca4fcff932b077f1d94da6e7fb`.

동일 모델의 별도 검토 turn이며 실행층 원 조사 담당자의 재판독이다. 외부 독립 검토·맹검이 아니고, 이번 검토에서 네트워크 열람·분석 재실행·root 파일 수정은 하지 않았다.

## 결과

요청 범위12개 확인 항목이 모두 일치한다. root RUN02 표1·C행·Q3/Q5에서 publisher manifest388행의 exact path/MD5와 보관 R1 전체 실측, 같은 archive의 원 action/input 명세가 연결됐다. 현재 gzip의 다른 MD5와 전체 decoded 내용 동일성을 별도 주장으로 유지한다.

- 자연 R0/6, 보강 R1/2, V0/2, 보강 조건부 V|R0/1이 일치한다.
- root runs.csv의 external-positive는 Wetlab-Zenodo-archive 한 행이다. GitHub의 다른 UUID는false다.
- RUN02 A/B는 고정 CHROM 출력과 chromosome1 parameter를 표시하지 않는다. C에서만 외부 입력 연결 R과 기록 재독 CHROM1을 보여 준다.
- 현재 결론에 전체 FASTQ 미실행 또는 prefix만 확인했다는 제한은 남지 않았다. 첫20 records는 최초 관측의 이력으로만 나온다.
- 후속 행동은 이미 끝난 전체 R1 비교를 다시 미수행 과제로 두지 않고, 원래 나머지 입력·변환·선정 CHROM의 독립 확인 및 취득/재압축 역사로 적혀 있다.
- 공식 재압축 시점/명령과 이름이 붙은 다음 발행판은 여전히 미확인이고, 독립 kernel-I/O 관측이나 전체 workflow 검증으로 확대하지 않는다.

## 발견 후 해결한 표현

초기 실행절의64range응답은 실제 기록 구조와 달랐다. JSON의 range_receipts64항목 중63개는 archive Range이고 마지막1개는 publisher 전체 GET이다. 부모가 수정·재생성한 RESULT의 해당 문장을 직접 다시 읽어 **archive Range응답63개와publisher전체GET1개**로 바뀐 것을 확인했다. 위 SHA가 그 최종 파일이다. 이 건은 해결됐으며 수치·R/V 집계에는 영향이 없었다.

개별 checks·파일 SHA·현재 문장 위치는 `final-A10-review.json`에 보존했다. 이전 검토와 R0 판단은 원 snapshot으로 남았고, 추가 실측에 따른 A10의 R0→1 정정을 숨기지 않았다.
