# 로컬 구성 대조 실행 원장
실제 실행 환경: container / (Git worktree 아님), jq-1.7, Python 3.13.5. 원저자/고정 소스 판과 동일하지 않다. 원저자 첨부, macOS, Cygwin, Anaconda, oniguruma 빌드는 미재현. 아래는 직접 실행 결과이며 공식 테스트 파일은 실행하지 않았다. 전체 스크립트 프로세스 exit 0; 각 jq subprocess exit 아래. 실행 UTC 개별 초 미계측, 2026-11-24 같은 세션. 
## jq: 명령 인수 / stdin / exit / 출력
- J1: jq -n --stream 'fromstream(1|truncate_stream(inputs)) | INDEX(.id)' ; stdin [{"id":"1","userId":"fa51531d"},{"id":"2","userId":"a167869a"}]; exit5, stdout empty, stderr Cannot index string with string "id".
- J1-alt: jq -n --stream 'INDEX(fromstream(1|truncate_stream(inputs)); .id)' ; same stdin; exit0, stdout object {"1":{"id":"1","userId":"fa51531d"},"2":{"id":"2","userId":"a167869a"}} (pretty printed), stderr empty. Output object memory not bounded by input record size.
- J2: jq 'fromjson' ; stdin JSON string "apiVersion: v1\nkind: Namespace\nmetadata:\n  name: test\n"; exit5, stderr Invalid numeric literal at line 1, column 11 (while parsing YAML); stdout empty. jq 'fromyaml' stdin "apiVersion: v1"; exit3, not defined, stdout empty. No inference about plugins/custom modules.
- J3: jq -nR 'inputs|gsub("^(?!cd ).*$|^cd "; "")' ; stdin "not a cd cmd\ncd /ok\n"; exit0 stdout "\"\"\n\"/ok\"\n", stderr empty. Alternative jq -nR 'inputs|if startswith("cd ") then .[3:] else "" end' same exact output, exit0. 1.6 author's failure not reproduced on 1.7.
- O42: jq -c '.date |= strptime("%Y-%m-%dT%H:%M:%SZ")' ; stdin {"date":"2024-01-05T23:51:47Z"} and separately {"date":"2024-06-08T16:34:21Z"}; each exit0, stdout {"date":[2024,0,5,23,51,47,5,4]} and {"date":[2024,5,8,16,34,21,6,159]} followed newline. Additional 2015-01-05/06-05 plain string test same zero-based month, date fields retained.
- O50: jq -e '. | has("foo")'; stdin "\n" exit4, " \n" exit4, "{}\n" exit1 stdout false newline, "{\"foo\":1}\n" exit0 stdout true newline; all stderr empty; empty/whitespace stdout empty. Author jq1.6 exit0 report conflicts with local 1.7.
- O59: jq -c ' . as $v | ("0",1,2,"0") as $k | $v[$k]?' ; stdin {"0":1}; exit0 stdout "1\n1\n". jq -c ' .["0",1,2,"0"]' same input exit5 stdout "1\n", stderr Cannot index object with number. jq -c ' .["0",1,2,"0"]?' same input exit0 stdout "1\n1\n". jq -c '. as $v | (0,-1,0,0,"0",2) as $k | $v[$k]?' stdin [1,2,3,4,5], exit0 stdout "1\n5\n1\n1\n3\n". No fixed 1.7.1 execution.
## Python exact synthetic commands
Run Python 3.13.5, stdlib csv/io:
~~~python
import csv,io
for last in ['a,b\r\n1,2','a,b\r\n1,2\r\n']:
 s=io.StringIO(last,newline='');s.seek(0,2);csv.DictWriter(s,fieldnames=['a','b']).writerow({'a':'3','b':'4'});print('P1',repr(last),repr(s.getvalue()),list(csv.reader(io.StringIO(s.getvalue(),newline=''))))
text='SEP=;\nHeader_Col1;Header_Col2;Header_Col3\nRow1_Col1;Row1_Col2;Row1_Col3\n'
print('P2-default',list(csv.DictReader(io.StringIO(text))))
f=io.StringIO(text);next(f);print('P2-skip',list(csv.DictReader(f,delimiter=';')))
for x in ['a,b,c\n1,,3\n','a,b,b\n1,,3\n','a,b,c\n1,\n','a,b,c\n\n']:
 print('P3',repr(x),list(csv.reader(io.StringIO(x))),list(csv.DictReader(io.StringIO(x))))
~~~
Observed stdout:
~~~text
P1 'a,b\r\n1,2' 'a,b\r\n1,23,4\r\n' [['a', 'b'], ['1', '23', '4']]
P1 'a,b\r\n1,2\r\n' 'a,b\r\n1,2\r\n3,4\r\n' [['a', 'b'], ['1', '2'], ['3', '4']]
P2-default [{'SEP=;': 'Header_Col1;Header_Col2;Header_Col3'}, {'SEP=;': 'Row1_Col1;Row1_Col2;Row1_Col3'}]
P2-skip [{'Header_Col1': 'Row1_Col1', 'Header_Col2': 'Row1_Col2', 'Header_Col3': 'Row1_Col3'}]
P3 'a,b,c\n1,,3\n' [['a', 'b', 'c'], ['1', '', '3']] [{'a': '1', 'b': '', 'c': '3'}]
P3 'a,b,b\n1,,3\n' [['a', 'b', 'b'], ['1', '', '3']] [{'a': '1', 'b': '3'}]
P3 'a,b,c\n1,\n' [['a', 'b', 'c'], ['1', '']] [{'a': '1', 'b': '', 'c': None}]
P3 'a,b,c\n\n' [['a', 'b', 'c'], []] []
~~~
Source tests (assertions) are not execution observations. All above are synthetic, except inputs taken verbatim from author as noted; no participant reader.
