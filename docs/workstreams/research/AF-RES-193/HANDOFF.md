# AF-RES-193 HANDOFF

- **작업자 판정: PARTIAL.** 정적 관계/호출·목적 분기와 당사자 관측 다음 단계 결측 확인은 충족. 엄격 BTS 표집 기준 미달. 자체점검 수행, 독립 검토 없음. 중앙 진행표 수정하지 않음.
- 착수 integration SHA 72cf39aea54e2de2ba78a245593aefdc40205a16; 계획 0f6765df46ad2128c7fdfa92c3bf917bbfe0c5e6; 선행 AF-RES-185 고정 인계 6581ffcae5a6d902c469e8275e6e6b2a70de2cc5. 차이와 blob 조회 내역 SCOPE.
- **결과 및 자체점검 고정 SHA (이 인계 직전): 8a52106de2dee1c5c07d7cfab5d0664667a8908b.** 이 SHA에서 RESULT, SELF_CHECK, sources, frame 본문·blob SHA를 다시 확인. RESULT 최초 커밋 5faa0055888e10c2b3b744668e78519b0ef92dd3. HANDOFF 자신의 SHA는 branch head에서 확인한다.
- 대표 파일: [RESULT.md](RESULT.md) 세 표→Q1–Q7→약점 3건; [SELF_CHECK.md](SELF_CHECK.md), [sources.jsonl](sources.jsonl), [frame.csv](frame.csv), [relations.csv](relations.csv), [events.csv](events.csv), [choices.csv](choices.csv), [SCOPE.md](SCOPE.md).
- 범위: bsd-mailx Depends OR; cron Recommends OR; 두 제공자 mail-transport-agent 충족 가능, Conflicts로 정상 동시 설치 불가. 같은 sendmail 진입점/파일 목록은 목적 대체 보증이 아니다. Exim local/smarthost+mail_spool 조건부 local mbox; satellite no local, local-only remote reject. Nullmailer relay-only, adminaddr recipient remap, allmailfrom envelope override; exit 0 queue ≠ remote receipt. cron MAILTO='' / no output no mail; missing MTA discards output. C01/C02 local reading/display reports, C06 local delivery/routing report; downstream final receipt 미확인. 기존 mbox 읽기와 새 배달 분리. 같은 relay/acceptance 목적은 두 후보 조건부 OR. 사용자 한 질문: 알림을 같은 호스트 mbox에서 읽나요, 외부 메일함/릴레이로 보내나요, 아니면 필요 없나요?
- 수량: 원장 46행, 직접 읽은 41행/고유 work_id 40, 보수적 산입 33(A6/B12/C8/D3/E4), 계보 8; C8은 편의 대조로만 사용, 엄격 유효 25(A6/B12/C0/D3/E4). C 최소 4건 부족, 4×2 예정 8자리 미확정. 실제 사건 8, runtime exact pair 최종 수신 관측 0 확보(부재 자체 미증명). 기관 자료 4는 서비스 조건, 개별 인수 사례 0. frame 54 data rows; 관계 4+2 대조, events 4 static+8 report, choices 3+2 대조. URL 누락 0. 5 접근 실패/불완전, 8 직접 보조 대조 최소치 제외.
- 약점 3: (1) archive all BTS first-two frame, (2) exact runtime/config/receipt 및 cached Exim man/cron compiled path, (3) 기관 개별 인수 관측 부족. 부재를 실패·성공률로 바꾸지 않음. 최초 표집 순서 검증 불가라는 이유로 완료 승격 금지. 독립 검토자에게 원장과 모집 재검증 요청.
- 변경은 owned_path 한정. 새 Debian build, install, daemon, mail send, 네트워크/메일 서버 실행 없음. 실제 설치/발송 검증은 이번 범위 밖, 후속 별도 승인 없이는 실행하지 말 것.

## 첫 재개 행동 — 결과를 보지 않고 BTS 전체 번호 프레임부터 복구

Codex Cloud scratch에서 공개 index 읽기만 시도한다(아래 명령 미실행). Web 도구에서 archive=both 조회 실패했으므로 일반 브라우저/HTTP read-only 재조회. source/binary 이관을 구별하고 exim4-daemon-light 별도 package 목록 및 mailx 과거 이관을 포함할지 scope와 함께 기록. archive=both 지원 여부/응답 본문 제목을 먼저 확인; active-only 결과로 순서 확정 금지. 2025-12-31 inclusive는 원 접수일 기준, 이후 댓글은 cutoff 밖 표시. 결과 유무와 관계없이 최초 적격 두 사건만 채택, 병합 ID는 동일 사건. 이미 본 C01–08 때문에 검토자에게 outcomes 가리지 못했다는 노출 이력 남기고 가능하면 독립 선별.

