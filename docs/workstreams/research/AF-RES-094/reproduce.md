# AF-RES-094 재현

## 접근 수단과 사전 점검

사전 점검은 pip 프로젝트 페이지, octocat Hello-World README의 blob과 미존재 파일, IANA 공개 도메인 예약 설명을 사용했다. 주 경로 주소는 이 단계에서 요청하지 않았다. [사전 증거](evidence/preflight/)

| 확인 | 브라우저 | GET | 증거 |
|---|---|---|---|
| Chromium 기본 신뢰 | pip·공개 GitHub에서 TLS 신뢰 오류, IANA에서 터널 실패 | pip 200, 두 GitHub 주소 503, IANA CONNECT 403 | [첫 회차](evidence/preflight/chromium-default-trust/run.json) |
| 격리 신뢰 설정 후 실행 준비 | 로컬 카드에 쓴 data: 탐색이 관리 정책에서 거부됨. 외부 탐색 발행 전 오류 | pip 200, GitHub README 200/미존재 404, IANA CONNECT 403 | [로컬 카드 시험](evidence/preflight/local-card-scheme/routes-observed.json) |
| 최종 수집 방식 | pip 200, README 200, 미존재 404, IANA 터널 실패 | pip 200, README 200, 미존재 404, IANA CONNECT 403 | [정상·오류 대조](evidence/preflight/confirmed/routes-observed.json) |

관리형 Chrome CUA는 pip 대조 탭 생성 때 `Browser Use could not read requirements`를 반환했다. 별도 Firefox ESR 153.5.1/geckodriver 0.36 시도는 약 18:05 UTC에 실행기 시작에서 타임아웃했고, 로컬 about:blank 화면 시험은 읽기 전용 UID map 오류를 남겼다. 두 시도 모두 주 주소를 열지 않았다. 최종 브라우저는 Debian Chromium 156.0.8078.79 + Playwright와 TLS 검증을 사용한다. 기본 Chromium과 curl이 사용하는 CA 저장소 차이는 해당 프로세스가 보는 격리 NSS 사본에 환경 CA를 넣어 해결했다. 프록시와 허용 정책은 적용된 상태다. 200→404 전환은 사전 회차 시간 차가 포함된 별개 관측이다.

## 순서와 출력

다음은 저장소 루트의 명령이다. 출력 디렉터리와 본문 캐시를 회차마다 새 이름으로 만든다. Chromium에 프록시 CA가 적절히 설치된 환경에서는 기본 실행 파일을 사용한다. `AF_PLAYWRIGHT`는 설치된 Playwright 모듈 경로다. 같은 세션의 네트워크 설정을 살핀 뒤 실제 브라우저와 GET이 같은 허용 정책을 사용하는지 사전 대조한다.

```sh
af_root=docs/workstreams/research/AF-RES-094
AF_PLAYWRIGHT=/opt/codex/runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright \
  node "$af_root/tools/collect.cjs" preflight "$af_root/evidence/preflight/new-UTC" /tmp/af094-preflight-new-UTC
AF_PLAYWRIGHT=/opt/codex/runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright \
  node "$af_root/tools/collect.cjs" main "$af_root/evidence/main-new-UTC" /tmp/af094-main-new-UTC
```

이 환경과 같은 NSS 보정이 필요하면 시스템 CA 파일의 출처를 확인하고 격리 경로를 사용한다. 이 회차의 `AF_CHROMIUM`은 PRoot 5.1.0-1.3+b1의 실행 래퍼였다. 아래 지정 패키지는 Debian 공개 배포물이다. PRoot의 바인드는 NSS 저장소 경로 한 곳에 적용된다. Chrome 정책, TLS 검증 및 외부 호스트의 접근 기준은 계속 적용된다. [Chromium Linux 인증서 문서](https://chromium.googlesource.com/chromium/src/+/main/docs/linux/cert_management.md)

```sh
af_trust=$(mktemp -d /tmp/af094-trust.XXXXXX)
mkdir "$af_trust/nss"
curl --disable -fLSs -o "$af_trust/proot.deb" https://deb.debian.org/debian/pool/main/p/proot/proot_5.1.0-1.3+b1_amd64.deb
curl --disable -fLSs -o "$af_trust/libtalloc.deb" https://deb.debian.org/debian/pool/main/t/talloc/libtalloc2_2.4.0-f2_amd64.deb
dpkg-deb -x "$af_trust/proot.deb" "$af_trust"
dpkg-deb -x "$af_trust/libtalloc.deb" "$af_trust"
certutil -N -d "sql:$af_trust/nss" --empty-password
certutil -A -d "sql:$af_trust/nss" -n 'managed HTTPS proxy root' \
  -i /usr/local/share/ca-certificates/environment-proxy-ca.crt -t 'C,,'
cat > "$af_trust/chromium-test" <<'SH'
#!/bin/sh
af_dir=$(dirname "$0")
exec /lib64/ld-linux-x86-64.so.2 --library-path "$af_dir/usr/lib/x86_64-linux-gnu" "$af_dir/usr/bin/proot" \
  -b "$af_dir/nss:$HOME/.pki/nssdb" /usr/bin/chromium "$@"
SH
chmod u+x "$af_trust/chromium-test"
export AF_CHROMIUM="$af_trust/chromium-test"
```

각 카드에 새 비로그인 browser context를 사용하고 CDP cache를 끈다. 첫·추가 링크를 오프라인 카드에서 실제 클릭한다. 문자 주소 탐색은 `verbatim_visible_uri_navigation`이고, 문서의 anchor 클릭은 `document_link_click`이다. HTTP는 독립 curl 8.14.1 프로세스로 GET을 수행한다. `--disable`로 기본 설정을 읽지 않고 쿠키 기능은 켜지 않는다. 본문 지문은 압축을 푼 응답 bytes 기준이다. MIME과 wrapper 지문은 그대로 기록하고 GitHub JSON이 담은 복원 파일 지문은 별도 열이다. 줄 끝 LF가 없는 `rawLines`의 결합본은 LF 하나를 붙인 후보 지문도 기록한다. 사전 README의 양쪽 복원 후보는 별도 원 응답으로 다시 검산했다. [파서 검산](evidence/preflight/wrapper-offline-parse.json)

주 실험은 목적별 교차한 카드 순서와 각 카드의 병행 브라우저/GET을 사용한다. 같은 문서 anchor, 자동 redirect, 메뉴 펼침, 하위요청은 별도 계수한다. 결과 비교는 새 회차의 원장에 기록하며 기존 회차의 판정은 보존한다. 저장소에는 시각·상태·응답 SHA·실제 화면·판별 발췌·안전한 응답 헤더를 저장한다. 임시 원바이트와 헤더에는 브라우저/서비스 내부 토큰이 있을 수 있으므로 전체 덤프와 쿠키는 공유 대상에서 제외한다.

선행과 같은 결과판 검사 명령은 아래와 같다.

```sh
python -B -m workbench.session check "$af_root/manifest.json" --fetch
python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean
python -B scripts/check.py --require-git
```
