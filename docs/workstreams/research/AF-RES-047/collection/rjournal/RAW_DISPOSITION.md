# 원시 복사본 정리

Parent 요청에 따라 의미 판독과 수치 재검산을 마친 뒤 논문 ZIP·그림, 전체 저자 코드·RDS, R/UCI 데이터 멤버, GitHub 전체 tree 응답, Python parser wheel을 제거했다. 제거 시각, 각 파일의 제거 전 바이트 수·SHA256은 raw_disposition.json에 있다. 외부 원본을 삭제한 것이 아니라 이 작업폴더의 복사본을 정리한 것이다.

남긴 것은 고정 원문 주소·commit·file ID, 다운로드 시각·응답 해시, ZIP/tar 멤버 목록,16개 입력명세, 선택 필드·실제 읽은 값, 한계·실패, 재개 명령과 검산 결과다. Zenodo의 판·개념 DOI·발행/수정일·고정 tag/commit·파일ID·발행자 기재 MD5는 zenodo_release_metadata.json에 정규화했다.215MB Zenodo ZIP 전체는 처음부터 받지 않았다.

verification.json은 정리 직전 **2026-11-22T22:36:57.824317+00:00**에 원시 입력을 다시 파싱한 결과다. R의 두 후보 release에서 Iris 멤버 해시 동일, 네 변형의 Df2, SumSq 차이, author1998경로16개와 publisher16객체,0/386, cases3/readings9 및 source ID 연결을 확인했다. 이것은 이 조사자의 감사이며 원 논문의 실행 증거가 아니다.

필요하면 보존한 원장을 덮어쓰지 않도록 owned_path 아래 별도 replay 디렉터리에서 download script를 복사해 실행한다. compare_public_objects.py는 공식 R 두 tar와 UCI ZIP, read_author_artifacts.py는 고정 저자 commit의 파일을 내려받는다. verify_candidate_values.py는 그 입력과 rdata1.1.0/xarray2026.9.0을 요구한다. Parser의 정확한 wheel 주소·SHA는 additional_http_receipts.jsonl에 있다. RDS를 R에서 직접 확인하는 명령과 원래 입력이 없어서 실행할 수 없는 항목은 findings.md §6에 적었다.

원시 코드의 재게시를 피하려고 전체 내용을 유지하지 않았지만, checksum만으로 과거 사용을 증명한다고 주장하지도 않는다. 동일 원격 객체를 다시 읽을 때 해시가 달라지면 변경 관측을 새 행으로 남겨야 한다.
