# AF-RES-173 HANDOFF — PARTIAL

## 상태 및 고정판

- 중앙 진행표에 173 RUNNING, attempt 1, depends_on 165, result_commit null이었으며 이번 작업은 중앙 상태를 수정하지 않았다. 중앙 완료 상태가 아니라 이 작업의 자체 판정 PARTIAL이다.
- 계획 통합 기준 53eaa286136019510f052179f5f51d901bdac858, 실제 시작 2ca38b464dcf72fc2570d77f44cc29ee7c9a4cbc. 시작 차이는 dot-control.json +207뿐.
- 선행 AF-RES-165 fixed 2c9e6495c19079006eb5612a3ee76a09d5c5f1da: 중앙 DONE과 그 작업자의 PARTIAL을 구분. HANDOFF 직접 읽음; 기존 jpeginfo/darkslide/FreeCAD/Fedora 사례 재모집 안 함.
- 결과 고정 SHA **95a46b1769b23478586455f1d88866f4ce839a4f**; 브랜치 work/research-af-res-173; 이 HANDOFF의 최종 SHA는 파일 자체에 자기참조할 수 없으므로 커밋 응답으로 확인. 모든 파일은 docs/workstreams/research/AF-RES-173/ 안에만 씀.

| 단계 | 대표 커밋 SHA | 재열람 |
|---|---|---|
| ① SCOPE | 9cf20363a817fdc538583bdf268b763984ad881b | 동일 본문 확인 |
| ② sources 첫 묶음 | 014914e061c262d473bfe1cdac893a8b303c7bbe | 동일 본문 확인 |
| ② frame | 75bfd6ef21217b0c2432dab60d3f579327786048 | 동일 본문 확인 |
| ② source 정정/고지·정확판 source 목록 추가 | 3bcb2a71f6eefd545246f7c2d705224b6e2a1894 | 동일 본문 확인 |
| ③ substitutions | ffc7bd8f50c2770d9ffc9aa41f5d87a765a3ba35 | 동일 본문 확인 |
| ③ outputs | 30afaae84cf2f81ed9432e7b863277cdbc8e5f8a | 동일 본문 확인 |
| ④ 반례 기반 권고 범위 | 23a9e3407233065c26929a81c38f8e4f0f7155d8 | 동일 본문 확인 |
| ⑤ 결과 | a2f76878276a5b8733ddcd21e47518358b750d50 | 동일 본문 확인 |
| ⑤ 날짜 보정 | 0ff19a6b7e6ad1279827c972c48f1d627e279ec3 | 동일 본문 확인 |
| ⑤ 자체검산 | 95a46b1769b23478586455f1d88866f4ce839a4f | 동일 본문 확인 |

대표 파일 RESULT.md(표1~3, Q1–7, 대안, 약점), SELF_CHECK.md, sources.jsonl, frame.csv, substitutions.csv, outputs.csv, advice.csv. 61 source rows, open45/failed16, counted unique works35/lineage labels28. frame 66 rows (LO fallback search38, 13 read/25 unread; planned8 unresolved; B16; P4), observations13, strict pairs0, report-only1, multi-change excluded2, expected/observed2. Exact release archive0/4, same-document strict QA0/4, two physical editions page comparisons0/4, producer records4. Source packaging decisions5 (not actual archive inclusion). Strict first four per product 0/8. Other typeface exact original versions, original license conditions, physical glyph/line/page comparison and Q5 specified controlled counterexamples unknown.

## 첫 재개 행동

새 사례 검색으로 채우지 말고 먼저 원모집 순서를 복구한다. S01 Bugzilla query(접근 실패), S02 ReleaseNotes(Anubis), S03 TUG(403), S10 historical TL2024 directory(읽음), S11 full db(19MB 오류), S47/S48 archive directory(timeout). frame.csv의 LO 38개 URL 순서/25 미열람을 최초 보고 및 official release dates로 확인하고 TL chronological package announcement/history를 정렬한다. 결과를 보지 않은 다른 작업자가 모집 조건을 적용하면 결과 오염 위험을 줄일 수 있다. 4+4 최초 적격의 named document and version을 고정하고 제외 사유/동률 확인. 다음에는 O01의 공통 입력을 먼저 확보. 두 font의 사용·입수 허가와 정확판, 재현 환경이 고정되기 전 실행하지 않는다.

