# HANDOFF — AF-RES-191

**작업자 상태 DONE (요청된 문헌 조사·설계 범위).** 특정 외부 지각 연구가 #10579에서 세 알고리즘 선택을 바꿨다는 직접 인과 및 세 후보의 지각 우월성은 **미확인**. 새 실행 또는 독립 검토의 완료를 의미하지 않는다. 중앙 진행표 변경 없음.

- 브랜치 `work/research-af-res-191`, 시작 통합 SHA `72cf39aea54e2de2ba78a245593aefdc40205a16`, 계획 SHA `0f6765df46ad2128c7fdfa92c3bf917bbfe0c5e6`, 선행 AF-RES-183 고정 HANDOFF `ed7c7278be22a5ad6eb8e87255c7d7064d12c9fb` (중앙 DONE, 자체 PARTIAL).
- 결과 본체 직전 SHA **`e89749e4f61897626c29c7e99760e7e19521460c`**. 묶음별 커밋: ① `aa1682e3e6c1508907c1579d1eaddf8e20d3e8a3`; ② `3a4722f764a33c44d8c0acc6c508ca9b05004241`; ② 보완 `64317015ff65f642617cc528f749a9b71db672ea`; ③ `6d90ae811518e3c971e1ab0e845ca73b081bd0d0`; ④ `22cc2ce94d8abd839918ee39a5c2ef4c0504b7a2`; ⑤ 본체 SHA 위. 
- 대표 파일 [RESULT](RESULT.md), [sources](sources.jsonl), [frame](frame.csv), [decisions](decisions.csv), [claims](claims.csv), [transfer](transfer.csv), [SCOPE](SCOPE.md), [SELF_CHECK](SELF_CHECK.md). 마지막 세 약점 및 다음 원자료는 RESULT 마지막 표.
- 결론: 2025-04-24 §13.2에서 단일 Local MINDE 설명, 2025-08-19 CSSWG #10579 결의로 기존 방법과 새 두 방법을 허용, 2026-01-22 f5642b931d905128daa075fdfeba6c9e74475b5a에서 실제 편집, 2026-06-23 24a74f8c006709dfbf0538af80ea3086b213228e Ray 수치 교정, 2026-08-25 §14.2 반영. 규격의 색역 내 유지, L/H 보존 지향과 세 방법 비용/품질 절충. 외부 원전은 모델의 관찰 조건·색상 균일성·JND와 장치/매체 경계를 설명한다. 근접 편집/구현 근거만으로 세 방법 허용 이유를 설명할 수 있다. 두 CRD 모두 Oklab 원저자 등재, 별도 ΔEOKr2 예제 코드의 toe에서 원저자 D09 직접 링크 확인. 이 연결을 #10579 선택 인과로 과대 주장하지 않는다.
- 원장 33행, 적격 22판·독립 자료(A4/B5/C5/D4/E4, 최소 부족 0), 21 work_id/14 lineage_id. frame 34 데이터 행(33 원장 행 + 중간 부족 보존 1); D03 산입 하향, D09 대체. 9 timeline 행, 14 claims, 6 transfer. CSS 후보 간 관찰자·조건·비교값 모두 확인된 지각 실측 0 발견; C02 별도 IPT 실험 9명/30 세션. 적격 count는 원자료 수이지 사람 실험 수가 아니다.
- 미확인: ΔEOK .02의 현대 화면·자극에 대한 직접 인간 검출 근거; 청록 개별 좌표 및 독립 출력; 실제 로고/프린트 측색·영상 직접 비교; 정확 구현 환경/버전/벤치 조건; EdgeSeeker 참조 구현 경로 접근 및 A03/A02 저자명 변화 이유; Hung/Berns 원문, CodePen, ICC 원래 entry 접근 실패(ICC WP40 대체). 개별 접근 초 미기록; living 자료 exact revision 미확인. PDF p13 IPT/Fig10, CAM16, ICC, Sharma 등 일부 실제 페이지 시각 검토; 다른 색 도표는 원문 수치·캡션 중심. 원문 판·검토범위·미확인 사항은 원장에 둠.
- **실제 자체 검증:** GitHub에서 본체 SHA의 8개 대표 파일을 다시 fetch, JSONL 33행 파싱, source_id 고유 33/33, 지정 필드 누락 0, 적격 22 및 각 분모 확인. RESULT 필수 헤더가 0/2938/6355 문자 위치 순서로 존재, 마지막 약점 표 3행. decisions 9/claims 14/transfer 6 data rows. base→본체 GitHub compare ahead 6, behind 0, 변경 8파일 모두 owned_path, 외부 변경 0. 원장·frame·판정문 내용 자체 검토. 독립 검토 없음. 코드 실행·브라우저·새 지각 실험·workbench manifest/check는 미실행. GitHub connector에서 읽기/문서 쓰기 및 JS 구조검사를 한 것이지 로컬 repo 실행 시험이 아니다.

