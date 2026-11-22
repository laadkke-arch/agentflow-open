# 자료

이 파일은 배정된 보기의 추가 자료입니다. 공통 과제와 환경은 t0 문서를 따릅니다.

1. [pandas 1.5.2 — dtype cast implementation](https://github.com/pandas-dev/pandas/blob/8dab54d6573f7186ff0c3b6364d5e4dd635ff3e7/pandas/core/dtypes/cast.py)

   P06-R1·R2·R3 → np_can_hold_element(L1931–2009), integer/whole-float guard(L1953–1966).

   적용 한계: 내부 helper이며 안정된 public API가 아닙니다. 소비자 편집기에 조합한 설계의 실행 여부는 따로 확인해야 합니다.

2. [pandas 1.5.2 — masked array implementation](https://github.com/pandas-dev/pandas/blob/8dab54d6573f7186ff0c3b6364d5e4dd635ff3e7/pandas/core/arrays/masked.py)

   P06-R1·R2·R3 → _validate_setitem_value 및 __setitem__(L198–235).

   적용 한계: nullable scalar 경로이며 NA·overflow·vector 입력에까지 이 범위의 근거를 확장하지 마세요.

3. [pandas 1.5.2 — nullable integer user guide](https://github.com/pandas-dev/pandas/blob/8dab54d6573f7186ff0c3b6364d5e4dd635ff3e7/doc/source/user_guide/integer_na.rst)

   P06-R1 → Construction의 명시 dtype과 추론 차이.

   적용 한계: 생성 설명만으로 모든 setitem의 거부 동작을 확인할 수 없으며 기존 컨테이너의 dtype을 바꾸는 허용을 뜻하지 않습니다.
