# 반례·결손·정정

## 정정 이력 (이전 행 삭제 금지)
- F03–F06: 프로젝트 빌드 화면 shell은 실제 로그를 읽지 못한 상태로 남긴다. 후속 Raw text 링크로 Y03–Y06를 열어 L0–7의 finished/Success=True, L14–35의 실제 checkout 및 commit 확인. P stable 293218ad059d994baf1777d882911bed6a49704a (13.0.0 version bump), U stable b1d30ab61fe0db8f11092805e8c5ac43e091064a (Release 2.8.0); latest 두 프로젝트 origin/main checkout. 현재 별칭을 구성한 실제 빌드 근거가 확보되었으나 CDN의 개별 응답과 당시 소비자 도착지는 여전히 별도 문제.
- D02/D04/D05/D06/D07/D08: tag 경로로 읽은 후 직접 immutable SHA 파일을 다시 읽음. blob 및 핵심 줄 일치. D01/D03의 rendered HTML이 그 SHA에서 빌드되었다는 독립 증거는 여전히 미확인.
- F01/F02: 같은 숫자판 루트도 추가 실패 F11/F12. H05 현재 프로젝트 목록은 stable/latest만 표시; 숫자판 404라고 단정하지 않음. Raw HTTP F07 DNS 실패 (exit 6, status 000). 경로를 수정해 접근 가능한 것처럼 쓰지 않음.
- Y07 dated W3C 2025 문서와 W02 latest alias는 같은 판; 중복 불산입.
- Y01/Y02 소비자 본문 C01/C02에서 링크한 정확한 커밋 코드 직접 재확인. 질문지의 경계는 알려진 이름 변경을 미리 노출한 목적 표본이다. 통계적 오류율 추정으로 일반화 금지.

## 실제 반증
1. U 오래된 호출은 1.26.18에서 경고를 내면서 허용(D02)하므로 stable 2.8.0 문서에서 이름이 사라졌다는 이유로 기존 배포를 무조건 차단하면 거짓 경보. 반면 C01/C02와 Y01/Y02는 2.x 소비자에서 제거된 keyword가 실제 코드에 남아 오류가 난 상황. total=10은 양쪽에 동일하므로 모든 링크를 폐기하는 정책도 과잉. 최신 CHANGELOG X05/R02의 old 이름은 현재 호출이 아니라 제거 이력. 1.25.8 배포에서 반대로 allowed_methods가 거부된 C06: 버전 확인 없는 새 이름 교체도 해롭다.
2. P 9.5.0의 __getattr__이 ANTIALIAS를 enum으로 반환(D06); stable 13.0.0의 resize 목록에 이름이 없다고 과거 코드가 잘못된 것은 아님. 10.0.0에서는 C04의 AttributeError와 D08/R04/X04가 일치. X03 현재 deprecations에는 과거 이름이 명확하고 X06 2.7.0 릴리스 노트는 당시 하위호환 별칭을 설명: 역사 설명 링크는 살아 있고 유효한 동시에 현재 호출의 근거로 쓰면 오류. Resampling.BICUBIC=3 두 고정판, X02 현재 목록에도 존재: 동일 의미가 확인된 범위에서 유지 가능. 실제 화질 동등성은 C03 요청이며 확인한 결과가 아님.
3. 문서 호스팅 관점: H01 규칙은 latest/ stable의 일반 정책, H02/H03 설정은 빌드 환경, Y03–Y06 실제 성공 빌드가 근거. 현재 제목과 build 기록이 일치하지만 실제 URL 전송 상태 및 HTML id 미수집; 사용 가능성을 단일 점수로 합산 금지. F01/F02/F11/F12는 실패 접근, 원인(비활성, 미빌드, 제한, URL 규칙)은 분리 미확인. numeric 대신 SHA 소스/RST 제공.
4. W3C W01/W02/W03/Y07: 2018 dated WCAG2.1 single-pointer 정의와 2025 latest/dated 정의가 달라졌고 변경 기록도 있다. latest alias가 계속 열리는 사실만으로 역사 인용의 의미 동일성 보장 불가. 반면 기존 보고서가 latest를 의도적으로 참조하면 현행판 유지 + 보고 당시 날짜 병기. 규범 정의의 변경은 Python 런타임 TypeError와 동치가 아니다.
5. 경쟁 설명: stable가 가리킨 판 자체가 아니라 fragment만 바뀌었을 수도 있다(X07 old anchor vs current heading). 원시 HTML에 옛 ID가 호환 앵커로 살아 있으면 fragment 교체 제안 철회; 호출 지원 판단은 별도 유지. 정확한 9.5/10.0 rendered 응답이 성공하면 SHA fallback 우선순위만 조정. 당시 archive가 old alias→target 당시 버전임을 증명하면 역사 링크 보조 근거를 추가하되 원문 href는 보존.