## 첫 재개 행동

1. [RESULT 마지막 표](RESULT.md) 첫 약점부터: #10579 회의·원저자 링크에서 **0.02 ΔEOK의 실측 원출처와 선택의 직접 발언**을 찾아 관찰자/자극/배경/기기/비교값 및 날짜를 대조. 발견 못하면 미확인 유지. 이후 A02 EdgeSeeker 참고문헌 경로의 Git history와 실제 제작자 정정, PR36/44 benchmark 조건의 exact SHA를 확인. 사진/인쇄는 특정 프로필·용지·기기에서 측색된 공개 기록에 한해서 보완. 새 브라우저 실행·신규 지각 실험은 이 연구의 제외 범위이므로 무단 수행하지 않음.
2. 후속 담당자가 checkout에서 구조 검증을 요구하면 아래는 **미실행 제안**. Codex Cloud의 깨끗한 임시 checkout, Git/Python 3, network read 허용; agentflow 변경은 owned_path만. 입력은 결과 본체 SHA, 시작 SHA, 해당 8 파일. HANDOFF는 그 다음 커밋. 기대 관측: changed paths 8개 모두 prefix; source 33/22/5개 category quota; 3 weakness rows. 통합 진행표는 건드리지 않음.

```sh
git fetch origin
git checkout --detach e89749e4f61897626c29c7e99760e7e19521460c
git rev-parse HEAD
git diff --name-only 72cf39aea54e2de2ba78a245593aefdc40205a16 e89749e4f61897626c29c7e99760e7e19521460c
python - <<'PY'
import csv,json,pathlib,collections
p=pathlib.Path("docs/workstreams/research/AF-RES-191")
s=[json.loads(x) for x in (p/"sources.jsonl").read_text().splitlines() if x.strip()]
i=[x for x in s if x["included"]]
assert len(s)==len({x["source_id"] for x in s})==33
assert len(i)==22
assert dict(collections.Counter(x["category"] for x in i))==dict(A=4,B=5,C=5,D=4,E=4)
for name,n in [("frame.csv",34),("decisions.csv",9),("claims.csv",14),("transfer.csv",6)]:
    with (p/name).open(newline="") as f:
        assert len(list(csv.DictReader(f)))==n
t=(p/"RESULT.md").read_text().strip().splitlines()
k=max(j for j,x in enumerate(t) if x.startswith("| 불일치·약점 |"))
assert len(t[k+2:])==3
print("structural checks only")
PY
```

후속 검사 결과가 기존 수치를 뒤집으면 원값과 이유를 새 커밋에 보존. 실행 환경·exit code·입력 SHA 기록. 필요하면 workbench CLI help를 읽고 별도 manifest 허용 경로 확인; 이번 문헌 과제에서는 추가 제품 구현·검산을 하지 않았다.

## 색인 제안
AF-RES-191 — CSS Color 4 2025/2026 CRD + #10579 실제 3 GMA 선택/정밀도 편집, 원저자 인용·지각 연구의 적용 조건과 비용 선택 분리, 단색/사진/인쇄 전이 실패, 22 직접 자료 및 9 결정 단위 (문헌 조사 DONE; 지각 인과/실측 미확인); docs/workstreams/research/AF-RES-191/RESULT.md.
