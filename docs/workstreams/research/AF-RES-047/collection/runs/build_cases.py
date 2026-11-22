import json,csv,pathlib,datetime
P=pathlib.Path(__file__).parent
CPM='https://zenodo.org/records/8095888'
CPMZIP='https://zenodo.org/api/records/8095888/files/rocrate.zip/content'
CPMOLD='https://zenodo.org/api/records/7676924/files/rocrate.zip/content'
WET='https://zenodo.org/records/12622362'
WETZIP='https://zenodo.org/api/records/12622362/files/wetlab2variations_full.zip/content'
CAM='https://camelyon-dataset.s3.us-west-2.amazonaws.com/CAMELYON16/'
GIAB='https://ftp-trace.ncbi.nlm.nih.gov/giab/ftp/data/NA12878/NIST_NA12878_HG001_HiSeq_300x/'
R1='140407_D00360_0017_BH947YADXX/Project_RM8398/Sample_U5c/U5c_CCGTCC_L001_R1_001.fastq.gz'
WP='https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0309210'
REPO='https://raw.githubusercontent.com/ResearchObject/workflow-run-crate/89025e50dbef6960c3b3e56b15eb04cd033b888c/docs/examples/WfExS-backend/Wetlab2Variations_CWL_provenance/ro-crate-metadata.json'
def view(urls,evidence,new,judgment,p=False,u=False,r=False,rr=False,v=False,value=None):
 return dict(visible_urls=urls,evidence=evidence,new_fact=new,judgment=judgment,publisher_exists=p,specific_usage=u,run_link=r,record_run_link=rr,value_checked=v,visible_value=value)
