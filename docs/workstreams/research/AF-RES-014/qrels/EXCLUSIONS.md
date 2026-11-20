# Must 및 필드 충돌 규칙

1. 011의 `force=must`만 대조한다. 각 항목의 기존 target·polarity는 보존한다. 완전 일치하는 NFKC+casefold+공백 접기 키를 아래 표기와 대응시키며 부분 문자열, 임의 어간, 벡터 유사도를 사용하지 않는다. 복합 조건의 독립적인 명시 항목만 펼친다. 이유·나중 댓글·N 판정·단순 선호는 필터 입력이 아니다.
2. 항목의 `exclusions`는 `target`(아래 개념), `polarity`(`unsupported` 또는 `required`), `evidence_url`로 구성한다. 공식 문서가 해당 제품·기능의 지원 불가 또는 필수 전제를 명시해야 한다. 표현이 없는 상태, 제삼자 반박, 버전·설정이 모호한 설명은 빈 필드로 남긴다. 제품 옵션 중 하나만 제한되는 경우 해당 옵션이 검색 항목 자체일 때만 넣는다.
3. Must가 해당 개념을 요구하고 항목은 unsupported이거나, must가 개념을 금지하고 항목은 required일 때만 충돌한다. 같은 개념의 다중 근거는 한 번 센다. `unsupported`는 부재가 확인된 기능에만 쓰고, 라이선스·배포·버전 문구의 적용 범위를 근거 원장에 남긴다.
4. 필터는 충돌을 제거하고 기본 순서를 유지한다. 감점은 기본 1-based 순위에 서로 다른 충돌 개념당 10위를 가산한다. 동점은 원래 순위로 해결한다. 두 처리는 일치하지 않은 경우 D-b의 기존 순위를 유지한다. 대조 불능 개념은 분모에 남겨 대조 범위를 별도로 알린다.

| 011 must target | 개념(필요/제외 방향) |
| --- | --- |
| 서버와 클라이언트 공개 소스 | `server_open_source` 필요, `client_open_source` 필요 |
| 공개 소스, 오픈소스 | `open_source` 필요 |
| 자체 호스팅 가능, 자가 호스팅 | `self_host` 필요 |
| 중개 서버 없는 저장소 | `relay_server` 제외 |
| 오프라인 한 컴퓨터, 로컬 오프라인, 오프라인 GUI | `offline` 필요 |
| 무료 | `free` 필요 |
| PostgreSQL 유지 | `postgresql` 필요 |
| OpenAPI 가져오기 | `openapi_import` 필요 |
| 요청 그룹 파일·CLI | `request_group_files` 필요, `cli` 필요 |
| 구형 .ppt 읽기 | `legacy_ppt` 필요 |
| 가능한 EXIF 보존 | `exif_preservation` 필요 |
| Boost 비의존·그래프 조작·공개 소스 | `boost` 제외, `graph_edit` 필요, `open_source` 필요 |
| 용어집 재사용 | `reusable_glossary` 필요 |
| VS Code·다중 파일 | `vscode` 필요, `multi_file` 필요 |
| SD카드 직접 저장 | `sdcard_write` 필요 |
| PDF 읽기, OCR·생성·편집 불필요 | `pdf_read` 필요. 불필요는 금지로 바꾸지 않는다. |
| .NET8·상업적 사용·무료 | `dotnet8` 필요, `commercial_use` 필요, `free` 필요 |
| 큰 메모리 AI | `high_memory_ai` 제외 |
| 온라인 방식이면 최종 사용자의 계정 생성 불필요 | `end_user_account` 제외. 무조건 계정이 필요한 온라인 항목에만 적용한다. |
| 영어 문장형 C# 테스트 | `csharp_bdd` 필요 |
| 별도 서버 예산 없음 | `separate_server` 제외 |
| ZooKeeper | `zookeeper` 제외 |
| 30초–1시간 작업 | `runtime_60m` 필요 |
| 클라이언트PC | 대조 보류. 011의 짧은 문자열은 접속 주체와 설치·방화벽 제한을 구별하지 못한다. |
| 활발히 유지되는 라이브러리, 활발한 유지보수 | `maintained` 필요. 명시 종료·보관만 배제한다. |
| 회로에서 라벨 대신 직접 선 연결 | `direct_schematic_wires` 필요 |
| PCB 배선 생성 | `pcb_routing` 필요 |
| 컨테이너에서 IMAP 메일 수신 | `imap_receive` 필요 |
| 한국어 화자 구분 | `ko_speaker_diarization` 필요 |
| 자막 처리 | `subtitle_management` 필요 |
| seedbox 연동 | `seedbox` 필요 |

다른 문자열은 원본 메타데이터로 유지하며 대조는 미지원으로 센다.
