"""Build this independent reader's gold and source ledger from inspected evidence.

Reads only the fixed corpus, selected original issues, and this reader's own work.
Never reads authoring, packet text, recipient trails, answers, or other gold.
"""
from pathlib import Path
from collections import defaultdict, Counter
import json, gzip, hashlib
from capture import BASE, now

ROOT=BASE.parents[1]
DOCS={d['id']:d for d in json.loads(gzip.decompress((ROOT/'corpus.json.gz').read_bytes()))['documents']}
EVENTS=[json.loads(s) for s in (BASE/'read-events.jsonl').read_text().splitlines()]
INSPECT=json.loads((BASE/'input-inspection.json').read_text())
SUPP=json.loads((BASE/'supplementary-input-inspection.json').read_text())
CONSTRUCTED=json.loads((BASE/'supplementary-constructed-results.json').read_text())

def srcid(s):
    return s.removesuffix('.json').removesuffix('.html').removesuffix('.pdf')

def span(identifier,did,anchor,conditions,start=None,end=None,first=None,last=None,quote='',sufficiency='partial',why=''):
    d=DOCS[did];t=d['text']
    if start is None:start=t.index(first) if first else d['anchors'][anchor]
    if end is None:
        end=t.index(last,start) if last else t.index('\n',start)
    assert 0<=start<end<=len(t)
    assert quote in t[start:end]
    if anchor is not None:assert anchor in d['anchors']
    return {'interval_id':identifier,'doc_id':did,'start':start,'end':end,'offset_unit':'Unicode code points, zero-based half-open in corpus documents[].text','anchor':anchor,'small_quote':quote,'conditionIDs':conditions,'sufficiency':sufficiency,'qualification_ko':why,'inside_corpus':True,'source_id':did,'version':d['version'],'source_sha256':d['source_sha'],'upstream_commit':d['upstream_commit'],'original_url':d['url'],'fixed_source_url':d['upstream_source_url']}

INTERVALS={}
def add(x):INTERVALS[x['interval_id']]=x;return x['interval_id']
I1=[];I2=[];I3=[];S=[]
I1.append(add(span('I1-O-gray','i7113_command-line-options','colorspace',['O'],start=48327,last='Conversion of RGB to Other Color Spaces',quote='-colorspace value',why='Gray 선택과 색공간 전환 일반 규칙. JPEG 디코더·양자화까지 포함한 특정 grayscale plane 재현은 이 구간만으로 검증되지 않는다.')))
I1.append(add(span('I1-O-fx','i7113_command-line-options','channel-fx',['O'],start=37371,last='For example, to create',quote='copy one channel',why='=> 복사와 | 입력 이동의 정의. meta라는 목적 채널의 실제 구현 및 TIFF의 저장 표지는 별도 근거가 필요하다.')))
I1.append(add(span('I1-P-format','i7113_architecture','multispectral',['O','P','E1'],start=32131,last='If you have a use case',quote='same dimensions',why='동일 크기 채널과 TIFF multispectral 지원 일반설명. 특정 writer·viewer의 올바른 해석을 보장하지 않는다.')))
I1.append(add(span('I1-E-extra-label','i7113_defines',None,['P','E1'],start=33712,end=33835,quote='associated|unassociated|unspecified',why='세 지정값의 존재만 제시한다. 0/1/2 의미, unspecified와 transparency의 차이, 원파일 태그는 제시하지 않는다.')))
I1.append(add(span('I1-P-channel-description','i7113_escape',None,['P'],first='%[channels]',last='%[colors]',quote='meta channels',why='전체 채널수와 meta 채널수가 별도라는 설명. 데이터·외관·태그가 실제 보존되었다는 증거는 아니다.')))

I2.append(add(span('I2-O-extract','i7114_command-line-options','alpha',['O','P'],first="Extract\nCopies the alpha",last='Copy\n',quote='alpha channel values',sufficiency='conditional_operation_definition',why='실제로 alpha로 정의된 채널이 있을 때 grayscale mask로 복사한다. extra sample이 alpha인지 먼저 확인해야 한다.')))
I2.append(add(span('I2-E-set','i7114_command-line-options','alpha',['E2'],first='Set\nActivates the alpha',last='Opaque\n',quote='resets the channel to opaque',sufficiency='sufficient_for_this_warning_only',why='-alpha set은 꺼져 있던 alpha를 opaque로 초기화하므로 원 mask를 복구한다는 무조건적 해법이 아니다.')))
I2.append(add(span('I2-O-fx','i7114_command-line-options','channel-fx',['O','P'],start=37371,last='For example, to create',quote='copy one channel',why='알려진 source plane 복사 문법. meta 존재와 의도된 의미는 입력과 구현에서 확인해야 한다.')))
I2.append(add(span('I2-O-separate','i7114_command-line-options','separate',['O','P'],start=209931,end=210036,quote='grayscale image',sufficiency='conditional_operation_definition',why='확인한 추가 plane을 grayscale로 꺼내는 별도 방법. 어떤 plane이 요청 대상인지 이 구간은 알 수 없다.')))
I2.append(add(span('I2-E-extra-label','i7114_defines',None,['E1','E3'],start=33712,end=33835,quote='associated|unassociated|unspecified',why='명칭만으로 associated의 premultiplication 요건이나 TIFF reader의 meta 처리를 확정할 수 없다.')))

I3.append(add(span('I3-O-jp2-capability','i7116_formats','supported',['O'],first='JP2\tRW',last='\nJPT',quote='JP2 File Format',sufficiency='capability_only',why='JP2 읽기/쓰기 지원 표지. 해당 파일 색공간·4개 성분의 의미·보존 여부는 알려주지 않는다.')))
I3.append(add(span('I3-E-grayscale-representation','i7116_porting','grayscale',['P','E1'],start=12816,end=13022,quote='only 1 channel',why='v7 grayscale 표현은 1개 채널이라는 일반설명. 보고된 4개 codestream component의 실제 의미와 decoder 결과는 별도 확인해야 한다.')))
I3.append(add(span('I3-E-alpha-definition','i7116_porting','alpha',['E1'],start=11911,end=12518,quote='pixel is opaque',why='alpha의 coverage 뜻. 4번째 component를 alpha로 간주할 근거가 되지는 않는다.')))
I3.append(add(span('I3-P-multispectral','i7116_architecture','multispectral',['P','E2'],start=32189,last='If you have a use case',quote='same dimensions',why='여러 채널을 담을 수 있는 일부 형식의 일반설명. 고정 JP2 reader가 네 채널의 색/IR 의미를 보존한다는 보장은 아니다.')))