cases=[dict(
 case_id='RUN01',layer='실행 기록 우선 보강층',analysis_title='CPM RO-Crate carcinoma classifier execution (Camelyon16 fragment)',
 consumer_url=CPM,consumer_locator='Description of the AI pipeline; archive predictions.h5:/test/test_001/table; logical non_index_axes order; first row',
 purpose='원 기술문은 prostate carcinoma 검출 학습/평가를 표방하지만 실제 입력은 Camelyon16이다. 작은 공개 fragment를 사용한 응용 실행이며 임상 효능 주장으로 확장하지 않는다.',
 target_time='원 test 2023-02-24 13:13:41–13:14:58(로그 timezone 미기재); 원 preprocess v1=02-24 13:11:14, v1.1에 보관된 preprocess=03-16 13:05:48',
 input_name='CAMELYON16 test_001.tif/test_001.xml → derived cam16_mrxs.h5',field='coord_x: predictions.h5 /test/test_001/table first logical data column, first row; y=4096, slide=test_001',reported_value=63488,unit='원본 WSI 좌표계의 patch 왼쪽 위 x pixel; polygon vertex 아님',
 publisher_url=CAM+'README.md',publisher_locator='Images; Annotations; Notes about the data; checksums.md5 annotations/test_001.xml; publisher XML coordinates',
 publisher_edition='GigaDB10.5524/100439 (2018 supporting snapshot); Radboud S3 CAMELYON16 file set Last-Modified2022-09-28',
 publisher_value='미확인: publisher polygon vertex와 소비 patch origin은 행/변환이 다르다. Publisher XML은30 polygons/4672 vertices; publisher MD5=59279f7dc2b6dd4a741904aca621501a.',
 usage_edition='소비자 RO-Crate v1 DOI7676924 및 v1.1 DOI8095888의 구체 member 이름; 원 CAMELYON 발행판은 미확인',
 usage_evidence='ro-crate-metadata.json: CreateAction object wsi/test/→hasPart test_001.tif/.xml; test object cam16_mrxs.h5; 원 test.log eid와 입력 table hash. 구체 local input 선언은 보존하되 원 발행판 동일성을 뜻하지 않는다.',
 run_id='test_script:ROCRATE-PUB-1438b57a750ce887d4433d9e; preprocess v1 9bdc1af0-53cf-4c3f-8c88-42f004b1f824; v1.1 ff67ce65-736f-46d5-9fec-10953cad8695 (각 별도 기록)',
 run_input_evidence='원 test.log splits.test_gen.table_0_sha256=c9015456f94b60a69b608715d80fdcea91d1e8f832742b5762bc11fe979c1d4b. 이 값은 pandas 표+metadata hash로 파일 byte hash가 아니다. v1.1 preprocess가 test 뒤여서 같은 실행으로 합칠 수 없다.',
 publisher_exists=True,specific_usage=True,specific_usage_scope='구체 보관 local file 사용 선언; 독립 원 발행판 특정은 미확인',run_link=False,record_run_link=True,local_run_link=True,publisher_bytes_match=False,value_checked=False,candidate_value_checked=False,strict_positive=False,
 current_correction='publisher README는 normal_86→tumor_111(오분류)와 test_049 제거(중복)를 명시한다. 선택 test_001 patch 값의 후속 발행판 정정은 미확인. 소비 archive v1→v1.1은 predictions.h5/원 test.log가 같은 bytes인데 preprocess ID/날짜 및 derived HDF5가 바뀐다.',
 missing_reason='원 자료 발행판→소비 XML/WSI byte 연결 및 원 preprocess→test 입력 table hash 전체 재계산 미확인. publisher XML과 소비 XML은bytes/좌표 정밀도/annotation 이름이 다르다. 최고 해상도 TIF 기반 patch 필터 재실행을 하지 않았다.',
 strongest_claim='공개된 두 소비 archive는 같은 예측 파일과 원 test 로그를 보관한다. 기록상 local 입력과 실행 ID 연결은 있으며, 원 발행판과 해당 patch 필드의 진본 사용은 독립 확인되지 않았다.',
 consumer_first_opened_utc='2026-11-22T22:06:25.769414+00:00',publisher_first_opened_utc='2026-11-22T22:16:04.096917+00:00',publisher_first_success_utc='2026-11-22T22:19:36.427668+00:00',
 source_ids=['R-FR-ZEN-7676923','R-ARCHIVE-cpm-small','R-ARCHIVE-cpm-v1','R-ARCHIVE-cpm-config','R-CPM-EDITIONS','R-CAM-PAPER','R-CAM-README','R-CAM-XML','R-CAM-MD5','R-CPM-CODE-1','R-CPM-CODE-2','R-CPM-CODE-3'],
 A=view([CPM,WP+'#sec013','https://gigadb.org/dataset/100439'],'소비 보고의 목적·Camelyon16 인용·결과 객체명만. 실행 graph/log/HDF5 내부는 이 구성에 포함하지 않는다.','입력 자료 이름과 분석 목적. 실제 파일판·실행 입력 연결은 아직 보이지 않음.','보류: 인용으로 실제 사용판을 특정할 수 없음'),
 B=view([CPM,CAM+'README.md',CAM+'checksums.md5',CAM+'annotations/test_001.xml','https://pmc.ncbi.nlm.nih.gov/articles/PMC6007545/'],'A + publisher 원문/파일/MD5. 실제 publisher XML MD5를 계산해 checksum list와 대조.','B−A: breast-cancer lymph node 자료라는 목적 조건, publisher file 객체와 정정문 존재. 원문 prostate 기술과 어긋남.','자료 목적 설명은 정정; 과거 사용판·patch값은 보류',p=True),
 C=view([CPM,CAM+'annotations/test_001.xml',CPMZIP+'#ro-crate-metadata.json',CPMZIP+'#predictions.h5',CPMZIP+'#prov_test.log',CPMZIP+'#prov_preprocess.log',CPMOLD+'#prov_preprocess.log'],'B + 같은 archive의 graph,log,configuration,HDF5 field. v1/v1.1은 별도 실행 기록으로 비교하고 다른 UUID를 합치지 않는다.','C−B: 구체 local file 사용 선언과 실행 ID, coord_x63488, 동일 prediction bytes/변경 preprocess 계보. C의 선언·값은 기록 재독.','보류: 선언/지역 실행은 관측; 원 publisher input 판과 해당 필드까지 strict V는 미확인',p=True,u=True,rr=True,value=63488),
 alternate_fields=[dict(field='is_cancer',value=False,location='first data row at x63488,y4096; alternative field only'),dict(field='pred',value=0.0003975369909312576,location='same row; alternative field only'),dict(field='Binary Accuracy',value=0.8773646444879322,location='prov_test.log evaluations.a0b620...; alternative metric, no publisher ground truth rerun')],
 selection_limit='기간 내 frame 5위. 방법 시연이라는 단어로 제외하지 않고 외부 실제 영상에 적용한 실행으로 포함. 향후 더 이른 적격 원문이 나오면 최초2 판정 재검토.'
),dict(
 case_id='RUN02',layer='실행 기록 우선 보강층',analysis_title='WfExS Wetlab2Variations NA12878 variant-calling execution',
 consumer_url=WET,consumer_locator='archive ro-crate-metadata.json actual CreateAction; outputs/_1693335046/abc2.sorted.md.realigned.bqsr.vcf.gz header #CHROM and first nonheader record',
 purpose='NIST GIAB NA12878 paired FASTQ와 hs37d5 reference/known variant resources로 chromosome1 gVCF를 생성한다. 표본 생산자는 NIST, 재사용 실행 기록 작성자는 José M. Fernández이다.',
 target_time='2023-08-29T18:50:46.906382+00:00–20:40:48.384424+00:00; 입력 path의 flowcell 140407_D00360_0017_BH947YADXX, publisher file Last-Modified2014-09-18',
 input_name='U5c_CCGTCC_L001_R1_001.fastq.gz in full NIST flow-cell path',field='CHROM: first VCF record (POS1, END63267, DP0)',reported_value='1',unit='염색체 identifier; 관측 read count나 정확도 아님',
 publisher_url=GIAB+R1,publisher_locator='directory file name; HG001-part2.md5 exact full flow-cell path; HTTP range0–65535 first FASTQ record',
 publisher_edition='NIST HG001 HiSeq300x, full flow-cell/library/R1 object; publisher MD5 52f3ed344d88278c703faa1280818ce1; Content-Length413005346',
 publisher_value='미확인: raw FASTQ에는 VCF CHROM 필드가 없다. 첫20 FASTQ records는 소비 gzip과 일치하나 전체 파일/선택 CHROM값 독립 재현은 아님.',
 usage_edition='archive local inputs/U5c_CCGTCC_L001_R1_001.fastq.gz; contentUrl=NIST exact path, sha256=4cd8ae63bb5fb67e714c3182bb3035df9d0e83edd26cc51d4439cd44c3015316, size487611787(작성자 선언)',
 usage_evidence='Zenodo archive graph action#bdfcc6a4-3bf4-4fd7-9e8c-cc6b0deaa43d object Collection#dcc0e6bb-4888-4bee-bc06-e995b5d18538 hasPart localR1/R2; localR1 retains contentUrl/source hash. Publisher와의 byte 대조 실패가 이 선언 존재를 지우지는 않는다.',
 run_id='archive #bdfcc6a4-3bf4-4fd7-9e8c-cc6b0deaa43d; outputs/_1693335046. GitHub export #2f5723c2-6d4f-4425-8bf7-47e240585fe9는 별도 ID로 유지.',
 run_input_evidence='같은 archive action→Collection→R1 input; stderr cutadapt/BWA commands use named files. stdout gVCF SHA1 297b1dcd38a5537a7c87de1564dbcdb5ae8d04c8 and metadata SHA25679c41a5e... match directly read VCF. 이것은 동일 저자 계보 확인이다.',
 publisher_exists=True,specific_usage=True,specific_usage_scope='full publisher source URL + concrete archived local input hash/size declaration',run_link=False,record_run_link=True,local_run_link=True,publisher_bytes_match=False,value_checked=False,candidate_value_checked=False,strict_positive=False,
 current_correction='공식 수정 사유 미확인. Publisher gzip413005346bytes와 archived gzip487611787bytes의 크기/헤더/압축 prefix가 다르나 첫20 decoded FASTQ records는 동일하다. 재압축과 양립하며 값 정정이라고 부를 수 없다.',
 missing_reason='전체 decoded digest/입수·재압축 영수증 없음; source compressed bytes 동일성 실패. 선택 CHROM1은 raw FASTQ의 필드가 아니며 첫 gVCF block은 DP0이라 정확한 입력판 판별력을 주지 않는다. 원 컨테이너 분석 재실행 미실시.',
 strongest_claim='구체 source URL과 local input hash를 지목한 실행 선언, 동일 archive output/hash를 확인했다. 원 publisher representation과 기록된 input의 전 파일 동등성 및 선택 출력값의 독립 재현은 미확인이다.',
 consumer_first_opened_utc='2026-11-22T22:11:32.695747+00:00',publisher_first_opened_utc='2026-11-22T22:18:03.806322+00:00',
 source_ids=['R-FR-REPO-02','R-FR-ZEN-12622362','R-ARCHIVE-wetlab-small','R-ARCHIVE-wetlab-output','R-GIAB-README','R-GIAB-MD5','R-GIAB-RANGE'],
 A=view([WET,WP+'#sec008'],'소비 보고 목적·워크플로/자료 참조 링크. 정확한 input graph 및 archive output 본문은 C에 추가한다.','Variant-calling use case와 보관된 실행 보고 존재.','보류: 일반 보고 링크만으로 사용파일판/선택값을 재확인하지 못함'),
 B=view([WET,GIAB+'README_NIST_Illumina_pairedend_NA12878.txt',GIAB+'HG001-part2.md5',GIAB+R1],'A + publisher raw-read 객체/MD5/flow-cell 식별.','B−A: 정확한 source object와 반복 basename/서로 다른 flow-cell MD5가 드러남.','보류: publisher 파일 실존과 다운로드 가능성은 사용증거가 아님',p=True),
 C=view([WET,GIAB+R1,WETZIP+'#ro-crate-metadata.json',WETZIP+'#meta/outputs/_1693335046/stdout.txt',WETZIP+'#meta/outputs/_1693335046/stderr.txt',WETZIP+'#outputs/_1693335046/abc2.sorted.md.realigned.bqsr.vcf.gz'],'B + 같은 Zenodo archive의 action,input,stdout/stderr,VCF. GitHub UUID와 archive UUID를 합치지 않는다.','C−B: exact local hash/size 사용 선언, 기록상 run 연결, CHROM1/DP0와 output hash 재확인. Publisher gzip 차이와 decoded prefix 일치가 동시에 보임. C 기록 재독이며 독립 V는 아님.','보류: full decoded 동일성·당대 transformation 영수증·독립 output 재현 필요',p=True,u=True,rr=True,value='1'),
 alternate_fields=[dict(field='first20 FASTQ records SHA256',value='03e6f9ab7fb44a4fd336c2be7c619acd3b39d535a4e5cf81a26a87257e728b36',location='publisher+archive partial reads, auxiliary; not main CHROM field'),dict(field='record_count',value=22386,location='archive gVCF; auxiliary, not independently regenerated')],
 selection_limit='기간 내 frame18위. 더 이른 LivePublication는 실제 run이나 input_data.txt 제3자 공개 출처가 불명하여 적격 미확인. 원 자료 출처가 밝혀지면 최초2 확정을 재검토해야 한다.'
)]
for c in cases:
 c['specific_usage_local']=True
 c['specific_usage_external']=(c['case_id']=='RUN02')
 for stage in ['A','B','C']:
  c[stage]['specific_usage_local']=c[stage]['specific_usage']
  c[stage]['specific_usage_external']=bool(stage=='C' and c['case_id']=='RUN02')
