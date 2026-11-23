# AF-RES-094 인계

**연구 상태 PARTIAL.** 2026-11-23 UTC에 두 수단으로 24경로·12대응쌍·34문서 시도를 남겼다. 엄격 충족 4/24, 접근 실패 20/24, 최종 미확인 0/24다. 본문 8/24, 후속 4/16이며 P1의 7.0.1 당시 서비스 귀속은 4행 모두 미확인이다. 직접 외부 1차 자료 43건과 독립 저작·사건 계보 17개를 기록했다. [결과](RESULT.md), [자가검산](SELF_CHECK.md)

bandersnatch는 A의 문자 URI와 B의 명시 링크가 같은 PyPI 홈페이지에 두 번 안에 도달했다. 수단별 B만 0/6, A만 0/6이고, 양쪽에서 서로 다른 실제 두 번째 URL을 요청한 분모는 0이다. P3와 R2 공통 입구, R1 후속 주소는 이 환경에서 CONNECT 403/브라우저 터널 실패로 막혔다. 정상 origin 판정과 B가 다른 URL을 주는 실제 이득은 남아 있다. 고정 R1/R2 blob은 같은 구간에서 각각 두 수단 200을 얻었다.

R2의 2.3.1 트리에 남은 두 TITLE SVG는 2022-07-05 변경 파일이다. 1.0.0.9000 문서의 실제 img src 및 파일 바이트와 일치하고, 2.3.1의 Using SVG files에는 이 URI가 없다. 옛 파일을 새 판 생성물로 격상하지 않았고 R2 B의 추가 주소는 미확인으로 유지했다. IIIF는 공개 manifest를 읽었으며 필수 JPEG payload는 회수하지 못했다. EPUB Moby-Dick의 내부 JPEG는 회수했다. [R2 계보](evidence/r2-asset-lineage.json), [payload 비교](evidence/payload-audit.json)

## 원격 커밋