S.append(add(span('S-P-profile','i7113_command-line-options','profile',['P_profile'],start=192063,last='To extract a profile,',quote='find out which profiles',why='내장 profile 확인과 strip의 관계. alpha sample 보존을 설명하지 않는다.')))
S.append(add(span('S-E-strip','i7113_command-line-options','strip',['P_profile','E_profile'],start=226482,end=226706,quote='profiles, comments',sufficiency='sufficient_for_documented_removal',why='strip이 ICC 관련 메타데이터를 제거한다. 보조 합성 입력은 설치된 7.1.1-43에서만 확인했으며 자연 3건의 고정판 결과가 아니다.')))

COMMON_LIMITS={
 'runtime':'원문의 7.1.1-3/-4/-6 바이너리와 당시 delegate/OS 조합은 실행하지 않았다. 설치된 7.1.1-43은 inventory 및 별도 합성 반례에만 사용했다.',
 'read_protocol':'download 자체는 direct read로 세지 않았다. read-events.jsonl에 실제 표시/검사 UTC를 기록했다. 한 긴 출력이 잘린 사건은 display_truncated_batch로 표시하고 의존하는 부분을 짧게 다시 읽었다.',
 'corpus':'아래 span은 고정 corpus의 실제 오프셋이다. 최소 근거의 일부가 corpus 밖에 있으므로 문서뷰만의 완전지원은 unknown이다. 이 reader는 3개봉 그래프를 열거하지 않았고 unreachable을 선언하지 않는다.',
 'counting':'동일 매뉴얼의 페이지·앵커·버전은 한 저작. 원요청의 댓글·첨부는 같은 lineage. 추가 반례의 댓글·수정 설명·첨부도 원 반례와 같은 lineage다.'}

def outside(identifier,conditions,refs,need,complete=True):
 return {'requirement_id':identifier,'inside_corpus':False,'conditionIDs':conditions,'source_ids':refs,'required_evidence_ko':need,'available_in_reference_layer':complete}

