# 공통 검사 Git 이력 보완

대상은 detached source `7a314fc78745d8fbd844ad3985376025e907e804`이며 검증 worktree는 `verification/source-check`다. 최초 공통검사는 공통55·lab7/9를 통과한 뒤 Git bundle 복원에서 부모 `320424d87f99e70c42eeb8cb7211467de27f2c2e`가 없어 종료1이었다. 최초 로그·영수증은 `evidence/resume/common-source-check.json`, `common-check-native-receipt.json`, `common-acceptance.stdout.log`에 그대로 보존한다.

읽기 진단에서 저장소가 shallow이고 경계가 `95688ccbc0550b03bb96c3933a35cfb0b51ca3e2` 한 개임을 확인했다. 검사기는 `git bundle create --all HEAD` 후 별도 디렉터리에 clone하므로 그 얕은 경계 밖의 부모가 필요했다. 소스나 검사기를 바꾸지 않고 공개 원격에 아래 명령을 한 번 실행했다.

```bash
git fetch --unshallow --no-tags origin work/research-af-res-079
```

2026-11-23 12:28:41–12:28:55 UTC에 종료0, shallow=false가 되었으며 source SHA는 그대로다. 누락됐던 부모도 commit 객체로 확인했다. branch reset·force·overwrite·push·commit은 하지 않았다. [취득 영수증](fetch-unshallow.json)과 [후속 진단](recovery-result.json)에 정확 명령·출력·시각을 남겼다.

같은 clean source에서 `python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean`을 12:29:18–12:29:29 UTC에 한 번 재실행해 종료0을 얻었다. doctor, acceptance, research-case, original-smoke가 통과했고 Git bundle 복원도 통과했다. sessions 명령은 종료0이지만 내용은 `no_active_sessions` / `not-executed`이므로 개별 AF-RES-079 계약 검사의 대체가 아니다. 실행환경 명칭은 호출자 label이며 별도 계정 연결의 증거가 아니다.

재시도 증거는 `evidence/resume/common-retry-check.json`, `common-retry-native-receipt.json`, `common-retry-acceptance-native.json`과 같은 접두사의 각 stdout/stderr에 있다. 이 검사는 고정 source7a314fc에 대한 검사이며, 이후 보고서·수용 문서 커밋이 그때 이미 검사됐다고 주장하지 않는다.
