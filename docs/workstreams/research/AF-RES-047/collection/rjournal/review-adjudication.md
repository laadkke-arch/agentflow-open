# RUN02 전체 입력 대조 뒤 R 판정 재검토

**RUN02의 R_external을 0→1로 바꾸는 것이 사전 SCOPE에 부합한다. CHROM의 엄격 V와 엄격 사용판+값 양성은 0을 유지한다.** 실행 보강층의 R_external은 1/2, 외부 입력 연결이 확인된 사례를 조건으로 하는 V는 0/1이다. 자연층 R은 0/6이고 그 층의 조건부 V 분모는 여전히 0이므로 해당 없음이다.

검토 시각은 2026-11-22T23:13:35.663166+00:00이다. 동일 모델의 별도 문맥에서 SCOPE, 원 archive 추출물, 실행 영수증과 전체 파일 대조 결과를 읽고 관계·해시·수치를 점검했다. 외부 독립 판독이나 과거 variant-calling 실행 재현은 아니다. 약 0.9 GB의 전체 전송도 여기서 반복하지 않았다. Root 파일과 코드는 수정하지 않았다. 입력 snapshot 해시와 12개 확인 조건은 review-adjudication.json에 있다.

## 사전 기준과 새로 닫힌 연결

SCOPE §4의 R은 실제 실행 ID에 입력 객체가 명시적으로 연결된 경우다. 해시만, workflow 정의의 예상 입력, 다른 실행 로그, 후대 재현은 이 조건을 충족하지 않는다. 동시에 실행 선언을 읽은 것과 실행 진위를 별도 검증한 것은 구별하라고 한다. 즉, R 자체에 별도의 syscall 추적이나 외부 운영자가 목격한 역사적 실행 증명을 추가 요구하지 않는다. 사용자 질문도 당시 실행 ID·입력 명세 또는 당사자의 구체적 기록을 허용한다.

이번 새 근거는 해시 하나가 실행을 증명한다는 논리가 아니다. 다음 세 연결이 함께 존재한다.

