# AF-RES-097 · 실행 전 범위와 판정

계획판 `fcde6becc49120c5be91adf43fb5b4aa42e71d48`, 시작 통합판 `01177554d0fbd33a914ea9c982c348d442d1358d`. 두 판의 변경 경로는 `docs/automation/dot-control.json`이고 AF-RES-097 배정은 시작판에서 읽었다. 시작 때 작업 브랜치의 원격 ref는 없었다. 처음 받은 checkout은 로컬 `work` ref와 이름이 충돌해 `git switch --create work/research-af-res-097 origin/chore/workspace-foundation` 종료 128이었다. 최신 통합 브랜치의 별도 전체 clone에서 같은 작업 브랜치를 만들고 정확한 계약 명령을 실행했다. [manifest](manifest.json)

계약의 AF-RES-093 원격 head와 인계 고정판은 모두 `ca82b938e429779d73d9de134ddac93e462ff03d`다. 인계에서 선행 결과 `4b1233ead75c0a701b497226b446794eedea3ceb`로 이어진다. 두 커밋 사이에 인계 파일만 추가됐다. 아래 blob이 연구 입력이다. 기존의 A/B 점수, 다른 사건, 사용자 시간은 이 실행의 분모 밖이다.

| AF-RES-093 입력 | 커밋 | Git blob |
| --- | --- | --- |
| [HANDOFF.md 및 새 이미지 예시](https://github.com/laadkke-arch/agentflow-open/blob/ca82b938e429779d73d9de134ddac93e462ff03d/docs/workstreams/research/AF-RES-093/HANDOFF.md) | `ca82b938…` | `83f93d02802b96a301417b432c3ee6ec3570d424` |
| [RESULT.md](https://github.com/laadkke-arch/agentflow-open/blob/4b1233ead75c0a701b497226b446794eedea3ceb/docs/workstreams/research/AF-RES-093/RESULT.md) | `4b1233ea…` | `e539957b104f8054f36b7fad2b1bb7bdf8075d0f` |
| [후보 정의](https://github.com/laadkke-arch/agentflow-open/blob/4b1233ead75c0a701b497226b446794eedea3ceb/docs/workstreams/research/AF-RES-093/evidence/pillow/candidates.json) | `4b1233ea…` | `0645c02d4e3f42e8f9634a96a1aaf05740f5394a` |
| [사후 원장](https://github.com/laadkke-arch/agentflow-open/blob/4b1233ead75c0a701b497226b446794eedea3ceb/docs/workstreams/research/AF-RES-093/evidence/pillow/post/truth.json) | `4b1233ea…` | `76cbcb67665940db7baa6c5158f436af824b47d6` |
| [선행 독립 판정](https://github.com/laadkke-arch/agentflow-open/blob/4b1233ead75c0a701b497226b446794eedea3ceb/docs/workstreams/research/AF-RES-093/evidence/adjudication/ADJUDICATION.md) | `4b1233ea…` | `5920b765140a72cd2c926718f14ee6490834de25` |

## 요구·입력·기대값

- **#5593.** 본문 assertion은 `RGBA` 모드를 요구한다. P·RGB 팔레트·투명 인덱스 `0`은 원 입력의 전제다. 변환에서 투명색 의미를 보존하는지 판별하려고 `RGBA` 및 네 채널, 사용 index 0의 alpha 0, 쓰인 불투명 index의 alpha 255를 검사한다. RGB 위치별 수치와 전체 RGB 일치는 연구자의 진단이다. 작성자는 좌표 및 RGB 수치를 별도 요구하지 않았다. 좌표는 변환 출력을 보기 전에 원 PNG 필터를 풀고 행 우선으로 선정했다. index 0 `(29,24)`, 처음 등장한 불투명 index 2 `(0,0)`, 같은 RGB를 가진 불투명 index 1 추가 검사 `(75,53)`. 원본 색은 순서대로 검정·흰색·검정이다. 원 입력은 [작성자 Gist 및 고정 ZIP](https://codeload.github.com/gist/d98a4b54fb409bc8f745d169df0196fc/zip/7389968dec0ac74f493d28ccd0f5f7b00e7ca8de). [원 요구](https://github.com/python-pillow/Pillow/issues/5593#issue-939528731)
- **#5595.** 요청의 배열 `p=[0,0,0,255,0,0,0,255,0]`를 `Image.new('P',(100,100),1)`에 붙인 직후 `getpalette()[:len(p)] == p`가 목표다. 작성자는 새 RGBRGB 순서를 선호했고 빨간 화면을 예로 들었다. `(0,0)` index 1과 RGB `(255,0,0)`은 그 화면 설명을 점검하는 부가 관측이다. 특정 좌표나 PNG 재열기는 본문의 필수조건에 없다. 픽셀 전부가 1이라는 입력을 각 실행에서 만든다. [원 요구](https://github.com/python-pillow/Pillow/issues/5595#issue-940162920) [후속 수용](https://github.com/python-pillow/Pillow/issues/5595#issuecomment-877853085)
- **판별 사전 가설.** #5593에서 8.2.0 기본/명시 모두 `RGBA`, alpha `[0,255,255]`를 예상한다. 8.3.0·8.3.1 기본 `RGB`, alpha 채널 부재, RGB 색 키 `(0,0,0)`를 예상하고 명시 `RGBA`는 세 판에서 원 인덱스별 alpha를 보존한다고 예상한다. #5595 8.2.0 객체 경로의 예상은 `[0,255,0,0,0,255,0,0,0]`, index 1, 파랑 `(0,0,255)`다. 8.2.0 raw 및 8.3.x 양 경로는 원 p, index 1, 빨강이 예상된다. 역사 이슈·선행 자료·코드로 세운 가설이다. 새 연구 실행은 이 봉인 이후 시작한다. [기본 변환 수정](https://github.com/python-pillow/Pillow/pull/5594) [당시 순차 실행](https://github.com/python-pillow/Pillow/issues/5595#issuecomment-877558030)
- **대조 예상.** 쓰인 투명 index가 있는 작은 PNG의 작성·재열기에서 P/원 인덱스 및 tRNS를 확인한다. 투명 정보 없는 대조에서 기본 `RGB`와 명시 `RGBA`의 RGB는 같고 RGBA의 alpha는 `[255]`만 있다. tRNS가 있으나 index 0을 사용하지 않은 대조는 RGB가 동일하며 명시 alpha가 전부 255다. 기본은 8.2.0에서 `RGBA`, 8.3.x에서 `RGB`를 예상한다. 중복 RGB 대조 A/B는 1·2의 순번만 바꾼다. 픽셀 RGB와 PLTE가 같아도 index 1 집합이 다르고, 같은 A의 두 호출은 모드가 달라도 RGB가 같다. `(1,2)`의 번호가 P 상태에서 정의된다. RGB(A) 출력에 역추정한 index는 미정의다. 두 팔레트 경로에 RGB 입력을 고의로 주면 동일한 실패로 예상한다. #5593의 RGB 결과를 `convert('RGBA')`로 다시 승격하는 대조에서 검정 색 키가 불투명 index 1의 검정에도 적용되리라 예상한다.

## 순서와 채점

1. [inputs.json](inputs.json)의 바이트/정의 지문, 좌표, 24자리 [초기 원장](runs.jsonl)을 커밋한다.
2. 세 판의 격리 실행체를 준비해 소형 P PNG의 저장·재열기 교정을 실행한다. 패키지·코어 경로 및 결과를 등록한다.
3. 사건 → 8.2.0/8.3.0/8.3.1 → 기본/명시 또는 객체/raw → 반복 1·2 순으로 실행한다. 새 child마다 원 PNG를 새 `BytesIO`에서 연다. PyPI 빌드의 로딩과 예상 출력의 검사를 분리한다. #5595는 새 리스트와 새 P 이미지를 매번 할당한다. 같은 객체 순차·저장·재열기·구성 대조는 각자 별도 행으로 둔다.
4. 출력을 얻은 두 반복은 PID·시각·경로 같은 실행 식별자를 빼고 값으로 대조한다. #5593은 두 후보 모두 원 PNG에서 두 번 출력 관측 및 반복 일치가 있는 판만 채점한다. #5595는 저장 전 동일 기준의 fresh 결과를 사용한다. 적합성 함수는 `#5593 = mode RGBA ∧ 4 bands ∧ alpha(index0)=0 ∧ alpha(index1,index2)=255`, `#5595 = palette_prefix == p`이다. #5593의 원 RGB 또는 #5595의 index/RGB 차이는 별도 관측으로 표에 표시한다. alpha의 `null`은 채널 부재이고 255는 있는 채널의 불투명 값이다.
5. 같은 목적을 양쪽이 충족하면 **양쪽 일치**, 하나가 충족하면 **한쪽만 충족**, 양쪽이 관측되고 둘 다 요구를 어기면 **양쪽 미충족**이다. 잘못된 입력처럼 양쪽의 호출 오류를 확인한 경우에는 실패 단계와 함께 양쪽 미충족으로 둔다. 입력 결손·환경 준비 실패·출력 관측 불능·미확인 반복은 **미확인**이며 특히 #5593의 원 PNG 양호출 출력 요건을 완화하지 않는다. PNG 대조의 무투명 목적은 채널 무시 RGB 또는 완전 불투명 등 목적 정의를 각 행에 표시한다.