(P/'cases.json').write_text(json.dumps(cases,ensure_ascii=False,indent=2)+'\n')
fields=['case_id','layer','analysis_title','consumer_url','consumer_locator','purpose','target_time','input_name','field','reported_value','unit','consumer_first_opened_utc','publisher_first_opened_utc','selection_limit']
with (P/'consumers.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(cases)
rows=[]
for c in cases:
 for label in ['A','B','C']:
  v=c[label];rows.append(dict(case_id=c['case_id'],composition=label,visible_urls=' ; '.join(v['visible_urls']),publisher_exists=v['publisher_exists'],specific_usage=v['specific_usage_external'],specific_usage_local=v['specific_usage_local'],record_run_link=v['record_run_link'],publisher_object_run_link=v['run_link'],same_field_value_checked=v['value_checked'],visible_value=v['visible_value'] if v['visible_value'] is not None else '미확인',judgment=v['judgment'],missing_reason=c['missing_reason'],new_fact=v['new_fact'],evidence=v['evidence'],rereading='기록 재독' if label=='C' else '자료 구성의 자체 재판독',source_ids=';'.join(c['source_ids'])))
with (P/'readings.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
ed=[
 dict(case_id='RUN01',role='publisher',edition='GigaDB10.5524/100439; S3CAMELYON16 2022-09-28',publication_date='2018-05-21',modified_date='2022-09-28',reference_period='images collected2006–2016',source_url=CAM+'annotations/test_001.xml',locator='30 polygons/4672 vertices; checksums.md5 rowannotations/test_001.xml',field='polygon vertex; not selected patch coord_x',value='first selected patch coord_x unavailable from publisher without transformation',checksum='publisher MD559279f7dc2b6dd4a741904aca621501a; auditor SHA256b487308cb057d064891d082a3f088aa0a7cc260a95e9879c141bf8244ff29e67',correction='normal_86 relabelled tumor_111; test_049 removed duplicate; target patch correction unknown',limitation='publisher edition is not inferred from consumer filename',source_ids='R-CAM-PAPER;R-CAM-README;R-CAM-XML;R-CAM-MD5'),
 dict(case_id='RUN01',role='consumer_artifact_original',edition='10.5281/zenodo.7676924 v1',publication_date='2023-02-25',modified_date='created2023-03-02; later metadata2023-06-29',reference_period='test2023-02-24',source_url=CPMOLD,locator='predictions.h5 /test/test_001/table; prov_preprocess.log',field='coord_x firstrow',value='63488; preprocess ID9bdc... ended2023-02-24 13:11:14',checksum='auditor prediction SHA25658b6ec9279718e91c0981484fad680628010b16fda6165da9d0310bbf6628444',correction='next archivev1.1 changes provenance and input HDF5 but not prediction bytes',limitation='consumer archive pair, not publisher raw-data successor pair',source_ids='R-ARCHIVE-cpm-v1;R-CPM-EDITIONS'),
 dict(case_id='RUN01',role='consumer_artifact_next',edition='10.5281/zenodo.8095888 v1.1',publication_date='2023-02-25',modified_date='created2023-06-29; modified2023-06-30',reference_period='test2023-02-24; preprocess2023-03-16',source_url=CPMZIP,locator='predictions.h5; prov_preprocess.log; ro-crate-metadata.json',field='coord_x firstrow',value='63488; preprocess IDff67... ended2023-03-16 13:05:48',checksum='same prediction SHA25658b6ec...; ZIPdeclaredMD53654836e51147c59b8072caa7be14406 (not recomputed)',correction='No correction rationale located; concrete altered stage ID/date observed',limitation='same prediction bytes do not establish same input execution chain',source_ids='R-ARCHIVE-cpm-small;R-CPM-EDITIONS'),
 dict(case_id='RUN02',role='publisher',edition='GIABNA12878 flowcell140407_D00360_0017_BH947YADXX',publication_date='unconfirmed; filetimestamp2014-09-18',modified_date='2014-09-18 23:43:59GMT',reference_period='flowcell directory140407',source_url=GIAB+R1,locator='HTTP headers; HG001-part2.md5 fullpath; first20FASTQ records',field='raw sequence; selected CHROM absent',value='Content-Length413005346; first record instrumentHISEQ1:17:H947YADXX',checksum='publisher MD552f3ed344d88278c703faa1280818ce1; first20decoded auditor SHA25603e6f9... only',correction='No subsequent publisher edition/correction notice identified',limitation='Full publisher compressed/decoded hash not recomputed',source_ids='R-GIAB-README;R-GIAB-MD5;R-GIAB-RANGE'),
 dict(case_id='RUN02',role='consumer_artifact',edition='10.5281/zenodo.12622362',publication_date='2024-07-02',modified_date='created2024-07-08',reference_period='run2023-08-29',source_url=WETZIP,locator='inputs/R1 graph; first gVCF record; archiveaction#bdfcc6a4',field='CHROM',value='1; POS1 END63267 DP0',checksum='declared inputSHA2564cd8ae63... size487611787; computed outputSHA25679c41a5e... matches graph',correction='Input gzip representation differs from current source, first20decoded records equal. Recompression plausible, not proven.',limitation='Do not treat current source mismatch as scientific value revision; no full decoded hash or acquisition transform receipt',source_ids='R-ARCHIVE-wetlab-small;R-ARCHIVE-wetlab-output;R-GIAB-RANGE')]
with (P/'editions.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(ed[0]));w.writeheader();w.writerows(ed)
runrows=[]
run_specs=[
 ('RUN01','CPM-v1-preprocess',CPMOLD,'#convert_script:9bdc1af0-53cf-4c3f-8c88-42f004b1f824','2023-02-24 13:11:14','wsi/test/ -> test_001.tif + test_001.xml','v1 derived cam16_mrxs.h5 auditorSHA2567880958ae4c8e9df18929b06debd6c09ada3e0895e6ebbdcfe9b0f5a30516fa9','Original chronological preprocessing record; publisher original files not byte-matched'),
 ('RUN01','CPM-v1-test',CPMOLD,'#test_script:ROCRATE-PUB-1438b57a750ce887d4433d9e','2023-02-24 13:13:41–13:14:58','cam16_mrxs.h5 + prov_test_config.json','log input tableSHA256c9015456f94b60a69b608715d80fdcea91d1e8f832742b5762bc11fe979c1d4b','Original local input declaration; table hash algorithm includes metadata, not file bytes'),
 ('RUN01','CPM-v1.1-preprocess',CPMZIP,'#convert_script:ff67ce65-736f-46d5-9fec-10953cad8695','2023-03-16 13:05:48','wsi/test/ -> test_001.tif + test_001.xml','v1.1 derived cam16_mrxs.h5 auditorSHA256a9eed7914094ee4be27fb7efa3cae952d543d1ab8dccbd0f096edc8b34e29f8a','Later preprocess record; cannot be antecedent of February test merely because file name is same'),
 ('RUN01','CPM-v1.1-test',CPMZIP,'#test_script:ROCRATE-PUB-1438b57a750ce887d4433d9e','2023-02-24 13:13:41–13:14:58','cam16_mrxs.h5 + prov_test_config.json','same original test.log bytes and predictionSHA25658b6ec9279718e91c0981484fad680628010b16fda6165da9d0310bbf6628444','Same original prediction/log retained in later archive, not new analysis execution'),
 ('RUN02','Wetlab-GitHub-export',REPO,'#2f5723c2-6d4f-4425-8bf7-47e240585fe9','2023-08-29T18:50:46.906382+00:00–20:40:48.384424+00:00','Collection#5c519991-d5c8-4fc0-9607-17674b093903 -> NCBI FTP R1/R2','declared R1SHA2564cd8ae63bb5fb67e714c3182bb3035df9d0e83edd26cc51d4439cd44c3015316','Metadata export only; not merged with archive action UUID'),
 ('RUN02','Wetlab-Zenodo-archive',WETZIP,'#bdfcc6a4-3bf4-4fd7-9e8c-cc6b0deaa43d','2023-08-29T18:50:46.906382+00:00–20:40:48.384424+00:00','Collection#dcc0e6bb-4888-4bee-bc06-e995b5d18538 -> local inputs/R1/R2 with exact source contentUrl','declared R1SHA2564cd8ae63bb5fb67e714c3182bb3035df9d0e83edd26cc51d4439cd44c3015316; computed outputSHA25679c41a5eac5d7ebf46d91f3b802b8a79f2c92d946b46bef02828719b992c61c2','Within this archive input/action/commands/output consistent; publisher compressed representation differs')]
for cid,rid,url,aid,t,inp,hashes,scope in run_specs:
 c=next(x for x in cases if x['case_id']==cid)
 runrows.append(dict(case_id=cid,run_record_id=rid,run_id=aid,source_url=url,execution_time=t,input_object=inp,input_hash_and_scope=hashes,record_run_link=True,publisher_object_run_link=False,independent_field_value_checked=False,field=c['field'],reported_value=c['reported_value'],verified_scope=scope,missing_link=c['missing_reason'],source_ids=';'.join(c['source_ids'])))
with (P/'runs.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(runrows[0]));w.writeheader();w.writerows(runrows)
(P/'summary-counts.json').write_text(json.dumps({'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'case_denominator':2,'natural_denominator_inclusion':False,'P':2,'U_concrete_local_input_declaration':2,'U_external_publisher_file_declaration':1,'R_record_local':2,'R_independent_publisher_object':0,'V_authentic_used_edition_selected_field':0,'strict_positive':0,'C_record_reread':2,'independent_selected_field_comparison_success':0,'conditional_V_given_canonical_R':'해당 없음 (분모0)','rows_A_B_C':len(rows),'not_a_blinded_experiment':'A/B/C are preserved material views built by the same analyst, not independent-reader accuracy trials'},ensure_ascii=False,indent=2)+'\n')
print('cases',len(cases),'readings',len(rows),'editions',len(ed),'runs',len(runrows))
