# 반례·결손·정정 (4차)
 
## 정정 이력
- R02, 3차 e7a0ce3b664d225d59ec94750d391219fa105dca: D02의 2013 Nature 유사 안내 및 별칭 추가 회신을 기록하되 현 부모 확인 보류. X09 L2,5–8 실제 링크는 nature-brackets, X10 L158–167은 대괄호 layout. A03 L161–188의 superscript와 다르다. 첫 링크를 X09→X10으로 정정. 과거 요청/응답을 삭제하지 않으며 단지 현재 링크 판정 근거를 바꾼다.
- R03: exact root/dependent 두 경로 404(F05,F06). generic Nature 추천은 2023 답변이지 고정 XML로 확인한 동일 스타일이 아니다. 정확 주소 추천 보류(다른 파일명 가능).
- R04: X11로 Nature Communications 현재 parent A03을 확인. 2022 D04→D07→X05 직접 연결; 2026의 A03과 같은 내용이라고 주장하지 않는다. A03 현재 preprint term과 merge 당시 article term 구별. 
- 프레임의 12 목적 자리는 24 소비자 정적 행 확인으로 actual 표기를 수정; 0 renderer runs 유지. E05 원문을 열어 WP classic 반례 한 개를 추가. A–E 핵심 원자료 산입 39, X09–18 보강 10은 보수적으로 비산입, F04–07 실패도 비산입.

## 반증 묶음
1. **같은 부모라도 언어 다름**: X12·X13의 동일 href + fr-FR/en-US, X14 parent의 and=text/accessed; A05/A07에서 and=and/et. 두 이름이 있는 입력에서 해당 분기가 실제 선택되면 다르게 나올 것으로 예상. Zotero C03은 자식 default-locale 강제, Pandoc C12는 명시 lang 우선 가능. 별칭 이름/parent만으로 출력 동일 단정 금지. 반대로 두 Nature alias는 en-GB 동일하고 A03의 and=symbol, et-al 및 일부 날짜 연도만 출력하는 분기는 달라지지 않을 수 있다. 둘 다 locale 파일 차이만으로 항상 차이가 난다고 하지 않는다. X15–17은 이탈리아어 부모 default와 EN/FR 자식 override가 있는 두 번째 사례.
2. **같은 표시 결과≠같은 입력**: X18의 MEDLINE mapping 2776 입력 key/63 중복 출력 그룹; BMJ, Acta Crystallogr. A. 실제 journal identity 합병은 금지; item title, ISSN, abbreviation source 및 UI option으로 확인. C15/D06의 Journal Abbr 누락 또는 plugin/copy 차이를 분리. APA A04 fr editor plural override와 A07 plural éd. 차이도 'locale 파일만 받으면 해결' 가설을 깨뜨린다.
3. **공유 수정의 파급**: D04 원요구→D07 merged PR→X05 body; X11과 A01/A02가 A03을 실제로 가리킨다. 소비자에서 새 parent를 고르게 되면 sibling에도 영향을 줄 수 있다. 별도 사본은 format 변경 범위를 축소하나 upstream update를 놓칠 수 있다. 사용자의 installed version/cache가 구판이면 당장 바뀌지 않을 수 있다. 승인 근거가 없다면 범위 격리를 우선 권고.
4. **자식 override를 다른 상속 도메인으로 일반화 금지**: E02 Template=twentytwentyfour, E03 parts/header.html child body와 E04 parent body의 navigation wrapper 차이(부모 L18–22에는 wrapper, child에는 없음). E01 공식 규칙은 같은 이름 template/part child override; classic E05 L90–95는 더 구체적인 parent가 일반 child보다 앞서기도 한다. functions.php는 두 파일 load; 스타일 CSS 별도 load. CSL dependent는 B02의 info-only라 child body override 허용 안 됨. WordPress 파일 배치만 보고 실제 database-customized template 선택까지 확정하지 않는다.
5. **오프라인의 실제 반례 후보**: Pandoc C08 로컬 basename 선택을 잘못된 nature.csl 파일로 충족하면 요청한 고정 부모와 다를 수 있다; 없으면 remote fetch. Zotero C03 설치 시 GET hidden parent vs 설치된 조회, C04 built-in resource/캐시. 같은 locale 확장자라도 공급 경로 다름. X01/X02와 X06–08의 버전 대조는 파일/번들 관찰이지 사용자 실행 증거 아님.
6. **저널 권위·자료 결손**: F01/F07의 공식 지침 본문 접근 실패; 검색 요약은 결론 근거로 사용하지 않음. 정확 두 대상 저널의 저자 요청/승인은 아직 직접 확보 못함. NBT/Nano가 Nature parent에 종속된다는 사실과 출판사가 현재 그 결과를 승인한다는 사실을 구분. 다음 조사에서는 정확 저널의 editor instructions 또는 author proof, item export, issue patch 연결부터 확인.

## 판정이 바뀌는 경쟁 설명
- 동일 스타일이어도 item type=article vs journal article, genre/DOI/URL/volume/page 결손 때문에 preprint 결과가 달라진다면 첫 링크는 parent edit 대신 item data/field mapping 설명이다(D04, A03). 
- 사용자에게 이미 설치된 parent+locale이 있다면 새 다운로드는 조건부 설명으로 내린다. 고정판이 아니라 다른 parent를 실제 load한다면 다운로드 링크를 exact parent 및 resolution path 확인으로 교체.
- 언어 변경이 학술지 규정 위반이면 FR 출력 방법은 테스트/사적 사용 전용으로 내리고 저널 정식 링크와 구별.
- WordPress child override는 실제 파일 위치와 template specificity가 맞을 때에만 적용. CSL의 metadata alias를 theme child와 같은 override 권한으로 추론하지 않음.