| 연결 | 직접 확인한 위치와 내용 | 허용되는 주장 |
|---|---|---|
| 실행 기록 → 보관된 R1 입력 | [같은 Zenodo archive](https://zenodo.org/api/records/12622362/files/wetlab2variations_full.zip/content)의 ro-crate-metadata.json에서 CompletedAction #bdfcc6a4-3bf4-4fd7-9e8c-cc6b0deaa43d의 object → Collection #dcc0e6bb-4888-4bee-bc06-e995b5d18538의 hasPart → inputs/U5c_CCGTCC_L001_R1_001.fastq.gz. 같은 archive의 stderr 85행은 mount, 95–108행은 cutadapt 입력 인자, 110·114·127–128행은 처리와 완료를 남긴다. | 당사자가 특정 실행과 R1 입력을 연결해 남긴 구체적 실행 기록이 있다. GitHub의 다른 action UUID를 합치지 않는다. |
| 보관된 R1 바이트 → 작성자 fingerprint | wetlab-full-fastq-comparison.json의 archive 객체와 원 crate File의 sha256/contentSize. 전체 487,611,787 bytes의 계산 SHA256이 선언과 일치한다. | 실제 보관 member가 실행 기록이 지목한 파일 fingerprint와 일치한다. |
| 보관된 R1 바이트 → 발행자 객체 | [HG001-part2.md5](https://ftp-trace.ncbi.nlm.nih.gov/giab/ftp/data/NA12878/NIST_NA12878_HG001_HiSeq_300x/HG001-part2.md5) 원문 388행의 전체 flow-cell/library/R1 경로와 archive 전체 계산 MD5가 일치한다. 동일 basename의 116·254행은 다른 flow cell이므로 사용하지 않았다. | 소비 기록의 입력을 다른 계보인 발행자의 구체적 파일 fingerprint에 연결할 수 있다. |

계산에 사용된 verify_full_fastq.py의 SHA256은 실행 영수증의 값과 일치하고, 생성된 결과 파일의 SHA256도 영수증과 일치한다. 스크립트는 archive member와 발행자 파일의 끝까지 읽고 gzip을 해제한 전체 stream을 계산한다. 실행 영수증은 2026-11-22T23:00:16.442063+00:00 시작, 23:09:38.308193+00:00 종료, exit code 0을 기록한다. 이것은 이번 감사 계산의 실행 영수증이며, 원 분석의 실행 영수증과 구별한다.

## 바이트판과 해제된 내용의 결과

| 항목 | 소비 archive의 R1 | 현재 발행자 R1 |
|---|---|---|
| 저장 바이트 수 | 487,611,787 | 413,005,346 |
| 저장 MD5 | 52f3ed344d88278c703faa1280818ce1 | 24ba6bb88db052d4bf64ac98131d6005 |
| 발행자 full-path MD5 목록과 일치 | 일치 | 불일치 |
| 해제된 전체 바이트 수 | 1,409,966,879 | 1,409,966,879 |
| 해제된 전체 SHA256 | 98be27b898b6ae3c12821a30b48adc1bfec9d98903219f0175240ebac66fccf3 | 같은 값 |

현재 발행자 객체의 주소는 [전체 flow-cell/library/R1 경로](https://ftp-trace.ncbi.nlm.nih.gov/giab/ftp/data/NA12878/NIST_NA12878_HG001_HiSeq_300x/140407_D00360_0017_BH947YADXX/Project_RM8398/Sample_U5c/U5c_CCGTCC_L001_R1_001.fastq.gz)다. archive 저장 SHA256은 4cd8ae63bb5fb67e714c3182bb3035df9d0e83edd26cc51d4439cd44c3015316으로 원 crate 선언과 같다. 현재 발행자의 저장 SHA256은 80d7b7e6ec395d03a8dcac652f640cb2d11fa41614b027eae17e51541c8638d2다.

따라서 기존의 첫 20개 FASTQ record 비교 한계는 전체 해제 내용 대조로 넘어섰다. 현재 gzip의 저장 표현은 다르지만 해제된 전체 내용은 같다. archive gzip은 발행자 MD5 목록에 보존된 fingerprint와 일치한다. 이를 현재 gzip도 옛 checksum과 같다고 쓰면 안 된다. 재압축과 양립하는 관측이며, 누가 언제 왜 바꿨는지나 공식 정정 사유는 아직 확인되지 않았다. Last-Modified 날짜만으로 그 변경 시점을 정하지 않는다.

## 왜 V는 그대로 0인가

고정 primary field는 첫 VCF record의 CHROM=1이다. 원 FASTQ에는 VCF CHROM 필드가 없으며, 선택 행은 POS1·END63267·DP0인 출력 블록이다. 이번 전체 입력 대조는 이 출력 행의 독립적 변환·값 검증을 실행하지 않았다. 같은 archive의 output hash가 맞거나 다른 판에서도 CHROM1이 보인다는 사실만으로 이 칸을 올릴 수 없다.

R1 입력 한 개의 외부 연결 성공을 paired R2·reference·known-variant 입력 전체 검증이나 출력의 과학적 정확도로 확대하지 않는다. 원 action의 시각과 완료 상태도 작성자 기록에 근거한 관측이다. 별도 시스템 관측으로 역사적 실행의 진위를 입증했다고 쓰지 않는다. 이 제한을 남기는 것은 R의 성공과 모순되지 않는다.

## 기존 판정의 보존과 보고 수정

앞선 R_external=0은 전체 파일 fingerprint와 발행자 일치가 미확인인 상태의 판정이었다. 그 0과 이전 review snapshot은 지우지 않는다. A10에는 새 열람·계산 시각, 이전 판정, 새 판정과 적용 행을 적는다. 기준을 완화한 것이 아니라 같은 기준에서 빠져 있던 소비 객체↔발행 객체 연결을 확인한 변화다.

- RUN02 A/B의 R은 0을 유지한다. 당대 사용 기록과 보관 member는 C에서 추가되기 때문이다.
- RUN02 C와 첫 표의 strongest claim은 R_external=1로 고친다. CHROM 기록 재독과 엄격 V=0은 유지한다.
- 실행층 R은 1/2, 조건부 V는 해당 없음에서 0/1로 바꾼다. 자연층은 그대로 둔다.
- prefix만 확인했다는 제한을 전체 decoded 대조 결과로 갱신하고, 저장 gzip 차이·발행자 목록의 현행 gzip 불일치·정정 사유 미확인은 유지한다.
- 정보 제거 감도는 새 baseline에서 다시 계산해야 한다. 실제 사용 근거나 구체 자료 식별자를 제거할 때 외부 R 연결도 잃는지 반영한다.
- 이번 대조를 고정 URL·같은 바이트·특정 실행의 실제 미사용이라는 강한 음성례로 대체하지 않는다. 그 빈칸은 여전히 빈칸이다.

낮은 수준의 문구 정합성 문제 하나가 있다. 실행 당시 스크립트 docstring 3행은 실행 전 작성되어 “Not run during AF-RES-047”이라고 남아 있다. 실제 영수증과 충돌하므로 실행 당시 script SHA를 보존한 채 그 문구가 사전 안내였음을 밝히거나 설명을 갱신해야 한다. 이 낡은 문구는 계산된 hash와 전체 내용 대조 결과 자체를 무효화하지 않는다.

R 판정을 다시 0으로 바꿀 최소 반증은 archive input fingerprint가 원 선언이나 발행자 정확 경로와 실제로 다르다는 정정, action→Collection 연결이 다른 실행에 속한다는 증거, 또는 해당 발행자 MD5 행이 다른 객체를 가리킨다는 증거다. V를 1로 올리려면 인증된 입력과 필요한 다른 입력·변환을 사용해 고정 CHROM 행을 다른 계보에서 확인하는 자료가 추가로 필요하다.