```sh
set -eu
mkdir -p /tmp/af193-bts
cd /tmp/af193-bts
for p in bsd-mailx cron exim4 exim4-daemon-light nullmailer mailx; do
  curl -fSLG --data-urlencode "pkg=$p" --data-urlencode "archive=both" \
    'https://bugs.debian.org/cgi-bin/pkgreport.cgi' -o "$p.html"
  sha256sum "$p.html"
done
# 수집 HTML이 실제 archive 포함 결과인지 확인 후 bug 번호 후보만 추출.
python - <<'PY'
from pathlib import Path
import re
for p in sorted(Path('.').glob('*.html')):
    s = p.read_text(errors='replace')
    nums = sorted({int(x) for x in re.findall(r'bugreport\.cgi\?bug=(\d+)', s)})
    print(p.name, len(nums), nums)
PY
# 실제 추출 번호를 한 건씩 원문에서 screening, original package/date/title/request 의미 기록.
# 예: 기존 편의 대조 697612 재확인 (이 번호 자체를 최초 표본으로 지정하지 않음)
curl -fSLG --data-urlencode 'bug=697612' \
 'https://bugs.debian.org/cgi-bin/bugreport.cgi' -o case-697612.html
```

위 정규식은 후보 추출일 뿐 완전성을 보증하지 않는다. links escaping/페이지 구분 또는 package reassignment 발견 시 원 목록과 대조. access failure 계속되면 공식 Debbugs SOAP 또는 archive index 안내를 직접 읽고 공개 읽기 경로만 사용. 프레임 전체를 고정한 후 각 package 첫 2를 오름차순으로 선별, 8개 슬롯을 frame.csv에서 판정, 최소 strict C4. 기존 8은 대조로 유지 또는 해당 순번 확인 때만 승격. 각 원제보/작성자 후속, 상태 변경 vs final delivery, 실제 actor/readout 구분. 결과 없거나 부족해도 임의 현대판 교체 금지.

## 추가 정적 판독 — exact binary와 man

Debian trixie amd64 package 파일만 별도 scratch에서 가져와 읽는 재검사 예시(미실행, apt download만; 설치/재빌드/서버/실제 mail 금지). 환경 apt metadata가 정확 버전을 제공할 때만; 이전 판이면 Debian snapshot에서 동일 판 archive URL을 직접 확인한 뒤 읽고 hash 기록, 최신 임의 대체 금지. 이 작업은 필요 시 후속 Codex Cloud에 전달.

```sh
set -eu
mkdir -p /tmp/af193-debs
cd /tmp/af193-debs
apt-cache policy bsd-mailx cron exim4-daemon-light nullmailer exim4-config
apt-get download 'bsd-mailx=8.1.2-0.20220412cvs-1.1' \
 'cron=3.0pl1-197' 'exim4-daemon-light=4.98.2-1+deb13u5' \
 'exim4-config=4.98.2-1+deb13u5' 'nullmailer=1:2.2+10~g7ed88a0-6.1'
for f in ./*.deb; do
  sha256sum "$f"
  dpkg-deb -f "$f" Package Version Architecture Depends Pre-Depends Recommends Provides Conflicts Replaces
  dpkg-deb -c "$f" | grep -E 'sendmail|cron$|mail\.1|README\.Debian|update-exim4' || true
  out="./extracted/$(dpkg-deb -f "$f" Package)"
  mkdir -p "$out"
  dpkg-deb -x "$f" "$out"
done
# 파일 존재/링크 target과 man source version/flags만 확인; binary 실행하지 않는다.
find ./extracted -iname '*sendmail*' -o -iname '*exim4.8*'
find ./extracted -type f -name 'cron' -exec strings '{}' \; | grep -E '/usr/(lib|sbin)/sendmail' || true
```

strings는 가능한 후보 문자열에 불과하고 실제 호출 위치를 보증하지 않는다. 정확한 binary/disassembly 또는 public package build log로 macro/path를 연결. Exim u5 man 압축 원본을 읽고 B13 구판과 비교, 옵션 대조가 바뀌면 원장/결과 보정 커밋. 네 package source 및 control URL은 relations/sources에 고정. 실제 queue/relay/recipient observation은 공개 기존 당사자 로그로만 확인; 동일 message ID/환경/구성을 연결하지 못하면 HOLD. 기관 자료는 공개 개별 ILL 대출/USPS 위탁 인도 사례가 발견될 때에만 실제 사건으로 추가한다. 다른 작업자의 후속 실행에 의존하지 않음.

## 색인 제안 (한 줄)
AF-RES-193 — PARTIAL: Debian bsd-mailx Depends/cron Recommends OR vs Exim light·nullmailer local/relay 목적 분리; 4/4 static pairs, 33 conservative direct sources(엄격25), 8 convenience BTS reports/strict0, no exact recipient proof; RESULT/SELF_CHECK/HANDOFF; first-two BTS archive frame 재구성.
