# 경쟁 설명·반례·타 분야 보정 (④)

## 원래 가설과 뒤집는 증거
- 가설 G1: "copy=False 오류라면 asarray로 교체하면 된다." **부분 채택**. N05 migration의 대부분 사례 및 F02는 값 생성 목적에 적합. 반례 N03/N04의 엄격 no-copy 계약: 리스트나 dtype/order 변경이 필요하면 False는 ValueError, None은 허용한다. 같은 값 반환은 원본 버퍼 공유를 보장하지 않는다. F03에서는 dtype/object/temporal 유지 기대만 있고 사용자 쓰기 요구가 없다. F01의 Arrow zero_copy_only가 upstream에서 성립해도 ChunkedArray의 list materialization 후 외부 ndarray는 같은 원버퍼라고 할 수 없다. 원래 제보에 없던 ndarray input을 대신 사용하지 않는다.
- 가설 G2: "Astropy #16181이 shim을 없앴으므로 copy=False가 언제나 end-to-end 무복사를 뜻한다." **기각**. F08 constructor의 Quantity unit mismatch는 .to(unit)로 바꾼 후 COPY_IF_NEEDED를 재설정; F09 q4 fixture는 copy=False에도 q0과 다른 object 및 base를 기대한다. F08의 비Quantity 정수 ndarray→기본 float astype도 별도 allocation 가능. 반대로 F09 q1 float arange 같은 단위는 base is a 기대, q2/q3 동일 객체 기대. 이것은 새 실측이 아니라 원문 코드 및 assert. 명시 False의 strict는 적어도 np.array 호출에서 강해졌지만 모든 분기·전체 연산에는 보장 불가. D09 release note의 기본값 설명을 Quantity 전체에 적용하지 않음: Quantity.__new__ copy=True 기본 유지(F08).
- 가설 G3: "PR merge가 오류 해결을 증명하고 같은 오류 재제보는 회귀다." **기각**. D01-D04의 2.20.0 release(06-13)는 merge(06-19) 전; 포럼 06-23 old line, 06-24 예정, 실제 확인 안정판 2.21.0(08-14). 정확 설치판 미확인. H02 12월의 3.2.0/NumPy2.2.1은 fasttext model.predict(text,1) 맥락이고 동일 stack 미확인, 따라서 동일 호출 회귀라고 하면 오류. A tag도 D05-D10에서 코드·release listing 확인하되 user deployment/retest 미확인.
- 가설 G4: "copy를 새 기본값으로 두기만 하면 된다." **조건부**. NumPy asarray의 기본은 필요시 copy; 2.0 array의 default True 및 Quantity default True는 다른 계약. Astropy의 이전 False default signature만 version-dependent None으로 변화(D09,A03), 외부에서 내부 constant를 import하도록 권하지 않는다(F10). 기존 dtype/subok/ndmin/units 요구가 유지되는지 검증해야 한다.
- 가설 G5: "공유와 쓰기 전파는 같은 속성이다." **기각**. N04 doc example shares_memory=True만 확인. X03 shared mapping도 PROT_WRITE 권한 별도이며 private mapping은 최초 내용 공유 가능해도 변경 미전파; X04 READ는 쓰기 불가. N03 object copy=True도 shallow element reference이므로 외부 버퍼 분리와 객체 변경 격리가 다르다. 테스트는 실제 쓰기/권한/원본 값 관측을 따로 저장해야 함.

## 분야 대조 (Q6)
| 원문/위치 | 요구 | 정책 | 넘길 수 있는 속성 | 넘기면 안 되는 주장 |
|---|---|---|---|---|
| [NARA film digitization](https://www.archives.gov/preservation/formats/motion-picture-film-playback-digitize.html), preservation/access | 원본 손상 방지·접근 | 고품질 preservation vs 낮은 bitrate access; 보존 원본 유지 | 원본 identity, 파생 사용 목적, 변환 허용, 저장비용 | 압축 access copy가 원본과 동일·수정 전파 |
| [LOC guidance](https://www.loc.gov/preservation/resources/rt/guide/guid_asp.html), preservation/access | 접근 대역폭과 원본 정보 | derivative 최적화; watermark/paper 등 원본 보관, 흐린 글씨의 microfilm 손실 | 보존 속성별 대조; 역변환/품질 손실 명시 | 배열의 buffer alias 직접 증거 |
| [Linux mmap](https://man7.org/linux/man-pages/man2/mmap.2.html), flags/protection | 공유/개인 변경 | MAP_SHARED vs MAP_PRIVATE, PROT_WRITE, msync | 초기 값·memory identity·권한·변경 가시성·지속성 독립 | 모든 shared mapping이 writable, 즉시 disk 반영 |
| [Microsoft MapViewOfFile](https://learn.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-mapviewoffile), dwDesiredAccess | 공유/읽기전용/개인 | FILE_MAP_READ/WRITE/COPY; COW private page, commit charge | lazy materialization과 수정 전파 분리, read-only 거부 | NumPy가 같은 COW semantics 제공 |

보존기관 사례의 재사용은 '원본/파생' role이 목적별로 다르다는 점이다. mmap의 재사용은 공유, 읽기권한, 쓰기 전파, 지속성이 독립 조건이라는 점이다. 두 분야의 구현을 배열 API와 같은 것으로 분류하지 않는다. 수치 성능·ABI·비용 추정은 범위 밖; NARA의 hundreds GB 및 Windows commit charge는 해당 원전 설명이지 NumPy 비용 수치가 아니다.

## 유지자·이용자·동일 메모리 호출자
유지자는 다양한 객체/설치판 호환과 회귀 회피(H01,A02,A03); 이용자는 값이 필요하고 예외를 피하려 함(H02); 공유를 요구하는 호출자는 서로 다른 input dtype/order, writeability 및 원본 mutation을 계약으로 취급해야 함(N03,N04,F09). 마지막 사람은 실제 포럼 제보자가 아니라 요구 유형의 대비이다. 라이브러리 내부 원칙이 엄격 무복사를 약속하지 않으면 외부 호출자에게 그 약속을 추천할 수 없다.

## 보정된 탐색 원리
후보 링크를 먼저 출력하는 대신 (소비 목적, 실제 객체/변환, copy 허용, alias/쓰기, 패키지/NumPy 버전, 적용 태그, 증거 종류)를 잠정 연결한다. 값 생성에는 migration+실제 패치, no-copy에는 2.0 함수 contract+반례, 의도 불명에는 한 질문으로 분기. 내부 자료는 원문 링크 탐색 지원용, 최종 저장 DB/API/랭킹은 설계하지 않는다. 비용은 extra copy/변환, 실패 처리, 호환 분기, alias 검증 및 증거 확인; 값은 정량화하지 않는다.
