# C02 · 원 PIL 1.1.7 배포물의 독립 확보

## 결과와 범위

**공식 Debian archive에서 원본 tarball을 확보했다.** `python-imaging_1.1.7.orig.tar.gz`는 498,749 bytes이며 SHA-256은 `895bc7c2498c8e1f9b99938f1a40dc86b3f149741f105cf7c7bd2e0725405211`이다. 같은 archive의 `python-imaging_1.1.7-2.dsc`에 기록된 SHA-256·SHA-1·MD5 및 길이와 모두 일치한다. 별도 Debian `.diff.gz`도 세 지문이 일치한다. 검사는 `archive-verification.json`에 주체·UTC·종료값0으로 남겼다.

이 결과는 Pillow repository에 옮겨 실린 README에만 의존하던 **원소스 확보 공백**을 줄인다. 배포물의 279개 member 중 원 README, setup, selftest, package placeholder, Image.py, ImageFile.py, PngImagePlugin.py를 직접 읽었다. 원 tarball에는 Debian patch를 적용하지 않았다. 현재 pythonware 페이지를 원 저자 근거로 쓰지 않았다. 이 보존본·원작판·반복 열람은 **추가 독립 저작 수 0**이다.

`.dsc`의 PGP 서명은 검증하지 않았다. 따라서 증거 범위는 공식 Debian 보존 경로와 descriptor/바이트의 일치이며, 원 발행 당시 upstream 서버 응답 또는 별도의 upstream 서명 신뢰 사슬을 확인했다는 뜻은 아니다. native PIL1.1.7은 실행하지 않았다.

## 원본과 Debian patch의 구분

| 확인 항목 | 직접 확인한 내용 | 근거 |
| --- | --- | --- |
| 원 발행판·저자 | 원 README는 2009-11-15의 PIL1.1.7, Secret Labs AB/Fredrik Lundh를 표시 | PA001; archive `Imaging-1.1.7/README` |
| upstream와 패치 파일 | `.dsc`는 `orig.tar.gz`와 `1.1.7-2.diff.gz`를 별도 파일로 지정 | PA002 |
| Debian -2 변경 | 2010-07-26 build dependency와 packaging 변경; patch 경로는 Debian metadata/rules와 `Scripts/pilfont.py` | PA003 |
| Image.py 무패치 확인 | 원 tar member와 Debian Sources의 `1.1.7-2/PIL/Image.py`가 바이트 동일 | PA004·PA005 |
| 파일 지문 | Image.py SHA-256 `a1872f7d4083d2edb0947473e292442440038750770fe4b30e34f5313043d625` | `source-members.json` |

이 비교는 정확히 Debian **1.1.7-2**에 한정된다. 이후 보안 패치판까지 원본과 동일하다고 하지 않는다. Debian copyright는 과거의 2001년 저작권 연도를 유지하지만 원본 README/Image.py에는 2009년이 있다. 판 식별에는 원본을 우선한다.

## import 이름에 관한 수정 가능한 주장

원 PIL의 `selftest.py`는 이미 `from PIL import Image`를 사용한다(PA007, L8-11). `setup.py` L477-482에는 `extra_path`, `package_dir`, 빈 package 이름을 조합한 설치 구조가 있고, tarball의 `PIL/__init__.py`도 존재한다(PA006). 따라서 **`PIL` namespace를 사용한다는 사실만으로 Pillow라는 배포물을 식별할 수 없다.** `from PIL import Image`를 Pillow가 처음 도입했다고 해석해서도 안 된다.

이는 2010년 Laurence Rowe의 직접 보고(R015 반복, PA010)와 교차 확인된다. Python2.6.4의 원본 easy_install에서는 top-level `Image`만 import되고, 직접 setup.py 설치에서는 두 경로가 된다. 제안 patch의 egg에서는 `PIL`이 되지만 top-level `Image`가 실패한다. 이 보고의 57개 selftest 통과는 **patch 후 그 실행 환경**의 보고이지 원본 전체·현재 Pillow 전체의 호환 보증이 아니다. 원 selftest의 ZLIB support 확인은 encoder 존재 검사이며, 연구에서 쓰는 특정 PNG를 디코드한 증거가 아니다.

## 이미지 동작과 예외의 원절

