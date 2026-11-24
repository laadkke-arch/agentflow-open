# AF-RES-165#1 HANDOFF

**PARTIAL — 모집 및 정확판 배포 증거 미달.** 결과와 자체 점검은 원격에 기록되었다. 중앙 진행표를 수정하지 않았다. 하류 처리 사실과 일반 재사용 승인/금지를 구별했다.

| 항목 | 값 |
|---|---|
| 작업 브랜치·소유 경로 | work/research-af-res-165 / docs/workstreams/research/AF-RES-165/ |
| 계획 통합판 / 실제 시작 통합판 | ded3420249a3d60ebbb578a8432cf262d3ffa7d7 / d32c697b4345442a4c91f62b8fb0bbed19e58034 (ahead 4, only dot-control diff +190/-6; [SCOPE_DELTA](SCOPE_DELTA.md)) |
| 선행 고정판 | AF-RES-150 ff2c1fc8786ba70a1432f1089f8f81288e43a61d, [HANDOFF](https://github.com/laadkke-arch/agentflow-open/blob/ff2c1fc8786ba70a1432f1089f8f81288e43a61d/docs/workstreams/research/AF-RES-150/HANDOFF.md) |
| 결과·자체점검판 | **488fd6819154748ad37d70e64ccdc0f24b345ccb** [RESULT](https://github.com/laadkke-arch/agentflow-open/blob/488fd6819154748ad37d70e64ccdc0f24b345ccb/docs/workstreams/research/AF-RES-165/RESULT.md) · [SELF_CHECK](https://github.com/laadkke-arch/agentflow-open/blob/488fd6819154748ad37d70e64ccdc0f24b345ccb/docs/workstreams/research/AF-RES-165/SELF_CHECK.md) |
| 마지막 인계 커밋 | 이 파일의 단독 커밋. 자기 SHA는 본문에 쓰지 않으며 branch HEAD 또는 아래 git log로 확인. |

| 묶음 | 실제 커밋 / 대표 파일 재열람 |
|---|---|
| ① 범위 | 04356e9430a81e020722fa41dee4c095a62cf049 SCOPE.md |
| ② 모집·원장 | fc3a47b1126cb437ccab3e1d48836bb9c38e178c sources.jsonl; b3a5536ae71f0083c314687f4c9c64c9cd0d8814 frame.csv; 749dc6fe311f983320b4640e5156fb444b8b48da SCOPE_DELTA.md |
| ③ 주 관측 | cb992185789f676e2b66027e3c4273cfe8bd1926 assets.csv; b2958d019edd6f1502018ecf4a433c551e4030ce decisions.csv |
| ④ 반례·정정 | 17a331036c5b98d214b8dab4e2640c2cb51b9ae4 sources.jsonl; 053ca70bf559c6485c847978eff3765406ac3089 assets.csv; 81e9e3f483199ede85beee79260c1027134dca1b decisions.csv; bb81e75f3bbee6ad4cbe1942765c91a64adb8296 frame.csv; 2184447a680f22dbc4f0a1b86bf7971cca5d427c advice.csv; e1918c1d2ed988734b81d54112e81fb2bf847d3f COUNTEREXAMPLES.md |
| ⑤ 결과표 및 자체점검 | fecb0089b012dfdd653dd2824905de3a4b7f01cb RESULT.md; 488fd6819154748ad37d70e64ccdc0f24b345ccb SELF_CHECK.md |

위 각 커밋의 해당 파일을 GitHub에서 다시 열어 작성 내용과 일치 확인했다. 결과판 비교는 실제 시작판 대비 ahead 14, behind 0, 변경 파일 10개 전부 소유 경로 내 추가. 결과판의 RESULT, SELF_CHECK, SCOPE도 별도 원격 재열람. 로컬 checkout, 빌드, package archive 추출, 독립 검사, workbench session manifest 및 명령 검사는 미실시.

## 넘길 판단과 분모

- 직접 원장 54행 중 열람 42행·실패 12행(중복/보조/입구 포함). 산입 고유 계보 22개: 하류 보고 8, 엄격 파일별 상류 5, 배포 목록 5, 박물관 2, 악보 2. rqrr 고정 include manifest는 추가 상류 결정이지만 원 사진 권리 표시가 아니므로 엄격 상류 6개 하한에는 1 부족. 하류 8은 보충/목적층(시험 파일, 운영 폰트, 미종결 포함), 자연창 적격 8 충족으로 보지 않음. 실제 원순위 0/예정 20, 결측 20; 양성 0이 아니라 원목록 접근·정렬 미복원. 확장 조건 미판정. 
- D3 jpeginfo는 고정 상류 test README의 NC-SA와 프로그램 GPL을 분리하고 #1064380 repack 보고 및 동일판 Debian source test 폴더·amd64 binary 목록에서 지정 jpg 부재를 확인했다. 원 tar 바이트 검사는 미실시. D2 darkslide는 SourceSansPro 조건 미상, 별도 Alegreya OFL 언급, 실제 6.0.0-2 WOFF2 포함과 Apache만 있는 하류 copyright를 확인. 포함이 허용의 증거가 아니다. D4 FreeCAD는 원저자 후속 CC0 및 Files-Excluded 항목 제거 기록이 있으나 실제 font 포함/교체 미확인. F1 동일 Zlib 고지가 두 예제 코드에 충분한 좁은 사례. F2 tiny_ttf 데이터 권리는 별도. F3 고지 추가 후 패키지 변경 보고, F4 crate include 범위 변경은 실제 artifact 검증 전까지 조건부.
- 정확한 심사판과 직접 공개 목록이 연결된 사건은 D2/D3 2/8, 지정 source+binary 경로 모두 확인은 D3 1/8. 실제 파일 교체 뒤 판정 뒤집힘, 순수 크기/중복/빌드로 파일 제외된 사건, 타 분야의 역사적 권리 정정 원판은 미확인. 외부 분야는 개별 소장품/악보·녹음의 표시를 읽었을 뿐 파일 자체나 법적 판단 아님. 
- 원장 S02/S03/S09 오독·축약은 phase 4 별도 정정. 원판 유지, 산입 계보 수 불변. 자기검산에서 CSV 23/16/8/10행, S번호 미연결 0, JSONL 고유 54 ID 확인.

## 다음 첫 행동 및 공개 입력

**자연 모집창의 원목록부터 복원**한다. 원 진입점 [BTS](https://bugs.debian.org/) · [UDD](https://udd.debian.org/bugs/) · [Bugzilla](https://bugzilla.redhat.com/) · [Fedora package-review archive](https://lists.fedoraproject.org/archives/list/package-review@lists.fedoraproject.org/). 사용 기간 2018-01-01~2025-12-31 최초 보고일, example/sample + font/image/artwork, Debian 패키징·저작권/Fedora Package Review; 날짜 오름차순 동률 공개 번호 오름차순, 앞 10 unique 각 창. 실제 필터 결과를 원본·공개 시각·ID로 저장하고 적격 경로 3건 미만일 때만 각 다음 10. 모든 미열람 및 배제 사유 기록. 최초 검색에서 처분을 넣지 말고 목적층은 따로 유지. Debian policy·Emacs 문서 제외. 원 순위 복원 실패시 계속 PARTIAL. Fedora HTML query 및 REST 시도 URL은 S40–41, archive S42. 
다음 정적 비교는 [COUNTEREXAMPLES](COUNTEREXAMPLES.md) 마지막의 구체 버전·파일·명령·기대값. 가장 먼저 D4 1.0.2+dfsg-1 원 source와 freecad-common 등 binary에 두 Y14.5 폰트 있는지, F3 1.3.2-1.fc41 SRPM 및 F4 .crate 0.9.0/0.9.1 파일 목록을 확인. F4 crate download는 공개 static.crates.io, tar -tf; F2 Koji의 정확 fc42 NVR source, main/devel/debugsource. D2 exact CSS data URI를 static decode 후 font metadata 및 upstream 원 권리 고지와 연결. 실행·설치·제품 빌드 필요 없음. 명령은 실행하지 않았으므로 실제 성공은 미확인.

후속 Codex의 repo 검사 입력:
```sh
git fetch origin refs/heads/work/research-af-res-165:refs/remotes/origin/work/research-af-res-165
git log -1 --format=%H refs/remotes/origin/work/research-af-res-165 -- docs/workstreams/research/AF-RES-165/HANDOFF.md
git diff --name-only d32c697b4345442a4c91f62b8fb0bbed19e58034 refs/remotes/origin/work/research-af-res-165
git diff --check d32c697b4345442a4c91f62b8fb0bbed19e58034 refs/remotes/origin/work/research-af-res-165
python -m workbench.session --help
```
세션 manifest는 없음. 현 저장소의 help 및 RESEARCH_WORKFLOW 규칙을 보고 고정 시작·의존·owned 경로가 맞는 manifest를 별도 검증 담당이 준비할 때 `python -m workbench.session check docs/workstreams/research/AF-RES-165/manifest.json --fetch` 실행. 원격 diff만 확인했으며 해당 명령의 통과를 주장하지 않음.

색인 제안: **AF-RES-165 · 기능 원리 링크와 파일별 배포 근거(PARTIAL)** — [RESULT](RESULT.md), [assets](assets.csv), [decisions](decisions.csv), [advice](advice.csv), 선행 150; 동일판 원권리·하류 처분·실제 목록을 분리, 모집과 교체 반례는 미완.

| 불일치·약점 | 영향을 받는 판단 | 다음 조사와 자료 | 결론을 뒤집을 관측 |
|---|---|---|---|
| 모집 원순위 0/20, 두 검색창 미복원 | 대표성 및 적격 사례 수 | BTS/UDD 및 Bugzilla/HyperKitty 원목록 | 2018–2025 최초 보고순 10+10 고정과 모든 후보 심사 |
| 실제 파일 교체·최종 포함 연결 부족, 상류 권리 5/6 | 파일 복사·조건 변화 안내 | D4 exact source/binary, F3 SRPM, F4 .crate 0.9.0/0.9.1, 원 폰트 및 이미지 고지 | 동일 경로의 교체 전후 해시·고지·실제 목록과 결정자가 연결되는 기록 |
| 다른 분야 정정 이력과 비권리 제외 대조 미확인 | 외부 원리 이전 범위 및 배제 이유 | 박물관/악보 권리 정정 원판, 크기·빌드·중복만을 이유로 제거한 패키징 원자료 | 정정 전후 동일 자산/판 기록 및 다른 사유만으로 실제 제거된 파일 목록 |
