# 자료

이 파일은 배정된 보기의 추가 자료입니다. 공통 과제와 환경은 t0 문서를 따릅니다.

1. [NumPy 1.4.0 — arraysetops.py](https://github.com/numpy/numpy/blob/4b42c8f6b81d87f35ed8dcf4430224992cf2d296/numpy/lib/arraysetops.py)

   N08-R3 → unique의 return_inverse 설명(L95–181). 한계: 이 함수의 반환값만으로 네 통계가 계산되지는 않습니다.

2. [NumPy 1.4.0 — add_newdocs.py](https://github.com/numpy/numpy/blob/4b42c8f6b81d87f35ed8dcf4430224992cf2d296/numpy/add_newdocs.py)

   N08-R2·R3 → bincount(L3810–3881)와 reduceat(L4341–4448)의 입력·감소 규칙. 한계: 두 API가 받는 그룹 표현과 반환하는 통계의 범위가 다릅니다.

3. [NumPy 1.4.0 — fromnumeric.py](https://github.com/numpy/numpy/blob/4b42c8f6b81d87f35ed8dcf4430224992cf2d296/numpy/core/fromnumeric.py)

   N08-R2·R3 → argsort(L579–666), sum·amax·amin·mean의 설명. 한계: 각 함수의 개별 계약은 전체 그룹 집계의 키-값 대응을 자동 보장하지 않습니다.