CASES=[
 {'case_id':'I1','original_request_source_id':'issue-6159','specified_version':'7.1.1-3','upstream_commit':'c5d5e7117fb07096158bcad05e1086f0c2fff172','start_doc_id':'i7113_processing',
  'O_definition':'lena RGB 영상에 mandril3를 Gray로 바꾼 한 plane을 meta 채널로 추가하여 TIFF를 저장한다.',
  'P_definition':'기존 RGB 샘플과 보이는 RGB 외관을 유지하고 추가 plane을 불투명도(alpha)로 적용하지 않는다. meta 데이터의 실제 값과 뜻을 함께 보존한다.',
  'semantic_complete':True,'fixed_corpus_semantic_complete':False,'input_unresolved':False,'historical_runtime_complete':False,
  'correct_answer':{'disposition':'qualified_supported','answer_ko':'회색 plane을 meta로 복사하는 의도는 타당하다. 회수한 meta.tif는 RGB photometric=2, SamplesPerPixel=4, ExtraSamples=(0,)인 TIFF이며, 네 번째 plane은 alpha로 표지되지 않았다. 직접 읽은 RGB의 모든 샘플은 lena.png와 동일하고 extra plane은 3–220으로 변한다. 고정 writer도 alpha가 없고 meta만 있을 때 unspecified extra sample을 쓴다. 따라서 첨부 출력이 네 번째 plane을 alpha처럼 그렸다는 이유만으로 RGB 데이터 훼손이나 writer의 alpha 저장 버그를 확정하면 안 된다. 후속 댓글은 ImageMagick display/Photoshop은 올바르게 표시하고 Mac Preview/GraphicConverter는 alpha처럼 표시했다고 보고한다. 이는 당시 작성자·maintainer의 관찰이며 이 reader가 해당 앱을 재현한 결과는 아니다. TIFF의 extra sample 의미를 따르는 표시기에서 확인해야 하며 모든 viewer에서 같은 외관을 강제할 수 있다는 답은 지원되지 않는다.',
    'commands_unexecuted':[{'command':"magick lena.png \\( mandril3.jpg -colorspace gray \\) -channel-fx '| gray=>meta' meta.tif",'preconditions':'7.1.1-3의 바이너리·delegates로 실행; 두 원입력 SHA는 input-inspection.json 참조; 출력은 별도 작업 디렉터리. 원문 끝의 typographic quote를 ASCII 단일 따옴표로 정상화한 의도상 명령이다.','claim':'문서와 fixed source로 뒷받침되는 절차, 이 세션의 historical runtime 성공 아님.'}, {'command':"magick identify -verbose meta.tif",'preconditions':'동일 7.1.1-3 런타임','claim':'channel/metadata 진단; 원시 TIFF tag 검사와 viewer 확인을 대체하지 않는다.'}]},
  'required_exceptions':[{'id':'E1','text':'TIFF ExtraSamples=0은 unspecified, 1은 associated alpha, 2는 unassociated alpha다. 4 samples만으로 RGBA를 결정하지 않는다.'},{'id':'E2','text':'viewer가 unspecified를 alpha로 오해할 수 있다. source-reported app 차이와 locally inspected file facts를 구분한다.'},{'id':'E3','text':'채널 크기·개수, writer 지원, RGB 및 extra plane 값, 색 해석을 각각 확인한다. 동일 RGB만으로 모든 color profile과 표시 환경 보존을 증명하지 않는다.'}],
  'counter_input_provenance':{'type':'original_reported_output_attachment','url':'https://github.com/ImageMagick/ImageMagick/files/10959346/meta.tif.zip','archive_sha256':'fab80ce67c51843376ad36e0205411154369312966da3e51670ce25ef5a61150','extracted_sha256':'1290cdd5eb69e627a428996b827986a7895689d6cc45b78c088b70cc0d65703a','locally_inspected':True,'inspection':'input-inspection.json','original_body_only':'추가 plane이 alpha처럼 보인다는 불만; viewer 이름·ExtraSamples tag는 원 body에 없음.','later_layer':'댓글과 현재 회수 첨부의 실제 태그를 gold 읽기에서 처음 확인했다.'},
  'minimal_supporting_intervals':[INTERVALS[x] for x in I1],
  'outside_corpus_requirements':[outside('I1-E-tiff-spec',['P','E1'],['TIFF6'],'TIFF 6.0 pp.31–32 ExtraSamples의 0/1/2 정의; p.77 associated alpha의 RGB premultiplication 요건.'),outside('I1-impl',['O','P','E1'],['tiff-7.1.1-3.c'],'고정 reader lines1700–1737, writer3622–3655; undefined alpha와 meta를 구분한다.'),outside('I1-input',['P','E1'],['meta.tif','lena.png','mandril3.jpg'],'첨부 파일 IFD와 uncompressed strip 샘플, RGB 전샘플 동일 비교.'),outside('I1-viewer',['E2'],['issue-6159-comments'],'2023-03-13 댓글의 앱별 차이 보고. 재현은 미실시.')],
  'unknowns':[{'status':'unknown','item':'당시 7.1.1-3/libtiff/delegate의 새 출력과 두 표시 앱의 역사적 재현','minimum_next_input':'버전·delegate·OS 기록이 있는 7.1.1-3 런타임, 당시 앱 버전, 회수 입력들. 위 명령 결과의 태그·샘플과 표시를 각각 비교한다.'}],
  'fixed_corpus_answer_status':'unknown','reachability_status':'unknown_not_assessed_by_this_reader',
  'reject_certainties':['4채널이므로 RGBA다.','meta 대신 alpha로 저장하면 원 의미가 보존된다.','-alpha off 하나로 모든 외부 viewer 표시가 고쳐진다.','같은 RGB 샘플이므로 ICC와 외관까지 항상 동일하다.']},
 {'case_id':'I2','original_request_source_id':'issue-6187','specified_version':'7.1.1-4','upstream_commit':'10ad43dc3e5113fa1969a55583a080c5a6a23f65','start_doc_id':'i7114_processing',
  'O_definition':'TIFF의 요청 대상 plane을 grayscale PNG로 추출한다. 선언된 alpha가 있으면 -alpha extract의 대상이 그것이다. 선언이 meta라면 먼저 대상 plane을 확인하고 구분하여 꺼낸다.',
  'P_definition':'요청자가 alpha라고 부른 공간별 plane 값을 흰색 상수로 대체하지 않고 유지한다. 그 plane이 TIFF상 alpha인지 unspecified extra인지도 정확히 설명한다.',
  'semantic_complete':True,'fixed_corpus_semantic_complete':False,'input_unresolved':False,'historical_runtime_complete':False,
  'correct_answer':{'disposition':'qualified_supported_with_semantic_correction','answer_ko':'회수한 demo.tif의 TIFF 선언은 RGB + unspecified extra sample이다(472×392, 8-bit×4, ExtraSamples=(0,)). 추가 plane은 0–255의 105개 값을 가진다. 7.1.1-4 reader는 이 경우 meta를 만들고 실제 alpha를 활성화하지 않는다. alpha가 없으면 accessor는 opaque를 반환하므로 -alpha extract가 흰 mask를 만드는 흐름과 부합한다. 이는 원하는 plane 데이터가 TIFF에서 없어졌다는 증거가 아니다. 값을 꺼내려면 확인된 meta plane을 직접 grayscale로 분리할 수 있다. 그것이 실제 의도한 transparency mask라는 전제에서 meta를 alpha로 복사한 뒤 -alpha extract를 적용하는 경로도 타당하다. 원 댓글의 성공 확인은 meta=>alpha에 대한 저자 보고이며 이 reader가 7.1.1-4에서 재현한 결과는 아니다. 이전 판에서 성공했다는 원 body만으로 새 판의 일반 alpha extraction 회귀를 확정하지 않는다.',
    'commands_unexecuted':[{'command':"magick demo.tif -channel-fx 'meta' extract.png",'preconditions':'7.1.1-4, 확인된 한 개 meta plane을 값 자체로 추출; alpha 의미를 강제로 부여하지 않는 분리 경로.','claim':'고정 ChannelFxImage의 단일채널 추출 및 grayscale 설정에 근거한 미실행 명령.'},{'command':"magick demo.tif -channel-fx 'meta=>alpha' -alpha extract extract.png",'preconditions':'7.1.1-4; TIFF unspecified plane이 사용자 의도상의 mask라는 전제.','claim':'meta=>alpha는 원 댓글에서 보고된 경로, 뒤의 alpha extract는 요청한 grayscale PNG를 위한 문서상 조합. 이 exact 조합의 역사적 실행은 미실시.'},{'command':'magick identify -verbose demo.tif','preconditions':'동일 고정 런타임','claim':'channel 표시 진단. TIFF tag와 sample 데이터 검사를 병행한다.'}]},
  'required_exceptions':[{'id':'E1','text':'extra sample이라는 사실이나 Photoshop의 Alpha1 이름만으로 TIFF transparency라고 판단하지 않는다. 원본의 ExtraSamples=0이 핵심 예외다.'},{'id':'E2','text':'alpha가 없는 상태의 흰 extract는 원래 meta plane이 흰색임을 뜻하지 않는다. -alpha set/opaque는 원값 복구가 아니다.'},{'id':'E3','text':'associated alpha 표지를 강제로 붙이면 RGB premultiplication 의미가 달라진다. associated와 unassociated를 임의 교환하지 않는다. 실제 opacity가 선언된 다른 입력에는 이 meta 전환을 무조건 적용하지 않는다.'}],
  'counter_input_provenance':{'type':'original_input_attachment','url':'https://github.com/ImageMagick/ImageMagick/files/11059385/demo.zip','archive_sha256':'cdcb7260ad3e4c46b3d89e0faf7f1cbe02b85b5c8bf53ce206de1c15677788a9','extracted_sha256':'79c2a9ccbf36de73a34b9090732cb19107fbc875b76e71020538073a72aac223','locally_inspected':True,'inspection':'input-inspection.json','original_body_only':'7.1.0-28/7.1.0에서 성공, 7.1.1-4에서 흰색이라는 보고; 원 body에 TIFF tag 없음.','later_layer':'현재 회수한 파일의 raw tag/sample과 후속 maintainer 설명·작성자의 성공 댓글은 별도 기준읽기 층.'},
  'minimal_supporting_intervals':[INTERVALS[x] for x in I2],
  'outside_corpus_requirements':[outside('I2-E-tiff-spec',['P','E1','E3'],['TIFF6'],'ExtraSamples와 premultiplication의 규격 정의.'),outside('I2-reader',['O','P','E1','E2'],['tiff-7.1.1-4.c','channel-7.1.1-4.c','pixel-accessor-7.1.1-4.h','composite-7.1.1-4.c'],'고정 reader1700–1737; ChannelFxImage240–465와 ExtractAlphaChannel1199–1204; GetPixelAlpha54–60; CompositeImage2451,2814–2817.'),outside('I2-input',['P','E1'],['demo.tif'],'원 파일 tag338=0과 비상수 네 번째 sample plane.'),outside('I2-followup',['E1'],['issue-6187-comments'],'해법 보고는 자연 원 body와 구분. 작성자의 meta=>alpha 성공 보고는 historical source-reported result.')],
  'unknowns':[{'status':'unknown','item':'원문의 두 역사적 런타임 비교와 exact grayscale PNG output equality','minimum_next_input':'7.1.0-28 및 7.1.1-4의 실행 가능 바이너리, delegate/quantum/OS 정보, 같은 SHA의 demo.tif. raw fourth plane과 추출 PNG의 8-bit 값·크기·방향을 비교한다.'}],
  'fixed_corpus_answer_status':'unknown','reachability_status':'unknown_not_assessed_by_this_reader',
  'reject_certainties':['-alpha extract만 있으면 어떤 4채널 TIFF의 네 번째 plane도 보존한다.','이전 버전에서 보였으므로 이 파일은 규격상 alpha다.','-define tiff:alpha=associated를 모든 파일에 적용하면 무해하다.','흰 PNG는 원 TIFF의 추가 데이터가 흰색 상수였다는 증거다.']},
 {'case_id':'I3','original_request_source_id':'issue-6237','specified_version':'7.1.1-6','upstream_commit':'b2dd67b1681e23d0e0b9769d81bed23f05129e2a','start_doc_id':'i7116_processing',
  'O_definition':'첨부 JP2의 codestream component와 색/채널 표지를 읽어 ImageMagick 영상 표현으로 디코딩한다.',
  'P_definition':'실제 RGB/gray/auxiliary/IR/opacity component의 값과 뜻을 유지한다. 네 성분이라는 개수에서 RGBA나 네 번째 alpha를 추정하지 않는다.',
  'semantic_complete':False,'fixed_corpus_semantic_complete':False,'input_unresolved':True,'historical_runtime_complete':False,
  'correct_answer':{'disposition':'justified_hold','answer_ko':'4 components는 component 개수이며 RGBA라는 정의가 아니다. JP2의 colr/ICC 색공간, cmap, cdef의 channel type/association과 codestream, 원 배포자의 band 의미를 같이 확인해야 한다. 후속 저자는 네 번째 채널이 near-IR라고 메타데이터를 보고했다고 썼으며 NRW의 공식 제품 이력 FAQ도 RGBI의 네 번째가 near-IR라는 제품군 설명을 제공한다. 그러나 이것은 현재 해당 JP2 파일을 직접 확인한 결과가 아니다. 원첨부 HTTP와 HTTPS, 원 배포 디렉터리가 모두 404라 원 바이트·실제 box 값을 확보하지 못했다. 고정 7.1.1-6 jp2.c는 OpenJPEG color_space==2이면 grayscale로 설정하고 component가 여러 개면 alpha를 켜며, numcomps>3이면 alpha를 켜고 component3을 alpha에 넣는다. 따라서 RGBI를 일반 RGBA처럼 취급할 구현상 위험이 확인된다. 하지만 어느 표지가 파일에서 왔고 어떤 원 plane이 실제로 보존·손실됐는지는 원본과 당시 delegate 없이 확정할 수 없다. 실제 색 손실이라고도, 올바른 grayscale 표현이라고도 단정하지 않고 입력 복원을 요청하는 것이 정당하다.',
    'commands_unexecuted':[{'command':'magick -version','preconditions':'7.1.1-6이 설치된 별도 재현 환경','claim':'버전과 quantum/delegate inventory를 기록한다.'},{'command':'magick identify -verbose dop10rgbi_32_280_5652_1_nw_2021.jp2','preconditions':'원본 JP2 바이트와 SHA가 회복되고 7.1.1-6/OpenJPEG 버전이 고정됨','claim':'ImageMagick의 해석 결과이며 원본 band 의미의 독립 증거가 아니다.'},{'command':'exiftool -G1 -a -s dop10rgbi_32_280_5652_1_nw_2021.jp2','preconditions':'ExifTool의 기록된 버전과 회복한 원본','claim':'색공간/채널/GeoJP2 메타데이터 확인; 출력이 cdef/cmap 원시값을 생략하면 해당 JP2 box dump를 추가로 요구한다.'},{'command':'opj_dump -i dop10rgbi_32_280_5652_1_nw_2021.jp2','preconditions':'기록된 OpenJPEG 버전과 원본','claim':'codestream component·정밀도·geometry 정보를 수집; 이것만으로 publisher의 IR 의미를 확정하지 않는다.'}]},
  'required_exceptions':[{'id':'E1','text':'JP2 ihdr NC, colr, cmap, cdef는 서로 다른 역할이다. 네 component와 Grayscale 보고의 병존은 헤더/채널 정의를 확인할 필요를 뜻하며 어느 한 보고를 버릴 근거가 아니다.'},{'id':'E2','text':'RGBI의 I는 제품군에서 near-IR일 수 있다. 그 경우 transparency로 소비하면 채널 의미 보존에 실패한다. 제품군 설명만으로 정확한 이 파일의 바이트를 검증하지 않는다.'},{'id':'E3','text':'고정 reader의 component 수 휴리스틱이 실제 cdef/auxiliary 뜻을 보존한다는 보장이 없다. 색공간을 나중에 sRGB로 바꾸는 명령이 이미 합쳐지거나 빠진 원 plane을 복구한다고 단정하지 않는다.'},{'id':'E4','text':'원본 파일·정확한 delegate·기준 decode가 없으므로 역사적 runtime과 실제 색 손실은 unknown이다. 불가능의 증명으로 바꾸지 않는다.'}],
  'counter_input_provenance':{'type':'original_file_with_conflicting_reported_metadata','original_url':'http://www.fmwconcepts.com/misc_tests/dop10rgbi_32_280_5652_1_nw_2021.jp2.zip','locally_inspected':False,'capture_attempts':[{'url':'http://www.fmwconcepts.com/misc_tests/dop10rgbi_32_280_5652_1_nw_2021.jp2.zip','status':404,'receipt':'attachments/i3.jp2.zip.receipt.json'},{'url':'https://www.fmwconcepts.com/misc_tests/dop10rgbi_32_280_5652_1_nw_2021.jp2.zip','status':404,'receipt':'attachments/i3-https.jp2.zip.receipt.json'},{'url':'https://www.opengeodata.nrw.de/produkte/geobasis/lusat/dop/dop_jp2_f10/','status':404,'receipt':'snapshots/nrw-directory.html.receipt.json'}],'original_body_only':'gray+alpha, 4 components, Grayscale은 원저자 도구 출력 보고; 색 기대와 RGBA 추론도 원저자가 불확실하다고 했다.','later_layer':'near-IR 주장과 Pillow/Photoshop/GIMP/GraphicConverter 관찰은 후속 댓글의 주장. 해당 앱을 직접 실행하거나 원본을 열었다고 세지 않는다.'},
  'minimal_supporting_intervals':[INTERVALS[x] for x in I3],
  'outside_corpus_requirements':[outside('I3-JP2-standard',['O','P','E1'],['T800-2015'],'ITU-T T.800 (11/2015), PDF155–159,162–164: ihdr NC, colr EnumCS 16/17/18, cmap, cdef type/association 및 auxiliary channel 요건.'),outside('I3-reader',['O','P','E3'],['jp2-7.1.1-6.c','openjpeg-2.5.0.h'],'fixed jp2.c429–446,511–545의 선택·매핑. OpenJPEG2.5.0 header의 enum값은 설명용이며 원저자의 실제 linked OpenJPEG 버전은 미확인.'),outside('I3-product-context',['P','E2'],['issue-6237-comments','NRW-history-faq'],'NRW FAQ p7 제품군 RGBI/near-IR 설명과 저자의 후속 주장. exact tile 파일 증명은 아니다.'),outside('I3-original-bytes',['P','E1','E2','E4'],[],'동일 원본의 모든 JP2 header box와 codestream, band별 독립 기준 decode 및 publisher metadata. 현재 회수하지 못함.',False)],
  'unknowns':[{'status':'unknown','item':'이 JP2의 실제 색/채널 의미 및 고정 런타임에서의 보존 여부','minimum_next_input':'원첨부의 바이트 또는 동일성이 입증된 원배포본(SHA-256 포함); ihdr/colr/cmap/cdef 및 codestream header dump; 해당 tile/2021 배포본의 band 정의; 7.1.1-6의 linked OpenJPEG 버전과 독립 component decode. 4번째 plane의 IR/opacity 의미를 확인하기 전 RGBA 처방을 하지 않는다.'}],
  'fixed_corpus_answer_status':'unknown','reachability_status':'unknown_not_assessed_by_this_reader',
  'reject_certainties':['4 components이므로 RGBA다.','Grayscale이라고 표시됐으니 원파일에 실제 색 데이터가 없다.','RGBA로 강제 변환하면 IR까지 보존된다.','-colorspace sRGB를 추가하면 원래 색을 복구한다.','입력을 구하지 못했으므로 원 소프트웨어에서 불가능하다.']}
]