## 후속 명령 (미실행)

웹 작업자는 공개 기록 내용만 해석했다. 로컬 Git CLI/빌드/렌더/Codex 실행·독립 검토 없음. GitHub connector에서 고정 SHA 본문 동일성 검산 및 비교만 했다. 후속 실제 실행 담당에게 입력:

```sh
# 저장소 diff 및 범위 검증
git fetch origin chore/workspace-foundation work/research-af-res-173
git diff --check 2ca38b464dcf72fc2570d77f44cc29ee7c9a4cbc 95a46b1769b23478586455f1d88866f4ce839a4f
git diff --name-only 2ca38b464dcf72fc2570d77f44cc29ee7c9a4cbc 95a46b1769b23478586455f1d88866f4ce839a4f
git log --format='%H %s' 2ca38b464dcf72fc2570d77f44cc29ee7c9a4cbc..95a46b1769b23478586455f1d88866f4ce839a4f
python -m workbench.session --help

# TL historical DB (공개 읽기 전용; 임시 디렉터리에서 실행)
# 정확 연도 고정; checksum/서명 원문도 같이 확보, db 추출 전 검증
curl -fL 'https://ftp.math.utah.edu/pub/tex/historic/systems/texlive/2024/tlnet-final/tlpkg/texlive.tlpdb.xz' -o texlive-2024.tlpdb.xz
sha512sum texlive-2024.tlpdb.xz
xz -dc texlive-2024.tlpdb.xz > texlive-2024.tlpdb
awk 'BEGIN{RS=""; FS="\n"} /^name (frenchmath|unbtex|stickstoo|stix2-type1|tex-gyre|newpx|newtx)\n/{print $0 "\n"}' texlive-2024.tlpdb
# 2023 final 역시 같은 공개 경로의 2023 디렉터리; 각 실제 package archive 주소는 DB와 directory 검증 후 확정.
# tar -tf downloaded_exact_package.tar.xz ; sha256sum downloaded_exact_package.tar.xz

# LibreOffice의 공개 core clone에서 O01 source before/after 확인
git show ec73b2894009a4cbb3446f8370b3de7bbbd5a35f^:chart2/qa/extras/data/pptx/tdf146756_bestFit.pptx > before.pptx
git show ec73b2894009a4cbb3446f8370b3de7bbbd5a35f:chart2/qa/extras/data/pptx/tdf146756_bestFit.pptx > after.pptx
sha256sum before.pptx after.pptx
unzip -l before.pptx
unzip -l after.pptx
# 실제 파일 경로를 commit diff와 재대조; 경로 오류면 git show --name-only <SHA> 사용.
# unzip 후 XML 변경이 font 외에도 있으면 엄격쌍으로 쓰지 않음.
# 권한 있는 양쪽 정확 TTF를 확보한 뒤:
# sha256sum original.ttf substitute.ttf
# fc-match 'Calibri'; fc-match 'Carlito' (격리한 fontconfig에서)
# 동일 input/renderer/options로 렌더 후 pdfinfo, pdffonts, pdftotext -layout 비교
# 정확 문자열/언어/script/direction 고정 후 hb-shape font.ttf 'STRING' --script=... --language=... --direction=...
```

4.4.0.3 LO source recipes S59–S61은 실제 installer가 아님. 정확 OS/arch release archive와 내부 TTF hash/notice를 별도로 확인. O01 파일의 실제 경로 및 원/후 입력 동일성이 확정되면 동일 문서의 broken/fixed 상태별 숫자, 실제 line/page/glyph를 분리해 검정. font 변경 외의 다른 변화는 제외. 실패/미입수는 그대로 원장에. 저장소 세션 manifest와 검사 실행은 별도 승인/환경 규칙을 따라야 함.

색인 제안: AF-RES-173 PARTIAL — 글꼴 대체의 파일 포함·선택·동일 출력 증거 분리, 35 원자료/28 계보, 자연 모집·엄격쌍 미완료; RESULT와 SELF_CHECK 참조.
