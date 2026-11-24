# AF-RES-159 HANDOFF — PARTIAL

## 식별과 고정판

- AF-RES-159 시도 1, Codex Cloud Linux. 저장소 `laadkke-arch/agentflow-open`, 브랜치 `work/research-af-res-159`, 허용 경로 `docs/workstreams/research/AF-RES-159/`. 한 작업자가 판독·사전 봉인·실행·자가 검산을 맡았다. 독립 검토와 실제 사용자 조사는 미실시.
- 계획판 `ff5a037d4926e5c3ce6032bfa22c75b62f3c6aa8`, 배정 때 관측 `02b3d3ca638c8f8cd7431c0a22ddbc83863d8f98`, 실제 세션 기준판 `ff2302a9c02fe72eea915dc1612d1791d5c780ec`. 계획판 대비 중앙 진행표 +98/−6, 계약 파일 차이 0. 선행 AF-RES-155 결과는 `9a62426f9a989c3c0fff513f66a63d68484cbe3c`. [SCOPE](SCOPE.md) [session.json](session.json) [155 인계](https://github.com/laadkke-arch/agentflow-open/blob/9a62426f9a989c3c0fff513f66a63d68484cbe3c/docs/workstreams/research/AF-RES-155/HANDOFF.md)
- **내용 결과판** `1c54a74f95031f1af250d337ab82fe59d9d88015`. **검증 영수증 포함 결과판** `dfd6feb005aabf0818d12cdf4e0e6a27345ab7f9`. 두 SHA 모두 새 checkout에서 검사했다. 차이는 ①–⑤의 원격 재열람 영수증과 첫 checkout 검증 영수증 두 파일이다. 이 HANDOFF는 뒤의 단독 커밋이다.

## 판독과 재개에 필요한 결과

- GIMP 3.0.6 태그 커밋 `a77e8fd05d3d08a58650531a3700100f6a3216b7`, Inkscape 1.4.3 `0d15f7504220b00925bc3cb3673fcf44610a17d5`, Inkscape 번역 gitlink `dd0592f12a5da07802a96b53293bbe12acdf45ff`. 고정 ko/de PO 네 자리, 자연 짝 12, 단일 대조 4, 실제 소스 연결 28. 공식 GIMP dist tar의 바이트와 업스트림 설치본 MO는 다운로드 403으로 보류했다. Inkscape 공급자 서명 tar와 Debian 발행 MO는 확인했다.
- 개봉 전 280개 판정 중 자연 48 호출×언어에서 A/C는 모두 다중, 실제 앵커 A+위치는 46, B는 48, 직접 키는 42를 한 기능으로 이었다. 단일 대조의 A는 8/8이었다. 공용 enum/위젯 소비 G06b는 B의 실제 역할이 필요했다. 직접 키로는 3호출의 별개 소비자를 가르기 어려웠다.
- 자연 24 그룹×언어에서 조회 값 19 동일, 5 상이. 문맥 조회 56자리의 54는 활성 MO 번역, 2는 ko fuzzy 원문 반환. 발행 코드를 읽은 범위에서 보고했으며 실제 앱 창·키 가속기·글리프 확인은 미실시. G15의 공용 핸들러 및 G35의 한국어 공백을 별도 재생했고 잘못된 실재 키 48자리 중 38은 실제 키와 같은 문자열을 냈다.
- 출처 136열람, 그중 29 고유 1차 저작 및 접근 실패 13. 지명 2사례·문화 2사례에서 엔티티 고유 주소와 이름에 부가 필드가 필요한 상황을 대조했다. C 사후 대조는 같은 파일의 위치 상관과 타 파일의 잘못된 확신을 보여 준다. [결과표와 Q1–Q7](RESULT.md) [반례](evidence/counterexamples.md) [출처](sources.jsonl) [자기 검산](SELF_CHECK.md)
- 색인 제안은 **AF-RES-159 / PARTIAL / 동일 UI 문구의 구현 링크와 번역 키 / GIMP 3.0.6 및 Inkscape 1.4.3 / RESULT.md / AF-RES-155 고정 의존**이다.

## GitHub 저장과 재열람

| 묶음 | GitHub에서 확인한 SHA | 실제 대표 파일 |
|---|---|---|
| ① 범위·규칙·manifest | `48bd0d052c55c8081c940681cd9a74513591e4e7` | SCOPE.md |
| ② 모집과 개봉 전 봉인 | `8000ac5d54c7564bb5cec61566e13ea8d78980f1` | predictions.csv, packets.jsonl |
| ③ 본 관측 | `49f4ab275460d0b4368b363b983fdf40c56c8621` | runs.jsonl |
| ④ 반례·누락·비용 | `55f9daa201b69008918d798a579e501b8a019f6c` | sources.jsonl, evidence/counterexamples.md |
| ⑤ 결과·자기 검산 | `1c54a74f95031f1af250d337ab82fe59d9d88015` | RESULT.md, SELF_CHECK.md |
| ⑤ 새 checkout 영수증 | `dfd6feb005aabf0818d12cdf4e0e6a27345ab7f9` | evidence/fresh-verification.json, 17:30:40 UTC, SHA-256 `6cfb886adf02350896f1ec242396ed5d322496fb8e85be2ab56ed351cd068f1a` |

[원격 재열람](evidence/remote-receipts.tsv)은 브랜치 SHA 및 파일 원바이트를 대조한 UTC·지문·exit 0이다. 사전 비교와 입력은 마지막 결과로 덮어쓰지 않았다.

## 새 checkout의 검사

두 검사는 2026-11-24 17:29:08–17:29:56 UTC(내용 결과판), 17:30:59–17:31:23 UTC(영수증 포함판)에 실행했다. Git 2.52.0, Python 3.12.14, GNU gettext 0.23.1, GLib 2.84.4, glibc 2.41, GCC 14.2.0. [첫 checkout 명령·UTC·종료·입력/출력 지문](evidence/fresh-verification.json)

| 영수증 포함판 dfd6feb0에서 실제 실행 | 종료와 UTC | 재확인 |
|---|---|---|
| `python -m workbench.session check docs/workstreams/research/AF-RES-159/session.json --fetch` | 0, 17:30:59–17:31:00 | remote_checked. 30개 변경 경로, 외부·미병합·오류 0. 통합 `ded3420249a3d60ebbb578a8432cf262d3ffa7d7`, 의존 155 고정. stdout `a1cebace4754b538848052971d6c34a441e88c263451b606766c7d61d4e14455` |
| `python scripts/check.py --require-git` | 0, 17:31:00–09 | 공통 단위 55, lab 7·9, 데모, 독립 export, Git bundle 복원. stdout `33d516da808176dfc048e9f50dc8a7d7be27b0f24ed94cdeaf61de290f9bd5f6` |
| `python scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean` | 0, 17:31:09–18 | doctor·acceptance·reference-audit discovery·원래 smoke·sessions 명령 통과. check-all의 docs/tasks 감지는 no_active_sessions. 이 폴더 계약은 별도 위 명령. JSON 영수증 `c13f29266e493ca6e2d669c44d2658b17f41d3ac80ee70de47209091992b7d8d` |
| `frame.py`, `seal.py`, 봉인 4파일 cmp | 각 0, 17:31:18–19 | 17:04:34 UTC 사전판 타임스탬프 재사용, frame/calls/packets/predictions 바이트 일치 |
| `run.py --repeat verify` 본 및 `--phase supplement`, `check.py --compare-main … --compare-supplement …` | 각 0, 17:31:19–23 | 328 본 조회와 12 보충 조회의 입력·MO·출력 지문이 주 실험과 일치. stdout main `ea2578f4404ea32bc1ab406c1f23ac492c68eeedcb1000ff02122e03038fb4f5`, supplement `6bc49cc60df49d65e83e225aef268e92e44b18a05098f8ac59176d5b42e7c9ec`, check `1c0f0819b4921c5b0ce7da7b0081d65aa68e70de549b5cfdb5c1d428b6fea092` |
| `score.py`, 판정·C 민감도 cmp, `git diff --check BASE HEAD`, `git status --porcelain` | 각 0, 17:31:18–23 | 채점·C 바이트 일치, 소유 경로 바깥 0, checkout clean |

프로젝트 입력은 [파일 SHA-256과 argv](evidence/fresh-verification.json)를 함께 보존했다. 양 검사에서 `session.json`은 `26909d14d4613a1cf2c11ac4232b339aeec9f31c902cc1c2df2601384eb13850`, `packets.jsonl`은 `ce3df4f4f94c6342eb8d11cd380941cb7581a32e65feeb386f7a8b4260cf7b0b`, `runs.jsonl`은 `c7ac6668a315af519df865fc1d0053deda07c60b70478ae3c0116969704fbe95`. 발행 원 입력 PO·tar·MO 지문은 [release-inputs.md](evidence/release-inputs.md)에 있다.

## 다음 첫 행동

공식 GIMP 3.0.6 tar를 받을 수 있는 승인된 실행 환경에서 **공식 지문을 먼저 확인한 뒤 ko/de의 tar 파일을 태그와 비교**한다. 아래 입력은 GIMP 공식 목록의 고정 3.0.6이다. 기존 결과는 영수증 포함 SHA로 검산한 후 새 원본을 별도 결과로 남긴다.

```bash
af159_checkout=$(mktemp -d /tmp/af159-checkout.XXXXXX)
git clone --no-tags --branch work/research-af-res-159 \
  https://github.com/laadkke-arch/agentflow-open.git "$af159_checkout"
cd "$af159_checkout"
git checkout --detach dfd6feb005aabf0818d12cdf4e0e6a27345ab7f9
af159_scope=docs/workstreams/research/AF-RES-159
af159_inputs=$(mktemp -d /tmp/af159-inputs.XXXXXX)
bash "$af159_scope/replay/bootstrap.sh" "$af159_inputs"
python -m workbench.session check "$af159_scope/session.json" --fetch

curl -fLsS https://download.gimp.org/gimp/v3.0/gimp-3.0.6.tar.xz \
  -o "$af159_inputs/gimp-3.0.6.tar.xz"
printf '%s  %s\n' 246c225383c72ef9f0dc7703b7d707084bbf177bd2900e94ce466a62862e296b \
  "$af159_inputs/gimp-3.0.6.tar.xz" | sha256sum -c -
for af159_lang in ko de; do
  tar -xOf "$af159_inputs/gimp-3.0.6.tar.xz" "gimp-3.0.6/po/$af159_lang.po" \
    > "$af159_inputs/gimp-dist-$af159_lang.po"
  cmp "$af159_inputs/gimp-dist-$af159_lang.po" "$af159_inputs/gimp/po/$af159_lang.po"
done
```

공식 바이너리 쪽은 [GIMP 3.0.6 x86_64 AppImage](https://download.gimp.org/gimp/v3.0/linux/GIMP-3.0.6-x86_64.AppImage)의 해당 파일을 내려받아 [공식 SHA256SUMS](https://download.gimp.org/gimp/v3.0/linux/SHA256SUMS)로 검증한 다음 임시 폴더 안에서 `chmod u+x GIMP-3.0.6-x86_64.AppImage`, `./GIMP-3.0.6-x86_64.AppImage --appimage-extract`, `find squashfs-root -path '*/LC_MESSAGES/gimp30.mo' -type f`를 실행한다. ko와 de MO 경로를 확인하고 상위 locale 디렉터리를 아래 `--shipped-gimp`에 넣는다. Inkscape 공식 같은 버전 패키지를 구한 경우도 `find EXTRACTED -path '*/LC_MESSAGES/inkscape.mo' -type f`로 MO를 찾아 `--shipped-inkscape`를 실제 패키지 디렉터리로 바꾼다. Debian과 원 패키지 출력명을 별도 보존한다. 실행 GUI에서 메뉴의 실제 가시성이나 사용자의 질문 효과를 확인하려면 별도 조사가 필요하다.

```bash
export LD_LIBRARY_PATH="$af159_inputs/tools/usr/lib/x86_64-linux-gnu"
export GETTEXTDATADIR="$af159_inputs/tools/usr/share/gettext-0.23.1"
python "$af159_scope/replay/run.py" \
  --gimp "$af159_inputs/gimp" --inkscape "$af159_inputs/inkscape" \
  --msgfmt "$af159_inputs/tools/usr/bin/msgfmt" \
  --gettext "$af159_inputs/tools/usr/bin/gettext" \
  --shipped-inkscape "$af159_inputs/published-inkscape/usr/share/locale" \
  --repeat verify > "$af159_inputs/verify-main.jsonl"
python "$af159_scope/replay/run.py" \
  --gimp "$af159_inputs/gimp" --inkscape "$af159_inputs/inkscape" \
  --msgfmt "$af159_inputs/tools/usr/bin/msgfmt" \
  --gettext "$af159_inputs/tools/usr/bin/gettext" \
  --phase supplement --repeat verify > "$af159_inputs/verify-supplement.jsonl"
python "$af159_scope/replay/check.py" \
  --gimp "$af159_inputs/gimp" --inkscape "$af159_inputs/inkscape" \
  --compare-main "$af159_inputs/verify-main.jsonl" \
  --compare-supplement "$af159_inputs/verify-supplement.jsonl"
python scripts/check.py --require-git
python scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean
```

| 불일치·약점 | 영향을 받는 결론 | 다음 조사·자료 | 결론을 바꿀 관측 |
|---|---|---|---|
| GIMP 공식 dist tar/원 MO 다운로드 거부, Inkscape 원 설치판 MO 공석 | 발행 원 바이너리 포함·표시값을 확인할 수 없음 | 동일 SHA의 소스 tar 및 공식 패키지에서 ko/de 파일을 위 절차로 비교 | 실제 발행 PO/MO 포함·활성 키·바이트가 태그나 로컬 재생과 다름 |
| 같은 연구자의 기술적 역참조. 사용자 응답과 렌더링 관측 공석 | B/C 및 A+위치의 질문 횟수·유용성 일반화 불가 | 같은 화면의 첫 입력에 앵커가 있던 참가자와 없던 참가자를 비교 | 앵커나 실제 역할이 있을 때에도 유일 출처 합의가 바뀜 |
| 자연 표본은 12개로 제한되고 C는 같은 파일에서 고른다 | 기술적 구별 가능성과 무관 이웃의 우연 일치에 대한 외삽 제한 | 다른 UI 도메인에서 먼저 모집하고 실제 독립 이웃의 예산 대조를 재현 | 무관 이웃의 적격성이 검증되거나 후보를 가르는 최소 근거가 달라짐 |