WORKS={
 'im-manual':{'allocation':'definition','counted_source':'i7113_command-line-options','author':'ImageMagick Studio LLC / project contributors','cases':['I1','I2','I3'],'independence':'모든 www 문서 페이지와 -3/-4/-6 버전을 한 매뉴얼 저작으로 통합.'},
 'tiff6':{'allocation':'definition','counted_source':'TIFF6.pdf','author':'Aldus Corporation, TIFF 6.0 specification; ITU public standards copy','cases':['I1','I2'],'independence':'TIFF 자체의 ExtraSamples 규격; ImageMagick 매뉴얼과 별도 저작.'},
 't800-2015':{'allocation':'definition','counted_source':'T800-2015.pdf','author':'ITU-T / ISO/IEC','cases':['I3'],'independence':'JPEG 2000 core file/channel 규격; TIFF·PNG·IM 문서와 별도 저작.'},
 'png-2003':{'allocation':'definition','counted_source':'PNG-2003.html','author':'W3C, ISO/IEC JTC1 SC24 and PNG Group; editor David Duce','cases':['I2','SUPPLEMENT'],'independence':'PNG의 alpha와 ICC/색공간을 별도로 정의한 규격 저작.'},
 'im-discussion-6299':{'allocation':'regression','counted_source':'discussion-6299.html','author':'indexofrefraction; replies snibgo','cases':['I2','SUPPLEMENT'],'independence':'2023-05-06, 독립 저자와 별도 64×64 LZW icon_0078 입력. #6187 demo와 기전은 유사하나 새로운 fix라고 세지 않고 별도 counter-input 저작 1로만 배당.'},
 'im-discussion-7848':{'allocation':'regression','counted_source':'discussion-7848.html','author':'bohemima; maintainer dlemstra and fmw42','cases':['I2','SUPPLEMENT'],'independence':'2024-12-20, 7.1.1-40→41의 별도 sample_info 회귀. 공개 Car 입력은 associated alpha. 댓글·첨부·maintainer patch 설명 모두 1개 lineage.'},
 'im-issue-8022':{'allocation':'regression','counted_source':'issue-8022.json','author':'ferdnyc; replies fmw42 and jonnyawsom3','cases':['I1','I2','SUPPLEMENT'],'independence':'2025-03-11, JXL alpha 제거와 ICC 보존이 갈라진 별도 사례. libjxl#4164를 별도 저작으로 세지 않고 같은 이슈 lineage에 포함.'},
}

