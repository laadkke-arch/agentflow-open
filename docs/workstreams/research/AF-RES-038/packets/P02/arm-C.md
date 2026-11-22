# 자료

이 파일은 배정된 보기의 추가 자료입니다. 공통 과제와 환경은 t0 문서를 따릅니다.

1. [CMake 3.23.3 — command-line manual](https://github.com/Kitware/CMake/blob/d566bd962df5b1bf0ec5d16e9e7affe592b8b3eb/Help/manual/cmake.1.rst)

   P02-R1·R2 → Introduction to CMake Buildsystems(L62–94), --parallel(L473–481).

   적용 한계: native build tool의 지원 범위가 있으며 이 문서만으로 Python wheel이나 pandas 빌드 성공을 확인할 수 없습니다.

2. [Meson 0.63.0 — Python module](https://github.com/mesonbuild/meson/blob/9c6dab2cfd310ef2d840a2a7a479ce6b9e563b1d/docs/markdown/Python-module.md)

   P02-R1·R3 → find_installation, extension_module, dependency, install_sources.

   적용 한계: native extension 선언 기능과 Python 배포 backend 연결은 별도 확인이 필요합니다.

3. [meson-python 0.7.0 — README](https://github.com/mesonbuild/meson-python/blob/2f9acf25e23de95b0ceead72770cad4acf19a449/README.md)

   P02-R3 → PEP517 backend 소개, Status, Platform Support.

   적용 한계: 당대 플랫폼별 내부 library 지원 차이가 있고 이 릴리스 자료는 pandas POC의 실제 실행 성공 증거가 아닙니다.
