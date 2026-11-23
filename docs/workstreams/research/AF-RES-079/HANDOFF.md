# AF-RES-079#2 · 최종 인계

**상태: PARTIAL. 식별·수선 연구 원장을 인계한다. 필수 모집·원문 최소량·두 질문·근거 연결을 충족했으며, 행동 수용은 실제 확인한 판·입력·소비자에 한정한다.**

- 저장소: `laadkke-arch/agentflow-open`
- 작업 브랜치: `work/research-af-res-079`
- 소유 경로: `docs/workstreams/research/AF-RES-079/`
- **결과 고정 SHA: [1398a21f724e3b6c7ad81ee2f56b44715a5c00bd](https://github.com/laadkke-arch/agentflow-open/commit/1398a21f724e3b6c7ad81ee2f56b44715a5c00bd). 이 HANDOFF 단독 커밋의 parent다.**
- 결과판 핵심 파일: [RESULT.md](RESULT.md), [SELF_CHECK.md](SELF_CHECK.md), [수용 증거](evidence/acceptance-evidence.json), [재현·미실시 명령](REPRODUCE.md), [수선 원장](relations.csv).
- 실제 최초 시작 통합판: `d73c8ec85d375f37451795b575dd7d0e6b2f3594`. 계획 기준: `0d2b08431067e8d87212a66ecb27657c65722a59`.
- 재개 때 확인한 작업 head: `eaee6360a23c9415353e02c13c9f44bf425d887b`. 재개 때 읽은 통합판: `4d41a965dceae431a1f8a2f8bc85cbf76a2d2782`.
- 유일한 결과 의존: AF-RES-075 인계 `4b2a29b63f691eebb6613f20e2deb4954b41cfdb`, 고정 결과 `8a8fe9e36e02b343740a2a8db478bc587e57f544`의 Q3·Q7 및 지목된 입력. [읽은 근거](streams/root/intake-075.json).

## 1. 수용한 범위와 분모

| 층·단위 | 확보·확인 | 행동 수용의 한계 |
|---|---:|---|
| 자연 GIS | 선정·양판 원문4/4; 역사 native3/4 | G02·G03·G04의 지정 입력. G01 pixel reader는 server/build가 없어 미실행 |
| 자연 OSS | 선정·양판 원문4/4; 역사 native4/4 | 4판×50호출=200호출,49대응.46 exact input hash+3명시 매핑. O02의 simps/cumtrapz 개별 native는 미실행 |
| 자연 합계 | 원문8/8; 역사 native7/8 | 단독 현재 실행·같은판 대조·HTTP 응답은 이 분자에 넣지 않음 |
| 대조 | 전후 원문3/3; 역사 native0/3 | C02 원PIL archive 공백은 해소했지만 원PIL 실행은 미확인 |
| 외부 등록 이력 | 실제 기록2/2 | IANA mo→ro와 bhk→4수신자. 소프트웨어 동작 보증으로 사용하지 않음 |
| 독립 원저작 |32계보 /최소20 | 추가로5 구현·시험 계보를 제외해도27.166출처·접근행,121본문판독행과 구별 |
| 관측·관계 |104관측,26관계 | 조건부③분리2행은 실제 운영 레코드를 고친 결과가 아님 |
| 가림 재판독 |자연4+대조2 /6 | 별도 도구 에이전트. 통계적 독립성·사람 검토·독립 일치율은 주장하지 않음 |
| 운영 추천 레코드 |제공0개 | 관측 운영 오병합0/0이며 오류율을 계산하지 않음 |

SCOPE의 두 부분 요구와 U/T 수선 규칙은 그대로 유지했다. 최초 로컬 봉인 `60114f7`(11:28:00 UTC)이 첫 GIS 취득(11:29:01)보다 앞서며, 같은 tree가 원격 `dfdfe1b`(11:29:48)에 공개되었다. Git 시각 자체를 외부 공증으로 보지는 않는다. [봉인·출처 감사](streams/resume-sources/audit.json).

## 2. 가장 중요한 판단

1. **수선 단위는 namespace가 있는 대상 ID·판·기능 계약이다.** URL은 위치로 보존하고, 계보상의 동일성과 행동 대체 가능성을 다른 열에 둔다. 옛 ID·당시 판정·원절·설정·출처를 지우지 않고 적용판과 방향 관계를 덧붙인다. ① 유지,② 판 한정 별칭,③ 실제 혼합 레코드의 분리,④ 별도 ID 관계,⑤ 보류를 구별했다.

2. **같은 이름·HTTP200·정상 종료도 필수 기능을 보증하지 않았다.** G04의 새 `GEOARROW` struct 파일은 구GDAL3.8에서 종료0으로 열렸지만 geometry field0·CRS없음이었다. 같은 전후 쌍의 지정 WKB 읽기 P1은 유지되므로 P1/P2 결론도 달랐다. `GEOARROW_INTERLEAVED` 별칭은 geometry·CRS를 복구하지만 bbox4필드를 추가한다. exact-schema와 필수 필드 subset 요구를 구별했다. GN04–07.

3. **변경이 항상 실패를 뜻하지도 않았다.** G03은 format beta.1→1.0.0 변경에도 지정 구GDAL3.7 소비자에서 값·형·순서·geometry·CRS를 보존했다. 지정 invalid compression/PointM 거절도 일치했다. O02의 실행한 적분/분포 별칭과 O04 label 합산도 지정 정상·오류 범위에서 P1/P2가 일치했다. GN01–03, H-O02/H-O04.

4. **정상값만 맞춘 adapter는 경계 계약을 복구하지 못했다.** O01은 옛 기본1.4826 대 새 기본1.0이며, scale adapter가 정상값을 맞춰도 빈(3,0)/axis1의 scalar→배열 변화가 남는다. O03은 exact radius1.0 경계 포함과 np.int64→Python int가 달랐고 새 메서드는 거리 출력을 주지 않는다. H-O01/H-O03.

5. **원래 없던 능력을 새 손실로 세지 않았다.** ARG의 -9999 NoData 요구는3.7부터 충족하지 못했다.3.8 default gate 변화와 이 기존 한계를 분리했다. Rasdaman의 원래 read-only/no-georeferencing도 이관 탓으로 세지 않았다. GN08–11, G-O01/02.

6. **현재 위치와 과거 인용의 연속성은 별개다.** C03은 live200이어도 원 기능 절이 사라졌고, C02 현재 PythonWare 페이지의 원 발행자 연속성은 미확인이다. U는 자연2수선/1유지/5보류, 대조1/1/1이며 보류를 오류로 바꾸지 않았다. 역사 redirect11/11은 미확인이다. mo의 단일 Preferred-Value와 bhk의 네 수신자 관계처럼 방향·판·복수 관계를 보존하되, 그 규칙으로 소프트웨어 입력·출력을 승인하지 않는다.

GIS는 conda-forge의 재구성 환경이다. G04의 Python pyarrow는 둘 다14.0.2지만 실제 C++writer는14.0.1/14.0.2이고 PROJ/build도 다르다. 관측한 호환 결과를 GDAL 판 하나만의 인과 효과 또는 전규격 인증으로 일반화하지 않는다.

## 3. 실행한 검사와 실제 종료값

모든 시각은 UTC다. 실행 장소는 제공된 ChatGPT cloud Linux executor이며 GitHub Actions 실행이나 별도 Codex 계정 연결을 주장하지 않는다. `--environment codex-cloud`는 공통 검사기의 호출자 레이블이다.

| 검사 | 주체·소스/장소 | 실제 결과 | 보존 근거 |
|---|---|---|---|
| 원장 통합 검산 |root, 재개 checkout;2026-11-23 12:22:46 확인 |36검사,종료0 |[원장 영수증](evidence/resume/audit-ledgers.json) |
| OSS 역사 실행·재개 |oss_evidence의4환경;oss_controls_audit 비가림 감사 |원200호출/49대응 receipt종료0;재개18API호출+2속성,4프로세스 모두종료0 |[대응 검산](streams/oss/historical/paired-check.receipt.json), [재개 감사](streams/resume-oss/audit.json) |
| GIS 회복 검산·재개 |gis_evidence의원실행;gis_resume_audit |65출력영수증·6writer지문 확인,11파일 보존;7read 중6종료0·예상거절1종료3;감사종료0 |[GIS 감사](streams/resume-gis/audit.json), [GN 원행](streams/gis/historical/observations.jsonl) |
| 공통 검사 최초 |root,깨끗한source7a314fc |종료1. shallow 이력 밖 부모320424d…가 없어 Git bundle 복원 실패. 소스 결함으로 단정하지 않음 |[최초 실패](evidence/resume/common-source-check.json) |
| 공통 검사 회복·재시도 |oss_controls_audit,같은source7a314fc;12:29:18–12:29:29 |공개unshallow fetch종료0 뒤 재검사종료0.55단위시험·예제7/9·bundle복원 통과 |[재시도](evidence/resume/common-retry-check.json), [회복](streams/resume-git/RECOVERY.md) |
| 개별 작업 계약 |root,source7a314fc 및reportR1 |모두종료0. 공통 sessions의no_active_sessions와 별개 |[source 검사](evidence/resume/session-source-check.json), [R1 검사](evidence/resume/session-exact-r1-execution.json) |
| 고정reportR1 |root,깨끗한daf15ec… checkout;12:36:37–12:36:46 |session0,결과감사38개0 |[실행 영수증](evidence/resume/audit-exact-r1-execution.json), [상세](evidence/resume/audit-exact-r1.json) |
| 원격reportR1 전체 |root urllib GET;12:36:37–12:45:27 |411/411 bytes·SHA256일치;모두첫시도,종료0 |[파일별 재독](evidence/resume/remote-result-r1.json);[connector4본문도일치](evidence/resume/provider-r1-readback.json) |
| **최종 결과1398a21…** |root,깨끗한최종 detached checkout;12:47:41–12:47:48 |**session종료0,38개결과감사종료0** |아래 실제 실행 요약 |
| **최종판 원격 재독** |root,정확1398a21…의420파일 |**420/420 bytes·SHA256 일치, 실패0, 종료0;12:47:41–12:51:16 UTC** |아래 실제 실행 요약; 이 파일만 마지막 단독 커밋한다 |

공통 검사기의 `sessions`는 종료0이지만 `no_active_sessions / not-executed`였으므로 개별 작업 검사를 별도로 실행했다. 음성 입력의 예상 종료3은 정상 파일 읽기 성공으로 세지 않았다. 최초 실패와 이후 성공을 함께 보존했다.

R1 이후 RESULT·SELF_CHECK·SCOPE·frame·세 원장·REPRODUCE의 bytes는 변하지 않았다. 최종 결과판은 검사 영수증과 수용/진행 metadata, 원격 검사기의 선택적 동시 읽기·진행 표시만 추가했다. 마지막 판의 검증은 아래에 직접 기록해, 검증 영수증을 자기 자신이 포함한 commit의 SHA라고 쓰는 순환을 피한다.

### 최종 고정 결과의 실제 계약·구조 검사 요약

```json
[
  {
    "check": "session-final",
    "actor": "root via supplied cloud Linux executor",
    "location": "/workspace/scratch/b2c25bae8d07/agentflow-open/docs/workstreams/research/AF-RES-079/verification/result-check-final",
    "source_commit": "1398a21f724e3b6c7ad81ee2f56b44715a5c00bd",
    "command_argv": [
      "python",
      "-B",
      "-m",
      "workbench.session",
      "check",
      "docs/workstreams/research/AF-RES-079/manifest.json",
      "--fetch"
    ],
    "started_utc": "2026-11-23T12:47:41.521011+00:00",
    "finished_utc": "2026-11-23T12:47:48.432485+00:00",
    "exit_code": 0,
    "initial_source_clean": true,
    "stdout_sha256": "039afb757a82eb89d9d032ad448f81bb589d8f22b19d2e2914b4a0b6537ae1c8",
    "stderr_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "limit": "Exact final result source; session contract or structural audit, not an additional software compatibility test."
  },
  {
    "check": "audit-final",
    "actor": "root via supplied cloud Linux executor",
    "location": "/workspace/scratch/b2c25bae8d07/agentflow-open/docs/workstreams/research/AF-RES-079/verification/result-check-final",
    "source_commit": "1398a21f724e3b6c7ad81ee2f56b44715a5c00bd",
    "command_argv": [
      "python",
      "-B",
      "docs/workstreams/research/AF-RES-079/audit.py",
      "--phase",
      "result",
      "--output",
      "evidence/reruns/final-exact-audit.json"
    ],
    "started_utc": "2026-11-23T12:47:48.432683+00:00",
    "finished_utc": "2026-11-23T12:47:48.541128+00:00",
    "exit_code": 0,
    "initial_source_clean": true,
    "stdout_sha256": "32fff0f48e80a2217cc7d479586b51775f2adb70297b2ac91fe2c875133c64a8",
    "stderr_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "limit": "Exact final result source; session contract or structural audit, not an additional software compatibility test.",
    "checks": 38,
    "failed_checks": [],
    "artifact_hashes": {
      "SCOPE.md": "ddd40c967448d6b93cc3620edcc329f40f6a2fb9a5a0358742bbccdc97622267",
      "frame.csv": "998bb1df93a679cbbf8750aee8a2aad811307e40594511f51aee9aeb7e7c33ab",
      "sources.jsonl": "44c5f9bcf232e47dc1b487c62dbdb52c9302574bd60fd097b353ea66a9c13efe",
      "observations.csv": "3cc7578ffa14ee62f5cdbcd8c050053687323ba7b6dd58c4a9b4ee7164ae78d5",
      "relations.csv": "013b259a35f3f7b37849aa3e11b5a8d1ba28067c6287f428719284b0f06dc62c",
      "manifest.json": "192c7e4e99c650eb319a5dd70ae486e75422714523a954371f1dbea787d4cc64",
      "evidence/first-assessment.json": "451e7ee3b76a16b80562147fe164ed5f6b8f904fa1928edeaaa200c61b66c66d",
      "streams/review/blind-review.json": "5ec70c5eae00ece48360bd95964eb30e3cfddfc4ff5987f3de9319e75da949b1",
      "streams/review/review-comparison.json": "df5ad52a1e4e531b7762b6f0245f560c07a585d358681c1bcdc353aae58ade2d",
      "RESULT.md": "9b5f69156854e62a2b507a9ed697f919111ab3c3e93d3c8fab0eba71455629d6",
      "SELF_CHECK.md": "81311a8c1f3a87df55055b3fa5fb6966e62e2ea7e60eada1e43ef420240b8568",
      "evidence/acceptance-evidence.json": "83a45909f7d263730b90ac781ccb07f1a6ad8d140be8225974b9a1fd7d6d28c0",
      "REPRODUCE.md": "557e65cc7c9a009f8b90f1c3216c21951788093507c15b6cdf17f2309dd89268"
    }
  },
  {
    "source_commit": "1398a21f724e3b6c7ad81ee2f56b44715a5c00bd",
    "all_exit_codes": [
      0,
      0
    ],
    "result_source_unchanged": true,
    "core_files_differ_from_R1": []
  }
]
```

### 최종 고정 결과의 실제 원격 재독 요약

```json
{
  "actor": "root via local Python urllib GET",
  "location": "/workspace/scratch/b2c25bae8d07/agentflow-open",
  "started_utc": "2026-11-23T12:47:41.525817+00:00",
  "finished_utc": "2026-11-23T12:51:16.199063+00:00",
  "repository": "laadkke-arch/agentflow-open",
  "result_commit": "1398a21f724e3b6c7ad81ee2f56b44715a5c00bd",
  "owned_path": "docs/workstreams/research/AF-RES-079/",
  "checked_files": 420,
  "matched_files": 420,
  "failed_paths": [],
  "canonical_manifest_sha256": "e3bf77fb6026ab7385ce94888d531895b2658adf08dd4e8cf04c90c7e3cb2e11",
  "exit_code": 0,
  "command_argv": [
    "docs/workstreams/research/AF-RES-079/remote_verify.py",
    "--commit",
    "1398a21f724e3b6c7ad81ee2f56b44715a5c00bd",
    "--brief",
    "--workers",
    "16",
    "--progress"
  ],
  "limit": "Exact remote bytes and committed scope only; not an additional software compatibility test.",
  "selected_hashes": {
    "RESULT.md": "9b5f69156854e62a2b507a9ed697f919111ab3c3e93d3c8fab0eba71455629d6",
    "SCOPE.md": "ddd40c967448d6b93cc3620edcc329f40f6a2fb9a5a0358742bbccdc97622267",
    "SELF_CHECK.md": "81311a8c1f3a87df55055b3fa5fb6966e62e2ea7e60eada1e43ef420240b8568",
    "evidence/acceptance-evidence.json": "83a45909f7d263730b90ac781ccb07f1a6ad8d140be8225974b9a1fd7d6d28c0",
    "frame.csv": "998bb1df93a679cbbf8750aee8a2aad811307e40594511f51aee9aeb7e7c33ab",
    "observations.csv": "3cc7578ffa14ee62f5cdbcd8c050053687323ba7b6dd58c4a9b4ee7164ae78d5",
    "relations.csv": "013b259a35f3f7b37849aa3e11b5a8d1ba28067c6287f428719284b0f06dc62c",
    "sources.jsonl": "44c5f9bcf232e47dc1b487c62dbdb52c9302574bd60fd097b353ea66a9c13efe",
    "streams/gis/historical/native-summary.json": "62e2eb3e3c2e5706d2c9c0f5893d0a8464b72738636898dc08d40fbca23866dd",
    "streams/oss/historical/paired-check.receipt.json": "ee0c62ba86ff31fcc13920f4ecfcb43d1a8fcb8902bf8b85d5b884d59e16f1ff",
    "streams/review/blind-review.json": "5ec70c5eae00ece48360bd95964eb30e3cfddfc4ff5987f3de9319e75da949b1"
  }
}
```

## 4. 커밋된 묶음

| 순서 | 묶음 | 커밋 |
|---|---|---|
|1|모집·P1/P2·U/T 봉인|`dfdfe1b82ee1921f2f90c723dbd9fe8d22138ead`|
|2a|대조·외부표준|`dd81c973210650690fa054e6c967919d1a1206db`|
|2b|자연 원판·원절|`2f0afa4d415a9e97b6f3d510b23958aeafd54a34`|
|3|관계·수선·반례·가림재판독·OSS역사실행|`eaee6360a23c9415353e02c13c9f44bf425d887b`|
|재개|원본 보존·회복 체크포인트|`a6825653a11cdfbc67b6f721c75356298e91b640`|
|보강|GIS회복검증·원장통합·비가림감사|`7a314fc78745d8fbd844ad3985376025e907e804`|
|4|RESULT·SELF_CHECK·수용·재현·공통검사|`daf15ec10f66b19637c5e72ab92a3a0c6c1ea7f6`|
|4검증|고정결과검사·원격411파일재독영수증|`1398a21f724e3b6c7ad81ee2f56b44715a5c00bd`|
|마지막|이 HANDOFF.md 하나|parent는위결과1398a21…;자기SHA는이파일안에자기참조하지않음|

중앙 dot-control.json 및 다른 소유 경로는 수정하지 않았다. 최초와 재개의 로컬 인증없는 push는 실패했지만 승인된 GitHub connector로 parent/expected head를 지정해 게시했다. 기존 branch/commit은 reset·force·덮어쓰지 않았다. 연구 산출물은 위 원격 commits로 판정한다.

## 5. PARTIAL을 남기는 이유와 최소 재개 행동

필수 모집·원판·20원저작·두 질문·연결은 충족했다. **미실행을 통과로 바꾸지 않기 때문에 행동 수용은 PARTIAL이다.** 접근 실패21행은 증거에 의한 기각과 구별했다. 새로운 조사자가 전체 모집이나 이미 끝낸 GN/H 실행을 반복할 필요는 없다.

| 남은 범위 | 막힌 이유·확인하지 않은 것 | 다음 첫 행동과 입력 |
|---|---|---|
|G01 pixel reader |raslib/server/collection과수신build가없음. 수신source는not_integrated_in_build |수신commit`ffe0c44714a491eb90ba82d8df74f621ac6003e7`과raslib/server판을함께확보해build조합확정. 같은rgb collection/checksum61774와없는collection/badquery를양쪽에실행. [REPRODUCE §3](REPRODUCE.md) |
|C01·C02·C03 역사 양판 |원PIL/scikit-learn지원환경·CPython과거쌍미실행 |C01의고정0.8/0.9source+지원의존성, C02의PIL1.1.7archiveSHA`895bc7c2…`와고정PNG SHA`78253200…`, C03의3.11/3.12에서json/없는module 입력을준비. 명령·정확SHA는[REPRODUCE §4](REPRODUCE.md) |
|G04 exact-schema |alias에서geometry/CRS는복구했지만bbox4필드추가. 실제consumer의필수subset/null계약미제공 |consumer계약을먼저고정한뒤,이미보존한SHA`f71606cd…`파일을`GEOARROW_INTERLEAVED`+`WRITE_COVERING_BBOX=NO`로변환하여구3.8reader확인. 정확명령은[REPRODUCE §3](REPRODUCE.md). 이조합은아직미실행 |
|OSS 미시험mapping/adapter |simps/cumtrapz 개별native·MAD빈형상·KDTree거리/정렬/strict경계/형adapter미완성 |[probe입력](streams/oss/probe.py)을그대로쓰고추가계약을먼저명시. O01빈(3,0)/axis1, O03점0/1/2·radius1.0과1.1;기존구별입력에서adapter를실행. [REPRODUCE §2](REPRODUCE.md) |
|실제수선·오류율 |원추천record/consumer요구미제공.조건부③만있음 |기존record1개의namespace·판·호출·필수결과를읽고해당relations행하나를적용. 전후diff와역방향복구를확인하며옛ID·원절·판정을보존 |
|과거redirect |현재GET만있고당시HTTP운영이력없음 |선택한이동당시날짜의원발행자redirect기록이나응답capture를확보. 현재301/200을소급근거로쓰지않음 |

재개 명령의 `/opt/gdal-<판>/bin/python3`는 준비할 정확 실행기의 역할 이름이며 이 세션에 그 경로가 존재한다고 주장하지 않는다. 원 실행환경의 패키지·build는 [environment-packages.json](streams/gis/historical/environment-packages.json)과 `*-explicit.txt`에 남겼다. 고정 입력·출력11파일은 결과판에 포함했고, 실행환경 디렉터리 자체는 결과로 취급하지 않는다.

**현재 판단을 바꿀 최소 확인:** 적용 대상 record 하나의 실제 consumer 계약을 먼저 확인한다. 그 계약이 exact-schema이면 G04 bboxNO 명령을, Rasdaman pixel-reader이면 server/build와동일collection을 첫 실행으로 선택한다. 새 증거는 옛 판정·인용을 지우지 않고 추가 관측과 관계 revision으로 연결한다.