META={
 'TIFF6.pdf':('tiff6','1992-06-03 / TIFF 6.0','ExtraSamples 0/1/2, associated alpha와 RGB premultiplication을 규격에서 확인.','규격은 원파일 태그나 특정 viewer 구현을 증명하지 않는다.'),
 'T800-2015.pdf':('t800-2015','ITU-T T.800 (11/2015) / ISO/IEC15444-1:2016','NC는 성분 수; colr와 cdef/cmap가 색공간·의미를 정의. auxiliary channels에는 complete cdef 요구.','읽은 범위는 JP2 core 규격. 원 I3 파일과 실제 linked delegate는 unavailable.'),
 'PNG-2003.html':('png-2003','2003-11-10 Second Edition','PNG alpha는 별도 sample/opacity이며 ICC는 iCCP의 색 해석 정보; gamma를 alpha에 적용하지 않는다.','원 I2 extraction 출력과 역사적 런타임 재현은 하지 않았다.'),
 'discussion-6299.html':('im-discussion-6299','2023-05-06 to 2023-05-08; IM7.1.1-8','별도 alpha extract 흰색 보고, meta0 분리/승격 해법과 저자 수용.','독립된 입력 사례이지만 #6187과 같은 extra sample 의미 문제. 새 regression fix 수를 늘리지 않는다.'),
 'discussion-7848.html':('im-discussion-7848','2024-12-20 to 2024-12-21; IM7.1.1-40/41','srgba 표지가 유지돼도 실제 alpha가 opaque가 되는 별개 회귀 보고와 maintainer 수정 설명.','역사적 실행은 source-reported. 15ec380 short SHA API 조회는422라 fix code를 직접 검증했다고 주장하지 않는다.'),
 'issue-8022.json':('im-issue-8022','2025-03-11; IM7.1.1-44 / libjxl0.10.4','alpha 제거 뒤 ICC가 9080→536 bytes 및 description/intent가 바뀌었다는 원저자의 입출력 기록.','소스 보고. 본 런타임에는 JXL delegate가 없어 원 JXL ICC를 독립 디코드하지 못했다.'),
 'issue-8022-comments.json':('im-issue-8022','2025-03-11 to 2025-03-30; IM7.1.1-45 reports','시각상 차이가 눈에 띄지 않는 경우도 profile 동일성 보존을 뜻하지 않는다는 논의.','추측성 원인 설명을 확정 사실로 승격하지 않음; 같은 lineage, 추가 카운트 없음.'),
 'openjpeg-2.5.0.h':('openjpeg-implementation','v2.5.0','OPJ_CLRSPC_GRAY=2와 별도 component.alpha 필드를 확인.','설명용 고정 API 코드. 원저자의 실제 OpenJPEG 버전은 알려지지 않았다.'),
 'NRW-history-faq.pdf':('nrw-product-faq','2024-03-21 Last-Modified; historical product table','p7 표·각주: 2010부터 네 번째 near-IR; 2019 이후 TrueDOP의 RGBI 제품군.','특정 dop10rgbi_32_280_5652_1_nw_2021.jp2의 바이트·header 값·정상 색 기준이 아니다.'),
}

