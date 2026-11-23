# AF-RES-067 — 모집·증거 계약 (부분 인계)

- 계획 통합 기준: `028d16fee1121f5862efd410b78ec1d79d7080f2`; 실제 분기 기준: `374dc309454e8847603c133c4c1d1029d63c0c92` (GitHub fetch_commit에서 확인). 의존 인계 `AF-RES-063@8e348bb1306d5243b0a5ff8ebae773707d2dcfb4`, 선행 본문 `86403f9082bfebe9eafefe00e673942380041761`.
- 배정자 제시 작업 ID AF-RES-067#1; 권한 경로 `docs/workstreams/research/AF-RES-067/`; 공통 진행표·타 경로 수정 금지. `dot-control.json`의 GitHub fetch_file 응답은 blob SHA `af867733d1cbfac88f181845bbf1dac56089bf91`이나 본문 길이 0이었다. 항목 존재/내용은 **미확인**. 연결환경에서 `workbench.session start` **미실시**; 가상 manifest를 만들어 통과라 하지 않는다.
- 기간 2024-01-01~2025-12-31 UTC. Debian 공식 archive/snapshot/tracker/buildd/buildinfo에서 jq, pandoc 별 amd64 바이너리 산출물 최초 공개/수록일+source version+attempt 키로 각각 첫 두 사건. 같은 업로드의 deb 다수/미러/서명은 한 사건. rebuild는 보조.
- MAST JWST NIRCam 영상의 공개 Level 2 단일 노출 `_cal.fits`; F200W/F444W 각각 최초 두 제품. `t_obs_release` 및 자료공개일을 확인하고 별도로 기록; observation/product ID 순. 같은 노출의 재처리판은 보조. 질의 페이지/수/제외/스냅샷 없이는 전역 '첫 두 건'이라 주장하지 않는다.
- 이 세션의 MAST API·Debian snapshot/buildd 원 카탈로그 직접 API는 웹 도구에서 접근 오류였으므로 **8자리는 배정은 했으나 사건으로 확정하지 못함**. 원목록 없는 행은 '모집 미완'이며 원본 자체 부재가 아니다. 풍부한 문서로 임의 교체하지 않음.

## 증거 등급

D=제작자 사양·선언, K=고정 파일·배포·dependency lock, I=동일 실행 설치/처리 영수증, L=동일 실행 선택/공급자 이름, H=동일 소비 실행의 실제 읽은 파일 바이트 지문과 출력의 연결; O=실제 원 출력(저자 또는 보관 실행), X=지금 연구자 재계산(과거 증거 아님). buildinfo Installed-Build-Depends는 설치되어 **영향 가능**한 패키지이며 도구 호출 영수증은 아니다. CRDS_CTX는 규칙 맵이고 R_FLAT은 선택 참조 이름일 수 있어 실제 파일 바이트 사용의 H가 아님. 서명은 서명 파일/대상에만 귀속. FITS CHECKSUM도 특정 FITS 데이터 범위의 무결성과 실행 당시 로드파일 증명을 구분.

## 보기·부재 분류

V0=주소+짧은 이유; V1=V0+실제 확인된 식별자·발행시각·출력지문; V2=V1+동일실행 입력·처리/로드 원기록 **실제 있는 경우만**. 8자리×3=24셀 고정, 보강사례 분모 밖. `미확인`=확인 자료 부족, `관측 0`=정해진 범위에서 센 0, `해당 없음`=분모 미정, `미실시`=행동을 하지 않음. 수신 byte는 도구가 실제 제공하지 않아 미확인. URL 열람 건수와 다운로드 바이트 별개.

## 재개 최초 명령 (이번 세션에서 미실시)

```sh
python -B -m workbench.session start af-res-067 --allow docs/workstreams/research/AF-RES-067/ --dependency work/research-af-res-063=8e348bb1306d5243b0a5ff8ebae773707d2dcfb4 --output docs/workstreams/research/AF-RES-067/manifest.json --fetch
python -B -m workbench.session check docs/workstreams/research/AF-RES-067/manifest.json --fetch
```
