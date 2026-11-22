# AF-RES-040 HANDOFF — REVIEW_READY_WITH_GAPS

**이번 시도는 원격 결과와 검사 기록을 남기고 종료한다. 완전 충족으로 승인하지 않는다.** 새 소비자 요구8건·24보기·직접 고유 원문64개를 비교했다. A/C는 풀에서 확인된 부분 근거8개를 보존하고 B는6개를 보존한다. 완전 적격 경로가 있는 요구는0/8이므로 완전 대안의 조건부 회수는 ‘해당 없음’이다. C가 A보다 우월하다는 결론이나 실제 사용자 효용은 입증하지 않았다.

## 1. 결과 SHA와 진입점

- 저장소·브랜치: `laadkke-arch/agentflow-open` / `work/research-af-res-040`.
- **최종 결과 묶음 SHA: `b99b5e2743e9cf0131a11d409707531f15a92f13`**. 이 SHA에서 RESULT와 최종 수용 파일을 직접 다시 열었고, 같은 SHA를 checkout한 뒤 지정 session check와 원장 검산을 통과했다.
- 분석 본문을 처음 고정한 커밋: `41f610d4a1700f339fc4a05c7625281e5f970bf3`. 최종 묶음의 RESULT blob은 그대로 `5f0697314e1560519b86e85a8ccaefe3b6e3eafe`다.
- 최종 수용 파일 blob: `06e5f9791ef16c2a365d8b36edbb1310dacde43d`. 수용 파일의 필수 조건은 **23/26 충족**, 남은 세 조건은 아래 §4에 명시했다.
- 이 HANDOFF는 위 검사가 끝난 뒤 **HANDOFF.md 하나만 추가하는 마지막 별도 커밋**으로 기록한다. 자신의 최종 commit SHA를 본문에 소급 삽입하지 않으며 실제 원격 commit metadata와 최종 응답이 그 SHA를 제공한다.
- 실제 배정/분기 SHA `de544231bc72fa6f2ddb3e91f9c0e8d16a0d1f62`, 계획 SHA `922bf3171cab62f30469720ac80327ad3f24fbf9`. 고정 선행003 `b13db3931b4021ff9e1ac6e404590c09526c3087`, 020 `856e6b40ae12d43197a6f02f7bf6ab7a7506fd35`를 읽었다.
- 제공된 확인 가능 모델 표시는 GPT-6 Astra Pro, 환경은 ChatGPT 공유 Linux·GitHub 연결이다. native web-pro 선택 UI와 실제 사람/독립 판독은 미확인이다.