ATTACHMENT_INFO={
 'meta.tif.zip':('im-issue-6159',['I1'],'original output archive; current bounded recovery'),
 'meta.tif':('im-issue-6159',['I1'],'ExtraSamples=0; raw RGB exactly equal to lena; extra range3–220'),
 'lena.png':('im-issue-6159',['I1'],'RGB256×256, no embedded ICC in inspected Pillow info; RGB reference array'),
 'mandril3.jpg':('im-issue-6159',['I1'],'RGB256×256 source to grayscale; historical grayscale conversion not run'),
 'demo.zip':('im-issue-6187',['I2'],'original input archive; bounded recovery'),
 'demo.tif':('im-issue-6187',['I2'],'ExtraSamples=0; raw fourth plane0–255,105 distinct values'),
 'icon_0078.tif.zip':('im-discussion-6299',['I2','SUPPLEMENT'],'independent input archive'),
 'icon_0078.tif':('im-discussion-6299',['I2','SUPPLEMENT'],'64×64,LZW,ExtraSamples=0; tags inspected, raw compressed plane not independently decoded'),
 'CarTransparentBackground.zip':('im-discussion-7848',['I2','SUPPLEMENT'],'public maintainer attachment of regression input'),
 'CarTransparentBackground.tif':('im-discussion-7848',['I2','SUPPLEMENT'],'1000×750 uncompressed,ExtraSamples=1; raw alpha0–255,256 distinct values'),
 'f42-01-day.zip':('im-issue-8022',['I1','I2','SUPPLEMENT'],'public JXL input ZIP, bounded recovery'),
 'f42-01-day.jxl':('im-issue-8022',['I1','I2','SUPPLEMENT'],'ZIP entry/signature inspected only; ICC and alpha values remain source-reported'),
}
EXTRACT_PARENT={'meta.tif':'meta.tif.zip','demo.tif':'demo.zip','icon_0078.tif':'icon_0078.tif.zip','CarTransparentBackground.tif':'CarTransparentBackground.zip','f42-01-day.jxl':'f42-01-day.zip'}

def evidence_path(name):
 if name in DOCS:return ROOT/DOCS[name]['source_file']
 if name.startswith('issue-') and name.split('-')[-1].isdigit():return BASE/'snapshots'/(name+'.json')
 for d in ['snapshots','attachments','attachments/extracted','supplementary-constructed']:
  p=BASE/d/name
  if p.exists():return p
 raise FileNotFoundError(name)

