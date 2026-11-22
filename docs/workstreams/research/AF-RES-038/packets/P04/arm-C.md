# 자료

이 파일은 배정된 보기의 추가 자료입니다. 공통 과제와 환경은 t0 문서를 따릅니다.

1. [pandas 1.4.4 — to_datetime documentation and implementation](https://github.com/pandas-dev/pandas/blob/ca60aab7340d9989d9428e11a51467658190bb6b/pandas/core/tools/datetimes.py)

   P04-R1·R2·R3 → errors(L703–706), dayfirst warning(L714–717), format/exact(L751–762), inference(L769–773).

   적용 한계: 이 판의 dayfirst 또는 infer_datetime_format 옵션과 명시 format의 보증은 같지 않으며 이 과제는 모든 입력·시간대의 호환성을 검증하지 않습니다.

2. [CPython 3.10.6 — datetime documentation](https://github.com/python/cpython/blob/9c7b4bd1646f2170247f88cf59936740d9c4c004/Doc/library/datetime.rst)

   P04-R1·R2·R3 → datetime.strptime(L1035–1047), strftime/strptime directives.

   적용 한계: 행별 API의 출력 타입과 지원 범위는 배열 API와 다르며 시간과 성능은 이 자료만으로 비교할 수 없습니다.
