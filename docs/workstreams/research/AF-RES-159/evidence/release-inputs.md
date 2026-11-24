# 발행판과 조회 입력 대조

- **GIMP 3.0.6.** 2025-10-06 공지의 안정판과 2026-01-24 3.0.8을 공식 소스 목록에서 대조했다. 태그 객체는 `a46d3b3e85ffe2223c4c1ab27b54de10ed24652e`, 태그가 가리킨 실제 커밋은 `a77e8fd05d3d08a58650531a3700100f6a3216b7`. Meson 버전 3.0.6, `po/LINGUAS` 18·47행의 de·ko, `po/meson.build`의 주 도메인 설치, `app/main.c` 1161–1166행의 bind/codeset/textdomain을 확인했다. 각 고정 PO는 GitHub 태그 checkout과 full commit raw GET에서 바이트가 일치했다. 공식 별도 dist tar의 표준 SHA-256은 `246c225383c72ef9f0dc7703b7d707084bbf177bd2900e94ce466a62862e296b`. 쉘에서 공식 tar, GNOME 호스트, 미러와 AppImage 요청이 403으로 막혀 tar 실내용과 공식 패키지 MO는 미확인이다. [공지](https://www.gimp.org/news/2025/10/06/gimp-3-0-6-released/) [공식 목록](https://download.gimp.org/gimp/v3.0/) [태그 소스](https://github.com/GNOME/gimp/tree/a77e8fd05d3d08a58650531a3700100f6a3216b7) [AppImage 목록](https://download.gimp.org/gimp/v3.0/linux/)
- **Inkscape 1.4.3.** 2025-12-14 후보와 12-26 정식 발행 공지를 구별했다. GitLab 태그 `INKSCAPE_1_4_3`는 2025-12-25의 `0d15f7504220b00925bc3cb3673fcf44610a17d5`. 그 커밋 트리의 `po`는 모드 160000의 `dd0592f12a5da07802a96b53293bbe12acdf45ff`이며 `.gitmodules` 13–17행은 translations.git 1.4.x를 가리킨다. 1.4.x 최신 head나 날짜가 비슷한 Weblate 사본을 사용하지 않았다. 3개 고정 파일(POT, ko/de PO)의 tar 대 gitlink raw GET `cmp`는 모두 종료 0. CMake 38–41행의 1.4.3 버전과 `po/CMakeLists.txt` 4–20행의 GNU gettext·`inkscape.mo` 설치를 확인했다. GitLab 태그 tar.gz `041d3a15ae26c69fc96ed2eaaf8e6a07954eec15e7ae298efbe558e6c105e025`에는 gitlink 내용이 비어 있다. Debian `.orig.tar.xz` `e83a2c3db570b6c5a1ff0fccfe7098837b3f6bd74b133567937c8a91710ed1d1`에 root `inkscape-1.4.3_2025-12-25_0d15f75042`, `po/ko.po`, `po/de.po`, `po/inkscape.pot`가 있다. `.dsc`의 SHA-256과 BLFS가 발행 URL에 명시한 MD5 `51779347adc1e9dafa3ab1f4d79aca13`도 일치했다. [공지 목록](https://lists.inkscape.org/hyperkitty/list/inkscape-announce@lists.inkscape.org/2025/12/) [태그](https://gitlab.com/inkscape/inkscape/-/tags/INKSCAPE_1_4_3) [번역판](https://gitlab.com/inkscape/translations/-/commit/dd0592f12a5da07802a96b53293bbe12acdf45ff) [발행 URL과 MD5를 명시한 BLFS](https://www.linuxfromscratch.org/blfs/view/13.0-systemd/xsoft/inkscape.html#package-information)
- 두 소스의 명명된 번역 자리 4/4가 존재한다. GIMP ko PO 내부 Project-Id는 GIMP 2.10이고 revision 2022-04-10이다. 헤더 이름으로 3.0.6의 공급 파일을 갈아끼우지 않았다. 최신 헤더와 오래된 렌더링 문자열 여부를 태그 파일·구체 키·실행으로 각각 보았다.

| 판·언어 | 원본 PO SHA-256 | 로컬 컴파일 MO SHA-256 | 해당 MO의 별도 패키지 |
|---|---|---|---|
| GIMP ko | `f2fff38b523c3ac78e6a9e48773f3321dcacb833bd6cdf5ea7c7512f629b9579` | `f0ffc71c93dce0f4a62933a5b2ef58aa84d01b4af0153da7b5fd2f116bd45bbb` | 공식 바이너리 미확인 |
| GIMP de | `8757f48b40709f92a8d3be1c32232833ada2872833be480469b94bcf29ceaae7` | `7c1e77e015a2c12f39b42f41e926cd027e1e0e6cf65fa6cec6f541540ba328b1` | 공식 바이너리 미확인 |
| Inkscape ko | `3d7af816d652468a60c78e36fb824739ec1ad1d8182fef52024c091e5fbaae1d` | `cf6e6d6a70d57e177b39d716eaac9fa94328b5b3586a0400877f0110e1f448da` | Debian 배포 MO와 SHA-256 일치 |
| Inkscape de | `c1d4de687e9394a8c34ea625ecf6de29866d6fe68cd7802bcbede8d8d59af9f3` | `1632fda0a62127f86a6c933aeab73f25b4e18c564135a43ef574b48cd0fb331f` | Debian 배포 MO와 SHA-256 일치 |

Inkscape Debian `inkscape_1.4.3-2+b2_amd64.deb` SHA-256 `852e19c0aa502aead85436c8786955f43a7009b8e0025cc22fe4e22debd84fbf`. `dpkg-deb --fsys-tarfile PACKAGE | tar -x ./usr/share/locale/ko/LC_MESSAGES/inkscape.mo ./usr/share/locale/de/LC_MESSAGES/inkscape.mo`로 분리했다. 두 `published` MO는 이 Debian 배포의 데이터다. 업스트림 AppImage·Windows·macOS 설치본의 지문은 미확인이다. [Debian orig tar](https://deb.debian.org/debian/pool/main/i/inkscape/inkscape_1.4.3.orig.tar.xz) [소스 영수증](https://deb.debian.org/debian/pool/main/i/inkscape/inkscape_1.4.3-2.dsc) [Debian 바이너리](https://deb.debian.org/debian/pool/main/i/inkscape/inkscape_1.4.3-2+b2_amd64.deb)

## 실행 영수증

실제 데이터는 [runs.jsonl](../runs.jsonl)이다. GNU gettext-tools/runtime 0.23.1(`gettext` Debian 아카이브 `25293e75989db79a1d4a6b942674b0e7243da54a0985f8d9df1b345d255d262b`, `gettext-base` `1a3dfadd661520ff01d379fd89cd0d49972a5a775d490609f1712134ee3d62ca`), GLib 2.84.4 Debian `2.84.4-3~deb13u5`, glibc 2.41, GCC 14.2.0. 각 실행 행은 명령·UTC·작업공간·종료·실제 바이트·입출력 SHA를 담는다. 빌드와 GNU 조회에 같은 gettext 버전을 사용했다. 발행 빌드에서 사용한 gettext 세부 버전은 미확인이다.

- W1·W2에서 고정 카탈로그 4개를 별도로 복사하고 컴파일했다. 총 엄격 검사 8, 통상 컴파일 8, GLib C probe 빌드 2가 모두 0. 고정 argv는 `replay/run.py`에서 복원한다.
- 각 W의 compiled 자연/대조 문맥 56 + 무문맥 56, 없는 문맥 56 + 초기 기본 도메인 56 + 다른 실재 문맥 48. Debian MO의 Inkscape 문맥 28 + 무문맥 28이 추가된다.
- 두 독립 작업공간의 입력·출력·MO 지문 불일치 0/328 대응. GNU CLI와 GLib 공개 API 출력 불일치 0/656. 두 API 프로세스의 종료 오류 0. 화면은 열지 않았다.
- 기본 도메인 대조는 CLI에서 TEXTDOMAIN을 제거하고 C에서는 초기 `messages`를 그대로 둔다. 무문맥 대조는 실제 도메인을 설정한다. 두 조건의 차이는 세팅이며 다른 제품이나 번역 자료를 넣지 않았다.