| 묶음 | 원격 SHA |
|---|---|
| 시작 통합판 | `f72073277e6be643302a33f204d70baeb2c749a4` |
| ① 목적·카드·순서·판정 봉인 | `51b8047d2272b960716266f7d0f3228aa9429b5c` |
| ② 수단별 양성·음성·수집 절차 | `3338808acf7156ea4d70dd74839004a5268aa5c7` |
| ③ 24경로·원 응답 영수증·반례 | `237b6a244b4cf2705f7a0064f62b460ba47cf28b` |
| ④ 대응표·권고·자가검산 및 검사 대상 | [082ba3b787edd92d804bf617397743e89d75c5f0](https://github.com/laadkke-arch/agentflow-open/commit/082ba3b787edd92d804bf617397743e89d75c5f0) |
| 결과판 검사 및 원격 재열람 영수증 | `eef4c898f8a9677bbab63776e3e36d6ca3a57c15` |

이 HANDOFF는 마지막 단독 커밋에서 연 파일이다. 브랜치 `work/research-af-res-094`, 소유 경로 `docs/workstreams/research/AF-RES-094/`. 의존 `work/research-af-res-090=e5f6cf5b1cb27b926ebc2356f9a8b763cebfcc87`. 090의 읽은 결과판은 `03c6102d6c0d90f6722550d5e2cb1c7219e49b5f`다. [계약](manifest.json), [범위](SCOPE.md)

## 읽을 파일

- [RESULT.md](RESULT.md), [SELF_CHECK.md](SELF_CHECK.md), [counts.json](evidence/counts.json)
- [cards.csv](cards.csv), [traversals.jsonl](traversals.jsonl), [pairs.csv](pairs.csv), [sources.jsonl](sources.jsonl)
- [주 영수증과 화면](evidence/main/), [보조 payload 판별](evidence/payload-audit.json), [실행 재현](reproduce.md)

## 결과판 확인

| 실제 확인 | 결과 |
|---|---|
| `python -B -m workbench.session check docs/workstreams/research/AF-RES-094/manifest.json --fetch` | 종료 0. passed, remote_checked, 범위 밖 파일 0 |
| `python -B docs/workstreams/research/AF-RES-094/tools/measure.py --verify` | 종료 0. 24행·12쌍·표 2·분모 및 원장 하한 일치 |
| `python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean` | 종료 0. 시작·끝 clean·동일 SHA |
| 위 wrapper가 실행한 `python scripts/check.py --require-git` | 종료 0. 공통 55개와 lab 7개·9개 테스트 및 acceptance 통과 |
| GitHub 결과 SHA 재열람 | 핵심 문서·원장·반례 17파일 바이트 일치. cards.csv의 첫 raw GET 실패와 200 재조회는 따로 기록. GitHub Connector blob도 일치 |

검사는 2026-11-23 18:32:57–18:33:04 UTC에 **④ 결과 SHA**에서 실행했다. 공통 wrapper의 check-all은 no_active_sessions이고, 명시적 manifest check가 이번 계약을 검사했다. [검사 영수증](evidence/validation/checks.json), [원격 재열람](evidence/validation/remote-readback.json)

R/Python 예제, SVG/cast 재생, IIIF viewer, EPUB reader 실행은 미실시다. 정적 문서와 payload 판독을 측정했다. 원응답 전체는 임시 검산에 사용했고 커밋에는 응답별 상태·지문·DOM/파일의 판별 표본과 화면을 저장했다. 프록시에서 막힌 두 브라우저 행의 DOM 발췌는 미확인이고 오류 이벤트와 화면은 있다. [재현 절차](reproduce.md)

## 다음 첫 행동과 약점 3건

**첫 행동.** 고정 카드와 결과판을 읽고, 대상 origin을 열 수 있는 실행 환경에서 별도 공개 대조를 통과시킨 뒤 동결 카드로 새 UTC 회차를 만든다. 이전 24행과 접근 실패는 보존한다. [봉인 URL과 순서](freeze.json)

```sh
af_root=docs/workstreams/research/AF-RES-094
node "$af_root/tools/collect.cjs" preflight "$af_root/evidence/preflight/recheck-UTC" /tmp/af094-recheck-control
node "$af_root/tools/collect.cjs" main "$af_root/evidence/recheck-UTC" /tmp/af094-recheck-main
python -B "$af_root/tools/read_sources.py" /tmp/af094-recheck-IIIF "$af_root/evidence/recheck-IIIF.json" IIIF-CANVAS IIIF-PAINTING
```

1. **정상 origin에서의 카드 이득.** 입력은 같은 여섯 목적·두 카드·두 수단이다. P3 A의 실제 메뉴 URL 또는 B만 읽히는 정확 root, R2 실문서 결과가 확보되면 이번 환경에서 공란인 판정이 바뀐다. IIIF의 필수 JPEG는 위 정확 URL에서 image/jpeg·3186×4612와 원 SHA를 확인한다.
2. **독자 조작 비용.** P1·R1의 같은 카드를 열고 실제 독자의 링크 선택·문자 복사·중단을 기록한다. 실제 링크가 같아도 B만 완료하거나 A/B에서 선택 오류가 갈리는 관측이면 독자 비용 해석을 고친다.
3. **역사 판과 후속 자원의 연결.** R1의 `45e0d9eb…` 생성 job R.VERSION과 그 판의 system.file 매뉴얼을 맞춘다. R2는 `92fecbc0…` 해당 절과 실제 생성 payload를 지목하는 발행자 기록 및 지문을 찾는다. 원 R판이 연결되거나 2.3.1의 새 SVG/cast와 실제 참조가 검증되면 그 판정이 바뀐다.

**색인 제안** · AF-RES-094 | PARTIAL | 같은 입구에서 후속 링크의 24경로 대조 및 SVG 파일 계보 반례 | docs/workstreams/research/AF-RES-094/RESULT.md | depends AF-RES-090@e5f6cf5b1cb27b926ebc2356f9a8b763cebfcc87

중앙 진행표와 색인 갱신은 진행 담당의 범위다. 결과판에서 시작 통합판 대비 소유 경로 밖 변경 0과 dot-control.json의 동일 바이트를 확인했다.