def ledger():
 groups=defaultdict(list)
 for e in EVENTS:groups[e['source']].append(e)
 rows=[]
 for name,events in sorted(groups.items()):
  path=evidence_path(name);original=None;arrived=None;redaction=None;receipt=None
  if name in DOCS:
   d=DOCS[name];original=d['url'];arrived=d['observed_source_arrival_url'];version=d['version'];work='im-manual';author='ImageMagick Studio LLC / contributors';confirmed='고정 매뉴얼의 기록된 부분을 직접 읽음. 해당 옵션·채널·형식의 일반 설명.';limits='매뉴얼 설명만으로 원 입력의 태그·samples·역사적 실행은 증명되지 않는다.';cases=['I1'] if name.startswith('i7113_') else ['I2'] if name.startswith('i7114_') else ['I3'];sha=d['source_sha'];source_fixed=d['upstream_source_url'];commit=d['upstream_commit']
  else:
   source_fixed=None;commit=None;sha=hashlib.sha256(path.read_bytes()).hexdigest()
   parent=EXTRACT_PARENT.get(name)
   rp=(BASE/'attachments'/parent).with_name(parent+'.receipt.json') if parent else path.with_name(path.name+'.receipt.json')
   if rp.exists():receipt=json.loads(rp.read_text());original=receipt['original_url'];arrived=receipt.get('arrived_url');redaction=receipt.get('arrived_url_redaction')
   if name in META:
    work,version,confirmed,limits=META[name];info=WORKS.get(work,{});cases=info.get('cases',['I3']);author=info.get('author','OpenJPEG project' if work=='openjpeg-implementation' else 'Bezirksregierung Köln / Geobasis NRW')
   elif name in ATTACHMENT_INFO:
    work,cases,confirmed=ATTACHMENT_INFO[name];version='current recovery of original public attachment';author=WORKS.get(work,{}).get('author','fmw42' if work.endswith('6159') else 'gursch');limits='후속 gold layer의 로컬 파일 검사. 원 body/저자 도구출력 또는 historical ImageMagick run과 구분.'
   elif name.startswith('issue-'):
    number=int(name.split('-')[1].split('.')[0]);work='im-issue-'+str(number);cases=[{6159:'I1',6187:'I2',6237:'I3'}[number]];author='fmw42' if number in [6159,6237] else 'gursch';version={6159:'2023-03-13;7.1.1-3',6187:'2023-03-24;7.1.1-4',6237:'2023-04-06;7.1.1-6'}[number];confirmed='원 body의 요청과 불확실성' if 'comments' not in name else '원 issue의 후속 공개 댓글';limits='현재 공개 body/comments snapshot. 최초 게시 순간의 원문을 복원했다는 주장 없음. 댓글은 원 body 모집 뒤 별도 층.'
   elif name.endswith(('.c','.h')):
    work='imagemagick-implementation';version='7.1.1-3' if '-3.' in name else '7.1.1-4' if '-4.' in name else '7.1.1-6';author='ImageMagick project contributors';cases=['I1'] if version.endswith('-3') else ['I2'] if version.endswith('-4') else ['I3'];confirmed='기록된 함수/분기의 고정판 소스코드를 직접 읽음.';limits='정적 코드 근거. 당시 binary/delegate/OS 조합의 실행이 아님.';source_fixed=original;commit={'7.1.1-3':'c5d5e7117fb07096158bcad05e1086f0c2fff172','7.1.1-4':'10ad43dc3e5113fa1969a55583a080c5a6a23f65','7.1.1-6':'b2dd67b1681e23d0e0b9769d81bed23f05129e2a'}[version]
   else:
    work='constructed-alpha-icc';version='local ImageMagick7.1.1-43 Q16,2026-11-24';author='independent gold reader (constructed input)';cases=['SUPPLEMENT'];confirmed='분리된 두 bool: alpha sample 동일성, embedded ICC byte 동일성.';limits='자연 요청·공개 1차 저작 quota·고정판 실행으로 세지 않는다. 색의 지각 차이를 입증한 것은 아니다.'
  wi=WORKS.get(work,{})
  allocation=wi.get('allocation','additional')
  unique=wi.get('counted_source')==name
  row={'source_id':srcid(name),'original_url':original,'arrived_url':arrived,'arrived_url_redaction':redaction,'fixed_source_url':source_fixed,'source_sha256':sha,'snapshot_path':str(path.relative_to(BASE)) if BASE in path.parents else str(path.relative_to(ROOT)),'work_id':work,'lineage':work,'author':author,'version_date':version,'upstream_commit':commit,'checked_utc':events[-1]['read_utc'],'read_utc':[e['read_utc'] for e in events],'read_sections':[{'read_utc':e['read_utc'],'sections':e['read_sections'],'display_truncated_batch':e.get('display_truncated_batch',False),'qualification':e.get('qualification')} for e in events],'confirmed':confirmed,'limits':limits,'counter_observation':confirmed if allocation=='regression' or work=='constructed-alpha-icc' else None,'unknown':'historical runtime unexecuted; other qualifications in limits','questions':['Q2','Q5','Q6','Q7'],'case_rows':cases,'allocation':allocation,'unique_counted':unique,'independence_basis':wi.get('independence','동일 원요청/구현 lineage의 보조 근거; quota 고유 저작 추가 없음.'),'primary':work!='constructed-alpha-icc','status':'read_with_qualified_limits','download_is_read':False}
  if receipt is not None:
   row['fetched_sha256']=receipt.get('sha256')
   row['snapshot_redaction']=receipt.get('snapshot_redaction')
  if name.startswith('issue-') and 'comments' not in name and name in ['issue-6159','issue-6187','issue-6237']:row['natural_request_already_allocated']=True
  rows.append(row)
 return rows