| 요구·입력 | 원본의 정적 근거 | 관측 수준·한계 |
| --- | --- | --- |
| 정상 PNG를 열고 픽셀 확인 | Image.py L1926-1980의 open은 lazy 식별; PNG plugin L302-359가 header와 tile을 설정; 실제 load는 ImageFile.py L124-230 | 코드 판독. 같은 PNG를 원 PIL에서 실행하지 않아 픽셀·mode·순서 보존은 보류 |
| C decoder가 없음 | Image.py L49-66은 일부 식별을 허용하지만 load에 `_imaging`이 필요; L371-385는 누락 decoder 오류 | import/open 성공을 decode 성공으로 바꿀 수 없음 |
| open mode가 r이 아님 | Image.py L1943-1947의 ValueError | 예측; 원 runtime 미실행 |
| 포맷을 식별할 수 없는 header | Image.py는 plugin 시도 중 일부 오류를 잡고, 끝에 IOError를 반환(L1959-1980) | 모든 손상 입력이 같은 단계·예외가 된다고 일반화하지 않음 |
| 픽셀 data가 잘림 | ImageFile.py L197-215의 EOF/decoder 결과 처리 | load 단계 오류. open 단계와 별도 기록 필요 |
| PNG verify를 load 뒤에 호출 | PngImagePlugin.py L361-373의 파일 handle 조건과 RuntimeError | verify는 open 직후 해야 함; 파일 재개방이 필요할 수 있음 |
| PNG CRC를 모두 검증하는가 | PNG header/verify 경로는 CRC를 검사하지만 load_read L383-403은 data chunk CRC를 건너뜀 | 성공적인 pixel load만으로 전체 checksum 검증 성공을 주장할 수 없음 |
| 지원하지 않는 mode로 PNG 출력 | PngImagePlugin.py L462-506의 mode table 및 IOError | P2의 출력/오류 비교 입력으로 쓸 수 있으나 양판 실행은 남아 있음 |

단순한 “열렸다/안 열렸다” 비교는 lazy decode와 verify 순서를 놓친다. 후속 실행에서는 **import → open → load → pixel 검사 → 별도 reopen+verify**를 각각 기록해야 한다. fork 계보와 이 단계별 행동 적합성은 별도 판정이다.

## 원격 주소와 재개 명령

원 tarball: <https://archive.debian.org/debian/pool/main/p/python-imaging/python-imaging_1.1.7.orig.tar.gz>

descriptor: <https://archive.debian.org/debian/pool/main/p/python-imaging/python-imaging_1.1.7-2.dsc>

별도 patch: <https://archive.debian.org/debian/pool/main/p/python-imaging/python-imaging_1.1.7-2.diff.gz>

바이트 대조한 Image.py: <https://sources.debian.org/data/main/p/python-imaging/1.1.7-2/PIL/Image.py>

2010 공급자 보고: <https://mail.python.org/pipermail/image-sig/2010-August/006480.html>

연구 디렉터리의 `acquire.py`와 `inspect_archive.py`를 순서대로 실행하면 다운로드와 지문/원본 분리가 재현된다. native PIL 자체는 실행하지 않는 명령이다.

```bash
python3 docs/workstreams/research/AF-RES-079/streams/pil_archive/acquire.py
python3 docs/workstreams/research/AF-RES-079/streams/pil_archive/inspect_archive.py
```

native 최소 첫 행동은 원 PIL1.1.7용 Python2와 `_imaging`/zlib가 있는 분리 환경을 확보하고 설치 방법을 고정하는 것이다. 그 환경에서 `python2 setup.py build_ext -i` 및 `python2 selftest.py`를 실행할 수 있으나 이 연구에서는 실행하지 않았다. 후속 paired PNG 검사는 통합 원장에 이미 봉인한 입력 bytes/hash를 양쪽에 동일하게 전달해야 하며, 새 이미지로 교체해 비교하지 않는다. 현재 Python3에서 source 문법만 변환해 실행하는 것은 원 runtime 시험으로 산입하지 않는다.

바이너리 tarball·원문 cache는 ignore 처리했다. 보존 산출물에는 HTTP 영수증 7개, source rows10개(추가 산입0), 관측4개, member 지문7개, 지문검사 결과와 이 분석이 있다.