| 먼저 볼 파일·위치 | 담긴 내용 |
| --- | --- |
| [RESULT 필수 표1](https://github.com/laadkke-arch/agentflow-open/blob/b99b5e2743e9cf0131a11d409707531f15a92f13/docs/workstreams/research/AF-RES-040/RESULT.md#L3-L14) — 3–14행 | 목적·판·후보 쌍·주소/상류/부품·역할·방향·직접 근거·미확인, 핵심10쌍 |
| [RESULT 필수 표2](https://github.com/laadkke-arch/agentflow-open/blob/b99b5e2743e9cf0131a11d409707531f15a92f13/docs/workstreams/research/AF-RES-040/RESULT.md#L16-L41) — 16–41행 | 8×3의 실제 대표 URL·보존/숨김·중복·귀환·분모·미확인 |
| [RESULT 전체](https://github.com/laadkke-arch/agentflow-open/blob/b99b5e2743e9cf0131a11d409707531f15a92f13/docs/workstreams/research/AF-RES-040/RESULT.md) / [SELF_CHECK](https://github.com/laadkke-arch/agentflow-open/blob/b99b5e2743e9cf0131a11d409707531f15a92f13/docs/workstreams/research/AF-RES-040/SELF_CHECK.md) | 8건 짝 집계가 먼저, 분야 간 비교·민감도·보관 대안이 뒤. Q1–Q7별 지지·반증·미확인 |
| [acceptance-evidence.json](https://github.com/laadkke-arch/agentflow-open/blob/b99b5e2743e9cf0131a11d409707531f15a92f13/docs/workstreams/research/AF-RES-040/evidence/acceptance-evidence.json) | 31조건의 mandatory/met, 파일·행, 분자/분모, 부족 이유·다음 행동 |
| [views.jsonl](https://github.com/laadkke-arch/agentflow-open/blob/b99b5e2743e9cf0131a11d409707531f15a92f13/docs/workstreams/research/AF-RES-040/views.jsonl) / [실제 카드24개](https://github.com/laadkke-arch/agentflow-open/blob/b99b5e2743e9cf0131a11d409707531f15a92f13/docs/workstreams/research/AF-RES-040/evidence/CARDS.md) | 표시 제목·설명·원링크·길이·숨은 멤버·잘린 그룹·빈칸 |
| [sources.jsonl](https://github.com/laadkke-arch/agentflow-open/blob/b99b5e2743e9cf0131a11d409707531f15a92f13/docs/workstreams/research/AF-RES-040/sources.jsonl) / [source-counts.json](https://github.com/laadkke-arch/agentflow-open/blob/b99b5e2743e9cf0131a11d409707531f15a92f13/docs/workstreams/research/AF-RES-040/evidence/source-counts.json) | 직접 열람 위치·사실·한계·중복·실패와 최종 고유 원문 수 |
| [losses.csv](https://github.com/laadkke-arch/agentflow-open/blob/b99b5e2743e9cf0131a11d409707531f15a92f13/docs/workstreams/research/AF-RES-040/losses.csv) / [relations.csv](https://github.com/laadkke-arch/agentflow-open/blob/b99b5e2743e9cf0131a11d409707531f15a92f13/docs/workstreams/research/AF-RES-040/relations.csv) | 기본24+민감도48행, 120후보쌍과 원 수동 방향 판정 |
| [RUNBOOK](https://github.com/laadkke-arch/agentflow-open/blob/b99b5e2743e9cf0131a11d409707531f15a92f13/docs/workstreams/research/AF-RES-040/evidence/RUNBOOK.md) | 미실행 제품 재현의 입력·명령·첫 자료와 원장 재검산 명령 |

## 2. 확인 범위와 핵심 관측

| 단위 | 최종 수와 범위 |
| --- | --- |
| 소비자 표집 | 두 원장 최초30씩, 총60노출. 각4·총8선정, 모두 특정 호출/규격/조건이 필요한 요청. 이름만 요청0 |
| 후보 풀 | 8×6=48슬롯, 실제39·빈9. 실제 후보 전부의 관련 절 직접 열람 |
| 후보 주소와 문서 | 고유 URL32, 판별 접근 키17, 그 키의 중복 제거 고유 원문15 |
| 전체 직접 원문 | **64개**: 소비자8·공급자22·배포/소스/동일성18·도서관5·음악11 |
| 출처 원장 | 176행, 중복·검색·노출·실패·범위 밖112행은 최소수에서 제외 |
| 관계·보기·손실 | 관계120행(실제 후보 수동85쌍·빈후보35쌍 unknown), 보기24, 손실72 |
| 요구 근거 | 필수 atom25, 풀에서 입증8·미입증17. A8/B6/C8 부분 atom 보존 |
| 완전 답변·조건부 회수 | 각 팔0/8. 적격 요구·경로 분모0이므로 조건부 완전 회수 ‘해당 없음’ |

B는 G2에서 MapInfo 대표 뒤의 **Java GetNextFeature 호출 근거**를, S1에서 gettext builder 대표 뒤의 **위치정보 config 문서**를 숨겼다. A–B 짝 비교는 A가 더 보존한 요구2·동률6이며, A–C는8건 모두 같은 atom 집합이다. B의 이질 병합48쌍을 해로운 오병합48건으로 세지 않았다. 실제 풀 내 필수 부분 근거 손실은2개/8개다.

반대 결과도 남겼다. G4의 HDF5 첫 원문 자체에 gdalinfo·크기·subdataset metadata 예제가 있으므로 B에서도 일반 호출 근거는 보존된다. G1도 HFA 첫 원문에 필요한 기능·설정3개가 함께 있다. 한 문서의 다른 앵커를 가렸다는 이유만으로 이미 열린 원문의 다른 절까지 가렸다고 세지 않았다.

기능·용도·판·역할 중복 슬롯은 각 팔0이며, 같은 고정 문서 반복 슬롯은 A7/B6/C7이다. 이는 다른 지표다. G2의 정확 URL 중복 제거로 새 참고 예제가 보이지만 Java 요구에 적격한 별도 대안이 되살아난 것은 아니다. 완전 적격 대안의 귀환은 모두0이다.

K에서 형제 목록만 열면 B의 근거6개는 그대로다. 모든 멤버 원문까지 읽을 수 있다고 가정한 **접근 상한**에서는 B가8개를 보존하지만 추가 원문11개 열람을 가정한다. 실제 총두클릭·채택 관측이 아니다. U의 미확인 동일성 후보0/39, Vg의 복수 후보판 요구0/8이므로 무변화는 안전성 증거가 아니다.

도서관의 Work/표현/판·소장 구분, MusicBrainz의 작품/녹음/발매와 실제 편집 사건, Cairo의 읽기/쓰기·PNG/PDF, libjpeg-turbo의 조건부 호환·역방향 예외, zlib-ng의 fork/compat/native 차이, GDAL COG/GTiff 호출·판 차이는 보조 원장에만 두었다. 주풀에 사후 삽입하지 않았다. 음향 동일성·무조건 구현 대체·전체 병합 복원 성공은 미확인이다.

## 3. 수행한 검사와 정정

### 최종 고정 SHA 재열람

`b99b5e2743e9cf0131a11d409707531f15a92f13`에서 두 파일을 다시 열어 로컬 고정 내용과 정확히 일치함을 확인했다.

| 파일 | 원격 blob | 줄 수 | 내용 일치 |
| --- | --- | --- | --- |
| RESULT.md | `5f0697314e1560519b86e85a8ccaefe3b6e3eafe` | 224 | true |
| evidence/acceptance-evidence.json | `06e5f9791ef16c2a365d8b36edbb1310dacde43d` | 1114 | true |

### 지정 세션 검사

아래 명령은 위 최종 결과 SHA에서 실제 실행했고 **종료 코드0**이었다. UTC 2026-11-22T19:23:00.816271+00:00, 사용자 시간대 Asia/Seoul로 2026-11-23 04:23경이다. 검사 중 원격 foundation 최신 SHA는 `a3e23f5264ba36d8e5513e620897f7af7434c387`였으나 task의 고정 scope base와 의존 SHA는 유지했고 계약 지문도 같았다.

```sh
python -B -m workbench.session check docs/workstreams/research/AF-RES-040/manifest.json --fetch
```

실제 출력의 핵심 필드만 옮긴다. 이 검사는 Git 계약·소유 경계 검사이며 제품이나 새 AI 세션 검증이 아니다.

```json
{
  "exit_code": 0,
  "status": "passed",
  "checked_at": "2026-11-22T19:23:00.816271+00:00",
  "checked_out_commit": "b99b5e2743e9cf0131a11d409707531f15a92f13",
  "freshness": "remote_checked",
  "integration_commit": "a3e23f5264ba36d8e5513e620897f7af7434c387",
  "scope_base_commit": "de544231bc72fa6f2ddb3e91f9c0e8d16a0d1f62",
  "contract_sha256": "19f08ce67f7b9d1914ccf214ac68112f3cefc68c95855c4aac0bbbd3393cd8bc",
  "changed_paths_count": 59,
  "outside_paths": [],
  "unmerged_paths": [],
  "errors": []
}
```

원장 검산 `python -B docs/workstreams/research/AF-RES-040/evidence/verify_delivery.py`도 같은 SHA에서 **23/23 통과·종료 코드0**이었다. 이 검산에 포함된 `recount.py --check-only`는 24보기·72손실·120관계 출력의 byte 일치를 확인했다. 여섯 봉인 입력 해시, 동일 원순서·3행 예산, 정확 대표 URL, 원멤버144관측의 복원, 관계85쌍 원 판정, 빈35쌍 unknown, 분모0 처리, 필수 표10/24행·마지막 약점3행, 허용 경로와 dot-control 불변을 대조했다.

[첫 결과 SHA의 전체 세션 영수증](https://github.com/laadkke-arch/agentflow-open/blob/b99b5e2743e9cf0131a11d409707531f15a92f13/docs/workstreams/research/AF-RES-040/evidence/verification-receipt.json), [원장 검사 영수증](https://github.com/laadkke-arch/agentflow-open/blob/b99b5e2743e9cf0131a11d409707531f15a92f13/docs/workstreams/research/AF-RES-040/evidence/delivery-validation.json), [처음 실패 기록](https://github.com/laadkke-arch/agentflow-open/blob/b99b5e2743e9cf0131a11d409707531f15a92f13/docs/workstreams/research/AF-RES-040/evidence/delivery-validation-first-failure.json), [실행 이력](https://github.com/laadkke-arch/agentflow-open/blob/b99b5e2743e9cf0131a11d409707531f15a92f13/docs/workstreams/research/AF-RES-040/evidence/execution-log.jsonl)을 남겼다. 재현 가능한 검사 성공으로 연구상의 세 미충족을 덮지 않았다.

정정은 [amendments M01–M09](https://github.com/laadkke-arch/agentflow-open/blob/b99b5e2743e9cf0131a11d409707531f15a92f13/docs/workstreams/research/AF-RES-040/evidence/amendments.jsonl)에 원 규칙·이유·달라지는 분모를 보존했다. G1 일반 gdaladdo의 HFA atom 과대 귀속을 제거했고, G4 HDF5 원문 안의 호출 예제를 반영했다. U/V의 혼합 처치, 자동 방향 추론, 보완 근거와 짝 집계, K 클릭 해석을 고쳤다. M08은 후속 명령별 문서 두 개를 통합 utilities 문서와 보수적으로 중복 제외한 **66→64 고유 원문 정정**이며 주결과 수치는 불변이다. M09는 S 최초 pool의 빈 의미 필드와 후속 coding을 같은 값으로 기대한 검사의 전제를 고쳤다. 원풀 행과 의미 판독 행을 ID로 따로 복원하며 실제 데이터는 바꾸지 않았다. 내부 검토는 사람·외부 독립·블라인드 판독이 아니다.

### 중간 원격 커밋

| 묶음 | 원격 SHA |
| --- | --- |
| ① 사전 표집·표시·판정 규칙과 manifest | `2ccbf7ab660d6e16dab637eea40867cbc4f83499` |
| ② 최초8요구·60노출·48슬롯 봉인 | `b406236564be8dc6435912912ba67e5d16c98102` |
| ③ 관계·24보기·손실·반례·내부 방법 검토 | `c65454136680986945206e21e04f6f6a6f906395` |
| ④ RESULT·자체 점검·수용·재집계 | `41f610d4a1700f339fc4a05c7625281e5f970bf3` |
| ④ 검사 영수증·최종 수용 상태 | `b99b5e2743e9cf0131a11d409707531f15a92f13` |
| 마지막 HANDOFF 단독 커밋 | 이 파일의 실제 Git commit metadata로 확인; 결과 SHA 위와 구별 |

## 4. 미충족과 미확인

**필수 수용 미충족3개**는 (1) 원 href 그대로의 완전한 전향 seed 순회, (2) 모든 방향 판정의 동일 범위·어휘, (3) 서로 다른 대표 설명의 실제 문자수 완전 일치다. S는 명명 항목에서 연구자가 만든 #L 링크이고 S1의 세부 순서는 사전 고정되지 않았다. G는 HFA 선열람·Java 역사판 역추적이 있었다. G의 문서 역할 치환과 S의 완전요구 대체는 방향 판정 범위가 다르므로 빈도를 합산하지 않았다. 설명은 동일80자 상한·동일 후보 문구이며 채워진 카드의 실제 길이는35–53자다.

완전 대안 분모0, 실제 사용자·독립 블라인드 판독·제품 실행·음원 비교·전체 원자료 병합 복원은 **효과 판정의 미관측 영역**이다. 단순 원장 검사의 실패와 구별한다. 최초 요구·풀을 본 뒤 새 성공 사례로 교체해 미충족을 숨기지 않았다. 이미 노출된 내용을 전향 관측 이전 상태로 되돌릴 수 없고 실제 재현 입력·역사판 실행 환경도 확보되지 않았으므로, 다음 조사는 별도 전향 반복 또는 입력 확보가 필요하다.

## 5. 실행하지 못한 검사: 명령·입력·첫 행동

자세한 입력·쉘 주의와 검증 범위는 [RUNBOOK](https://github.com/laadkke-arch/agentflow-open/blob/b99b5e2743e9cf0131a11d409707531f15a92f13/docs/workstreams/research/AF-RES-040/evidence/RUNBOOK.md)에 있다. 아래 값은 실제 확보가 필요한 입력이며 현재 latest나 임의 데이터로 대체하지 않는다.

| 대상 | 필요한 입력·환경 | 실행할 명령 또는 확보 후 호출 | 첫 행동·막힌 이유 |
| --- | --- | --- | --- |
| G1 | [저자 test_hfa_block_size.zip](https://github.com/OSGeo/gdal/files/4027388/test_hfa_block_size.zip), Windows10/Python3.7.2/GDAL3.0.1 | `python -m zipfile -l test_hfa_block_size.zip` 후 확인된 저자 스크립트 실행 | zip 멤버·스크립트명부터 확인. 아티팩트 성공은 미실행이다. |
| G2 | 원 MapInfo 입력·Java 전체 재현·native library/jar, GDAL2.4.0·3.0.1 | `java -Djava.library.path="$AF040_GDAL_NATIVE_DIR" -cp "$AF040_GDAL_JAR:$AF040_REPRO_CLASSES" "$AF040_REPRO_MAIN" "$AF040_MAPINFO_INPUT"` | [#2169](https://github.com/OSGeo/gdal/issues/2169)에서 입력·main 인자 계약부터 확보. 값이 없어 현재 완성 재현은 미확인. |
| G3 | 당시 dev SHA에 연결된 alpine-small **검증 digest** | `docker run --rm "$AF040_IMAGE_DIGEST" ogrinfo --version`; `docker run --rm "$AF040_IMAGE_DIGEST" ogrinfo --formats` | [고정 Dockerfile](https://github.com/OSGeo/gdal/blob/6d5d00851c24c25b4d814305cc5d4122ce72b4bc/gdal/docker/alpine-small/Dockerfile#L90-L119)과 당시 배포 digest 연결부터 확보. |
| G4 | 원 CSKS1_DGM_B_HI_24_HH_RA_SF_20091113111415_20091113111422.h5, Windows10/GDAL3.0.3/HDF5 1.10.4 | `gdalinfo --version`; `gdalinfo CSKS1_DGM_B_HI_24_HH_RA_SF_20091113111415_20091113111422.h5` | [#2193](https://github.com/OSGeo/gdal/issues/2193)의 원 파일·binary/dependency 출처 확인. |
| S1 | 원 source/conf.py, Windows의2.2.2·2.3.0·2.3.1 환경 | 각 환경의 `python -m sphinx -b gettext -d "$AF040_DOCTREES" "$AF040_S1_SOURCE" "$AF040_POT_OUT"` | [#7019](https://github.com/sphinx-doc/sphinx/issues/7019)의 source와 경로 조건 확보 후 POT 위치 주석 비교. |
| S2 | cad1f86 핀·원 이미지 확장·개별/전역 비교 입력 | `python -m sphinx -b html "$AF040_S2_SOURCE" "$AF040_HTML_OUT"` | [#7032](https://github.com/sphinx-doc/sphinx/issues/7032)의 원 extension과 두 이미지 동작을 확인. 전역 off만으로 성공 처리하지 않음. |
| S3 | doctree-resolved 확장·샘플 이미지·원 사용판 | `python -m sphinx -b html "$AF040_S3_SOURCE" "$AF040_HTML_OUT"`; `python -m sphinx -b latex "$AF040_S3_SOURCE" "$AF040_LATEX_OUT"` | [#7054](https://github.com/sphinx-doc/sphinx/issues/7054)의 이미지 등록·두 출력 파일/URI를 함께 확인. |
| S4 | 원 source·함수값 html_context·테마 aebde13·2.2.2/2.3.1 | 같은 outdir로 `python -m sphinx -b html "$AF040_S4_SOURCE" "$AF040_HTML_OUT"`를 두 번 실행 | [#7093](https://github.com/sphinx-doc/sphinx/issues/7093)의 함수값을 보존하고 둘째0 outdated인지 확인. |

분야 간 재개는 IJG v6b 원판과 libjpeg-turbo 소비자의 고정 호출/입력/빌드, MusicBrainz [edit115752742](https://musicbrainz.org/edit/115752742)의 old/new 및 후속 split 관계, 카탈로그가 같다고 연결한 두 track의 실제 동일성 근거가 먼저다. 원 입력이 없어 실행할 완전한 호환/음향 검사를 만들지 않았다. 타인에게 메시지를 보내거나 운영 카탈로그를 편집하지 않았다.

## 6. 색인용 한 줄과 재개 첫 자료

```text
AF-RES-040 | REVIEW_READY_WITH_GAPS | 새 요구8·24보기·고유원문64: A/C 부분근거8, B6; 완전 적격0/8·조건부회수 해당없음; 저장소 병합의 G2/S1 근거 손실과 G4 무손실 반례, 자연href/방향범위/실제문자수 미충족 | docs/workstreams/research/AF-RES-040/RESULT.md | 결과 b99b5e2743e9cf0131a11d409707531f15a92f13
```

재개자는 먼저 [G2 원 요청](https://github.com/OSGeo/gdal/issues/2169)과 고정 풀에서 빠진 G2.A3를 확인하고, [Sphinx v2.3.1 contents](https://github.com/sphinx-doc/sphinx/blob/v2.3.1/doc/contents.rst)의 raw href·순서를 새 관측 전에 봉인하는 계획을 작성한다. 기존8건·풀·정정 이력은 보존한다. 최종 설계 하나를 선택하거나 원자료 병합 비용을 추정하는 작업으로 확장하지 않는다.

## 7. 같은 우선순위의 약점 세 건과 다음 조사

| 중요한 불일치·약점 | 영향받는 결론 | 근거 URL·행 | 다음 최소 조사·첫 자료 | 결과가 바뀌는 조건 |
| --- | --- | --- | --- | --- |
| W1. 완전 적격 경로0/8, 이름만 요청0/8, U 후보0/39·Vg 노출0/8인 두 프로젝트 표본 | 적격 대안 귀환·C의 A 대비 우위·미확인/판 병합 안전성은 판정할 수 없다. 부분 근거2건 손실만 관측했다. | [G2 원 요청](https://github.com/OSGeo/gdal/issues/2169) Expected behavior; [S2 원 요청](https://github.com/sphinx-doc/sphinx/issues/7032) 개별/전역 구분; [losses.csv](losses.csv) strict·eligible_paths_n; [source-counts](evidence/source-counts.json) | 먼저 이 두 원 요청과 고정 풀의 부족 atom을 재확인하고, 별도 전향 등록 원장에서 실제 대안·판 차이·미확인 후보가 자연 노출되는 새 표본을 봉인한다. 기존8건을 교체하지 않는다. | 고정 원 풀에 모든 필수 atom을 입증하는 경로가 확인되거나 새 사전 표본에서 C가 A와 다른 적격 경로를 보존하면 효과 판정 범위가 달라진다. |
| W2. 자연 href·세부 seed 순서의 완전 전향 고정 미충족, 80자 상한만 동일, K는 원문 접근 상한 | 후보 순서가 완전히 자연스럽다는 주장과 엄격히 동일한 노출/두 클릭 비용의 인과 비교를 지지하지 못한다. | [Sphinx v2.3.1 contents](https://github.com/sphinx-doc/sphinx/blob/v2.3.1/doc/contents.rst) toctree; [S receipts](evidence/sphinx/receipts-S.json); [G notes](evidence/gdal/NOTES-G.md) §2; [views](views.jsonl) budget·description_length | 첫 자료인 contents와 GDAL formats_list의 raw href·목차 순서를 후보 본문 전에 봉인한다. 실제 같은 문자수 카드와 총 클릭 예산을 따로 사전 고정해 재구성한다. | 사전 등록된 raw href 순서와 엄격한 카드·클릭 조건에서도 G2/S1 손실이 반복되거나 반대로 사라지면 처치의 영향 판단이 바뀐다. |
| W3. 단일 내부 판독, G/S 방향 범위 비균질, 별도 구현의 무조건 대체·음향 동일성·병합 전체 복원 미확인 | 방향 대체율·실제 소비자 효용·보관만으로 오병합 복구가 충분하다는 일반 주장은 할 수 없다. | [libjpeg-turbo README](https://github.com/libjpeg-turbo/libjpeg-turbo/blob/af9c1c268520a29adf98cad5138dafe612b3d318/README.md) compatibility; [MusicBrainz edit115752742](https://musicbrainz.org/edit/115752742) 접근 미확인; [M07](evidence/amendments.jsonl) | 공통 목적·판·판정 범위로 핵심 G2/S1/G4 쌍을 독립 재판독한다. IJG v6b 원판·소비 호출을 먼저 확보하고 edit115752742 및 뒤따른 split의 old/new 관계를 다시 연다. | 독립 판독이 핵심 atom을 바꾸거나 제한 계약에서 완전 대체가 입증되거나 원 멤버/관계의 전체 복원이 확인되면 보존·호환·복원 결론을 수정한다. |