def main():
 rows=ledger();counts=Counter(r['allocation'] for r in rows if r['unique_counted']);assert counts=={'definition':4,'regression':3}
 assert len({r['work_id'] for r in rows if r['unique_counted']})==7
 for case in CASES:
  issue=json.loads((BASE/'snapshots'/(case['original_request_source_id']+'.json')).read_text())
  case['original_issue_url']=issue['html_url']
  case['original_body_sha256']=hashlib.sha256(issue['body'].encode()).hexdigest()
 CASES[1]['input_unresolved_scope']='원 파일 바이트·TIFF tag·sample 값은 확인됨. unspecified plane의 제작자 의도와 RGB premultiplication은 태그만으로 확정하지 않으며 조건부로 남긴다.'
 gold={'schema':1,'created_utc':now(),'project':'AF-RES-116','reader':'/root/gold_imagemagick independent reference reader','status':'PARTIAL_INPUT_AND_HISTORICAL_RUNTIME_GAPS','language':'ko','seals':{'natural_requests':'seal878f2e1b8d053f6eea4e3473d5b467ca98476a01','corpus':'seal27bdf61aac1c24299401879749fcbca1ce43e8a4','packets':'seal762fe1fc57b3b5f765f9d13537fa9c15b71b5b80'},'blindness':{'authoring_read':False,'packets_read':False,'inputs_directory_read':False,'readers_read':False,'recipient_trails_answers_read':False,'other_gold_read':False,'hints_read':False,'boundary':'공유 파일시스템의 절차적 가림. OS 격리 주장 없음.'},'semantic_complete_meaning':'필수 예외가 포함된 한정 reference answer의 내용이 정해졌는지. historical 실행 성공이나 corpus-only/3개봉 지원과 별개다.','limitations':COMMON_LIMITS,'cases':CASES,'work_allocation':{'counts':dict(counts),'natural_requests_already_allocated':3,'unique_works':WORKS,'source_rows':len(rows)},'supplementary':{'natural_case':False,'contribution_to_natural_success_denominator':False,'alpha_and_colorprofile_counterexample':{'public_primary_case':'issue-8022','public_case_claim':'alpha 제거 조작이 성공해도 원 ICC 보존이 성립하지 않는 source-reported counterexample.','constructed_bidirectional_check':CONSTRUCTED,'result':'같은 비상수 alpha/ICC 입력에서 -strip은 alpha를 보존하고 ICC를 제거; -alpha off는 ICC bytes를 보존하고 alpha를 모두 opaque로 바꿈. 한 보존 bool로 다른 bool을 추론할 수 없다.','corpus_intervals':[INTERVALS[x] for x in S],'qualification':'독립 만든 보조 입력, 7.1.1-43에서만 실행. 자연 사례·고정 버전 검증·추가 공개 저작으로 세지 않는다.'},'additional_regression_conclusions':[{'source_id':'discussion-6299','result':'다른 unspecified extra 입력에서도 alpha extract 흰색이 보고됨. 이는 metadata/plane 확인이 필요한 독립 counter-input이며 새 fix로 세지 않음.'},{'source_id':'discussion-7848','result':'실제 associated alpha 입력에서는 후기 별개 reader 회귀가 보고됨. 현재 입력 태그/비상수 raw alpha는 독립 확인. srgba 채널 이름만으로 실제값 보존을 확인할 수 없음.','historical_runtime':'unknown/source-reported only'}]}}
 row_by_id={r['source_id']:r for r in rows}
 external=[
  ('REF-TIFF338','TIFF6',['I1','I2'],['P','E1','E3'],{'pdf_pages_1based':[31,32],'section':'ExtraSamples, tag338'},'0/1/2 의미; 4 samples만으로 alpha를 판단하지 않음'),
  ('REF-TIFF-associated','TIFF6',['I1','I2'],['E3'],{'pdf_pages_1based':[77],'section':'Section18, associated alpha representation'},'RGB premultiplication 요건'),
  ('REF-I1-reader','tiff-7.1.1-3.c',['I1'],['P','E1'],{'lines_1based':[1700,1737],'function':'ReadTIFFImage'},'unspecified extra를 meta로, alpha 표지일 때 alpha로 읽는 분기'),
  ('REF-I1-writer','tiff-7.1.1-3.c',['I1'],['O','P','E1'],{'lines_1based':[3622,3655],'function':'WriteTIFFImage'},'alpha_trait와 meta_count에 따른 extra sample 배열'),
  ('REF-I2-reader','tiff-7.1.1-4.c',['I2'],['P','E1'],{'lines_1based':[1700,1737],'function':'ReadTIFFImage'},'수신된 태그가0인 경우 actual alpha를 만들지 않는 분기'),
  ('REF-I2-fx','channel-7.1.1-4.c',['I2'],['O','P'],{'lines_1based_ranges':[[240,244],[314,320],[353,361],[393,411],[461,465]],'function':'ChannelFxImage'},'clone/source 채널 검사/destination alpha·meta 할당/단일채널 grayscale 처리; 이 조각들을 직접 읽었으며 사이의 전체 범위를 읽었다고 주장하지 않음'),
  ('REF-I2-extract','channel-7.1.1-4.c',['I2'],['O','E2'],{'lines_1based':[1199,1204],'function':'SetImageAlphaChannel, ExtractAlphaChannel'},'AlphaCompositeOp 실행 후 alpha_trait 해제'),
  ('REF-I2-opaque-default','pixel-accessor-7.1.1-4.h',['I2'],['E2'],{'lines_1based':[54,60],'function':'GetPixelAlpha'},'undefined alpha trait이면 OpaqueAlpha 반환'),
  ('REF-I2-alpha-composite','composite-7.1.1-4.c',['I2'],['O','E2'],{'lines_1based_ranges':[[2451,2452],[2814,2817]],'function':'CompositeImage'},'normalized source alpha를 color output 값으로 사용'),
  ('REF-JP2-NC-colr','T800-2015',['I3'],['O','P','E1'],{'pdf_pages_1based':[155,158,159],'sections':['I.5.3.1 NC','I.5.3.3 colr','TableI.9–I.10']},'성분 개수와 색공간 선언을 구분'),
  ('REF-JP2-cdef','T800-2015',['I3'],['P','E1','E2'],{'pdf_pages_1based':[162,163,164],'section':'I.5.3.6 channel definition; tablesI.16–I.19'},'channel type/association, opacity/unspecified, auxiliary channels의 complete cdef 요건'),
  ('REF-I3-coder','jp2-7.1.1-6.c',['I3'],['O','P','E3'],{'lines_1based_ranges':[[429,446],[511,545]],'function':'ReadJP2Image'},'gray colorspace 및 numcomps 휴리스틱; component3→alpha'),
  ('REF-I3-openjpeg-types','openjpeg-2.5.0.h',['I3'],['E3'],{'lines_1based_ranges':[[316,323],[700,704]],'symbols':['OPJ_COLOR_SPACE','opj_image_comp_t.alpha']},'API enum2=GRAY와 component alpha 필드. 이 tag가 원 binary의 delegate 버전이라는 뜻은 아님'),
  ('REF-I3-NRW','NRW-history-faq',['I3'],['P','E2'],{'pdf_pages_1based':[7],'section':'question5 historical product table and footnote3'},'제품군 RGBI의 네 번째 near-IR; 특정 원파일 판정으로는 부족'),
  ('REF-PNG-independence','PNG-2003',['I2','SUPPLEMENT'],['P_alpha','P_profile'],{'sections':['4.2','6.2','11.3.3.3'],'derived_text_intervals':[[30300,31150],[54504,56400],[81454,84300]]},'alpha와 iCCP 색 해석은 서로 다른 정보')
 ]
 gold['outside_corpus_minimal_intervals']=[{'interval_id':iid,'source_id':sid,'case_rows':cases,'conditionIDs':conditions,'inside_corpus':False,'location':loc,'source_sha256':row_by_id[sid]['source_sha256'],'version_date':row_by_id[sid]['version_date'],'sufficiency':'이 조건의 일반 정의/정적 구현 근거; 특정 입력 및 historical 실행의 대체물 아님','qualification_ko':why} for iid,sid,cases,conditions,loc,why in external]
 (BASE/'gold.json').write_text(json.dumps(gold,ensure_ascii=False,indent=2)+'\n')
 (BASE/'sources-imagemagick.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
 (BASE/'minimal-intervals.json').write_text(json.dumps(list(INTERVALS.values()),ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'gold_cases':len(CASES),'intervals':len(INTERVALS),'source_rows':len(rows),'unique_allocation':dict(counts),'created_utc':gold['created_utc']},ensure_ascii=False))
if __name__=='__main__':main()
