# 판·용도·정정 반례와 대안 필드

| 사례 | 처음 가능해 보인 결론 | 반대 관측·원문 위치 | 보존한 판단 |
|---|---|---|---|
| RJ02 | 날짜만 있고 입력 manifest가 없을 것이다 | [고정 target_meta.RDS](https://github.com/chainsawriot/rstyle/blob/07a60457c88dbb20858441047f248d61ce2955c7/target_meta.RDS) year1998의16행과 [yearly feature record](https://github.com/chainsawriot/rstyle/blob/07a60457c88dbb20858441047f248d61ce2955c7/data/syntax_feature_yr1998.RDS)의 path16개가 일치 | 초기 U미확인은 반증됐다. U=true는1998 filename/version 선언 범위이며 실제 mirror bytes·run은 미확인. |
| RJ02 | 파일명 버전과 내부 Version은 같은 키다 | [acepack1.1](https://cran.r-project.org/src/contrib/Archive/acepack/acepack_1.1.tar.gz) DESCRIPTION=1.0-4; [class](https://cran.r-project.org/src/contrib/Old/0.61/class_5.2pl005-2.tar.gz)/[nnet](https://cran.r-project.org/src/contrib/Old/0.61/nnet_5.2pl005-2.tar.gz) DESCRIPTION=5.2pl005-1 | 이름 하나로 판 키를 합치지 않는다. 실제 접근 성공16/16과 값 검증을 분리한다. 공식 정정 이유는 미확인. |
| RJ03 | 해시가 같으면 한 판이거나 그 파일을 사용했다 | [R4.2.0](https://cran.r-project.org/src/base/R-4/R-4.2.0.tar.gz)과 [4.2.1](https://cran.r-project.org/src/base/R-4/R-4.2.1.tar.gz)의 iris.R 멤버 SHA가 같고 전체 tar SHA는 다름.4.2.1 공개일은 논문 발행 뒤 | 같은 바이트는 데이터 동일성을 돕지만 release 정체성·당시 사용의 연결이 아니다. 뒤의 공개 release 자체를 원 입력으로 지정할 수 없다. |
| RJ03/AUX-RJ-IRIS | 보고값 Df2가 맞으면 수정 전후 자료도 구별된다 | [UCI](https://archive.ics.uci.edu/dataset/53/iris) Additional Information rows35/38 및 [ZIP](https://archive.ics.uci.edu/static/public/53/iris.zip)의 두 실제 파일: 값·해시가 달라도 Df2는 같음 | Df2만 보는 목적에는 둘 다 양립. 정확 Petal.Length나 보조 SumSq에는 정정이 중요. 이 둘은 날짜 확정된 연속판이 아님. |
| RJ03 | Df 대신 SumSq를 고르면 실제판이 확정된다 | [소비자 §5](https://journal.r-project.org/articles/RJ-2022-007/) SumSq437.1은 UCI iris.data의436.6과 불일치하나 R두판·bezdek변형은437.1 | 보조 필드는 후보를 배제할 수 있지만 실제 R판·run을 지정하지 못한다. Primary Df를 교체하지 않음. |
| RJ01 | 부록 코드만 있으면 원 입력·값을 복구한다 | [ZIP](https://journal.r-project.org/articles/RJ-2022-004/RJ-2022-004.zip)의 shrinking_cities.r12,17–21이 research_data.xlsx를 읽지만 ZIP에 workbook 없음.47–57은 다른 row slicing | 실행 계획과 실제 실행을 분리. 정확 Fig2값을 Table2 std.dev2.40의 제곱으로 꾸며내지 않는다. |
| RJ01 | 같은0.44는 같은 관측이다 | [Table2](https://journal.r-project.org/articles/RJ-2022-004/)의1992·2018 variance proportion은 모두0.44, cumulative는44.2/44.0% | 시간 목적·행 키가 없으면 다른 기간을 합치게 된다. 기간차를 판차라고 부르지 않는다. |

현재 용도 판단은 findings.md §5의 정보제거 표와 연결한다. RJ01은 보류, RJ02는 특정filename선언 유지·실제실행/독립값 보류, RJ03은 좁은 Df양립 유지·실제사용판 보류다. 실제 사용자 채택은 관측하지 않았다.
