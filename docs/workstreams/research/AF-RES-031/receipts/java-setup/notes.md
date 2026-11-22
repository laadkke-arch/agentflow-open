# Java 빌드와 복구

- Temurin 21.0.10+7, Maven 3.9.11, CMake 3.31.6, Linux x86-64. CMake C 전용 설정과 설치 종료 0. 고정 arrow-java source tree에는 변경 사항이 없었다.
- 최초 Maven은 central로 직접 DNS를 시도해 확장 POM 전송에서 종료 1. 관리형 프록시를 Maven Settings에 지정하고 기존 JVM CA를 사용했다. 다음 실행은 reactor에서 기본 비활성인 c 모듈을 찾지 못했다. 고정 pom.xml L800–806 및 ci/scripts/test.sh L60에 따라 arrow-c-data profile을 추가했다.
- c profile test-compile의 9개 reactor 모듈은 성공했고 후처리에서 Develocity의 읽기 전용 홈에 쓰지 못해 명령은 종료 1. 재실행에 JVM 전용 임시 user.home을 지정했다. POM과 Java 원 시험 소스는 동일하다.
- 원 테스트 첫 선택은 두 건 모두 실행됐지만 CMake는 lib/arrow_cdata_jni 아래에 설치했고 JNI loader의 classpath 상대 경로에는 lib 접두사가 없었다. export 단계에서 FileNotFoundException 두 건을 기록했다. JniLoader.java L77–105가 공식으로 지원하는 arrow.cdata.library.path에 실제 디렉터리를 연결해 두 시험을 동일 이름으로 다시 실행했다.
- 검사는 Java 공급자 두 건, 별도 Java 프로세스 IPC 두 입력, 동일 프로세스 C Data 두 입력, 별도 고주소 payload 한 입력이다. 잘못된 예상 형을 준 IPC 증명용 실행은 정상적으로 실패하며 정식 15행 분모 바깥에 있다.
