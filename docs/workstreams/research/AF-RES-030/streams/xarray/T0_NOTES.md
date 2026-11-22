# xarray T0 판독 — 후속 미열람

A8: 2023Q1 #7406/#7408/#7409/#7411; 2024Q3 #9196/#9197/#9201/#9203. 네 번째 적격까지 선별. 이후 A #7413/#7414/#9204/#9207 본문이 한 배치에 불필요하게 출력되었으나 선정8건이나 그 결과를 대체하지 않았고 각 후보를 after_stop_not_screened로 둔다. 전체 search page100건씩은 내려받았지만 metadata-only tail은 직접원문수에 산입하지 않는다.

B27: 2023-04 전체 순서에서6제외 후 #7790까지. 첫 실질 응답에 직접 환경/입력/목적을 묻는 적격 XB03/#7721, XB06/#7726, XB08/#7730, XB13/#7754, XB14/#7758. B는 root가 M/X/D interleave로 최종8개를 고른다. 최초 실질답이 root+90일 밖인 XB06도 결과나지연으로 제거하지 않는다.

원판: API root updated_at/HTML bodyVersion은 원본 복원이 아니다. root lastEditedAt/edit history 미제공. #7406의 첫 답 code 인용은 제한적 Q 보강이며 본문전체원판확정이 아니다. #7406 root Edit 및 metadata 정규식에서 후대 'Closing now. Feel free to reopen'이 실제로 노출되어 exposure=true, 엄격미노출집합에서 제외. 이후 HTML은 root path만 파싱했다. 다른 사례도 원판미확인을 원판확정으로 바꾸지 않는다.

#7408은 저장API open_zarr/to_zarr의 새/기존 dataset 구분 및 cached-state 사용법 문제이므로 포함. #9203은 shoyer가 이전 대화에서 처음 공개한 설계제안을 TomNicholas가 독립논의로 옮겼다는 provenance를 보존. 유지관리자·반복작성자 sensitivity 필수. #9201의 첫 실질 타인응답은 newcomer가 maintainer/requester에게 pure-xarray reproducer 의미를 되묻는 역방향이다. 일반 지원자→사용자 누락정보 요청으로 평탄화하지 않는다.

비질문 경계: #7409 Have you seen 문장은 링크와 제안을 주는 수사적 포인터. #7408 I wonder 는 tmp_path 권고. #7730은 첫 출력에서 접힌 Environment를 생략해 버전없음으로 초안했으나 봉인 전 재독에서 main@f8127fc/flox0.6.10 등을 확인했다. current-root-present지만 first-response 이전 존재는 미확인으로 교정했다. 새 정보로 세지 않는다. #7737 fixed 여부는 trial/outcome confirmation이므로 B의 기존환경/목표/입력질문 아님. #7773 netcdf4.Dataset 실행요청은 새로운 진단행동 요청. #7722/#7748/#7764 hypothetical design proposals는 B의 직접 정보요청 아님. #7721 최초 ping/ #9201 할당요청은 실질답에서 제외하고 그 다음 직접질문까지 읽음.

retrieved/는 원문 재다운로드 캐시이며 프로그램만 받아둔 미열람 후속 댓글을 포함한다. 원격 봉인에 포함시키지 않는다. 다음 단계 전 root stage2 SHA를 기다린다. 각 변수 예상분기는 questions.csv에 미열람 상태에서 고정했다.
