# RUN02 전체 R1 대조 — 초기 보류를 수정한 반증

실제 실행: `2026-11-22T23:00:16.442063+00:00`–`2026-11-22T23:09:38.308193+00:00`, exit0, 약561.9초. 지정 명령은 실행 영수증에 있으며 전체 입력 파일을 저장하지 않는 스트리밍이었다. 처음20 records 검사와 최초 R0 집계는 그대로 보존했다.

| 범위 | 원 실행 archive R1 | 현재 publisher R1 |
|---|---|---|
| gzip 전체 bytes | 487611787 | 413005346 |
| gzip 실측 MD5 | 52f3ed344d88278c703faa1280818ce1 | 24ba6bb88db052d4bf64ac98131d6005 |
| gzip 실측 SHA256 | 4cd8ae63bb5fb67e714c3182bb3035df9d0e83edd26cc51d4439cd44c3015316 | 80d7b7e6ec395d03a8dcac652f640cb2d11fa41614b027eae17e51541c8638d2 |
| decoded 전체 bytes | 1409966879 | 1409966879 |
| decoded 전체 SHA256 | 98be27b898b6ae3c12821a30b48adc1bfec9d98903219f0175240ebac66fccf3 | 98be27b898b6ae3c12821a30b48adc1bfec9d98903219f0175240ebac66fccf3 |

**압축 표현은 다르고 전체 decoded 내용은 같다.** 별도로 [NIST의 공식 MD5목록](https://ftp-trace.ncbi.nlm.nih.gov/giab/ftp/data/NA12878/NIST_NA12878_HG001_HiSeq_300x/HG001-part2.md5)을 다시 열어 전체64161bytes의 hash가 이전 열람과 같음을 확인했다. 정확388행은 다음 객체를 지목한다.

```text
MD5 (/Volumes/UHTS1/AWSTransfer//140407_D00360_0017_BH947YADXX/Project_RM8398/Sample_U5c/U5c_CCGTCC_L001_R1_001.fastq.gz) = 52f3ed344d88278c703faa1280818ce1
```

이 MD5는 현재 publisher gzip과 다르지만 **실제 보관 gzip 전체 MD5와 일치**한다. 같은 basename의 다른 flow-cell은116행/254행에 다른 MD5로 있다. full path가 일치하는388행만 적용했다. manifest HTTP Last-Modified는2014-09-19지만 이 header를 변경 불가능한 최초 공개일 증명으로 쓰지 않는다.

## 판정을 바꾼 연결

1. 같은 [Zenodo archive](https://zenodo.org/records/12622362)의 원 action `#bdfcc6a4-3bf4-4fd7-9e8c-cc6b0deaa43d`가 collection `#dcc0e6bb-4888-4bee-bc06-e995b5d18538`을 통해 R1 File을 입력으로 지목한다.
2. 그 File의 SHA256은 이번 전체 member 실측 SHA256과 일치한다. archive stderr에는 named R1/R2를 mount하고 cutadapt에 넣은 명령이 있다.
3. 독립 publisher manifest의 exact path/MD5가 그 **같은 전체 archived gzip**을 식별한다.

요구된 당사자의 구체적 runID/input 명세와 독립 발행자 fingerprint가 만났으므로 **RUN02 선택 Zenodo action의 R_external을0→1로 수정**했다. GitHub의 다른 UUID는 자동 승격하지 않았다. 전체 decoded 일치만으로 이 결론을 낸 것이 아니다. publisher의 checksum 목록이 현재 served gzip과 다르다는 사실을 전체 조사 실패로 취급하면 이 과거 표현의 연결을 놓친다.

현재의 gzip을 원 실행이 읽었다고 주장하지 않는다. 원래 기록된 입력은 publisher checksum으로 지목된 다른 압축 표현이다. 자료 취득/재압축 날짜·명령과 명명된 다음 발행판은 미확인이다. 별도 machine-I/O attestation도 없지만 사용자 기준은 당대 runID+input 명세/당사자 구체적 기록을 허용한다.

## 아직 확인하지 않은 주장

선정 필드는 raw FASTQ의 sequence/quality가 아니라 output gVCF의 CHROM=1이다. 이 출력의 독립 재계산을 하지 않았으므로 **V=0**이다. 동일 작성자 graph/VCF/로그 hash 대조를 독립 output 검증으로 세지 않는다. gzip byte 변화가 생물학적 내용 정정이라는 주장도 하지 않는다. 두 전체 decoded payload는 동일했다.

최종 보강 집계는 P2/2, U_external1/2, U_local2/2, R_local2/2, R_external1/2, V0/2, V조건부R=0/1이다. 새 direct-read3행은 기존 publisher/consumer 저작의 추가 관측이므로 최소 원문 수 추가0이다. 전체 전송·hash 결과, 원본 실행 스크립트 SHA, before-full-fastq snapshots, publisher exact line은 각각 execution receipt/comparison/interpretation/변경 원장에 연결돼 있다.
