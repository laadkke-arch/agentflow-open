"""Serialize the human review of the first 60 question revisions; no network."""
import csv
import datetime
import hashlib
import html
import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
OUT = BASE / "evidence/imagemagick"
CACHE = BASE / ".cache/imagemagick"
UTC = datetime.datetime.now(datetime.timezone.utc).isoformat()
items = json.loads((CACHE / "initial-h1.json").read_text())
acq = json.loads((OUT / "acquisition-h1.json").read_text())

# eligibility, specific attempt, review reason (initial body only)
review = {
1:(True,False,"숨은 QR 입력·일반 리더가 읽는 출력; 방법은 불특정"),
2:(False,False,"배포용 macOS portable build; 이미지 입력·변환 결과 목표 없음"),
3:(False,True,"C++ 설치·빌드 오류; 구체 이미지 입력·출력 없음"),
4:(False,True,"PNG→CR2 실패는 예시. 주 요구는 지원 포맷 capability 목록 API; 이미지 변환 결과가 아님"),
5:(True,True,"회색 제거 명령을 QuickMagick.exec3로 실제 시도·오류 보고"),
6:(True,False,"사진의 사진 입력과 자동 왜곡 보정 목표; deskew는 언급·추정뿐"),
7:(True,True,"기존 crop/composite 파이프라인의 내부 if/else를 시도하고 미작동 보고"),
8:(False,True,"RMagick 설치·헤더 탐색 오류; 이미지 입력·출력 목표 없음"),
9:(True,False,"블러 패딩 사진에서 원 영역 crop 목표; 특정 호출 없음"),
10:(True,False,"PDF에서 JPG thumbnail 목표; 설정 이름은 언급했으나 적용 시도 명시 없음"),
11:(True,True,"223 JPEG 배치 변환 Killed 및 for-loop 시도"),
12:(True,False,"Plex cover를 제자리 정사각형으로; 명령은 추정·희망 구문"),
13:(True,True,"pango 색 텍스트를 SVG로 쓰면 흑백; PNG 대조 보고"),
14:(True,True,"mogrify scale 실행 뒤 portrait 크기 불일치"),
15:(True,True,"crop/composite 변수 치환 뒤 escaped 괄호 파일명 오류"),
16:(True,False,"무지개 입력을 세로 줄별 평균 hex로 추출; 호출 없음"),
17:(True,True,"template 크기로 두 번째 이미지만 resize하려는 magick 실행"),
18:(True,True,"inline:png:- 쓰기 오류; crop을 base64로 반환하는 구체 명령"),
19:(True,True,"Photoshop warp 목표, polynomial/Shepards/perspective 실제 시도"),
20:(True,True,"bytes 입력 liquid-rescale 파이프 오류와 함수 제시"),
21:(True,True,"PDF→TIFF append 시 숫자 순서가 아닌 사전순 결과"),
22:(True,True,"Lighten composite 실행에 상위 레이어 75% opacity 추가 목표"),
23:(True,True,"PNG chop 실행 후 팔레트 변형 이미지 보고"),
24:(True,True,"고정 폭·원 높이 resize를 두 표기로 시도"),
25:(False,True,"ActiveAdmin 오류 메시지와 create/update 폼 처리; 이미지 변환 출력 목표 아님"),
26:(True,True,"MemoryStream→magick.exe 입력 실패와 디스크 없이 출력 목표"),
27:(True,True,"투명 인물형 하단만 soft edge; blur는 전부 흐려져 포기한 보고"),
28:(False,True,"MoviePy 동영상 렌더링 성능; 이미지/문서 출력 범위 밖"),
29:(True,True,"kmeans 20 동일 이미지 조작의 Docker 지연; 이미지 생성 단계 최적화"),
30:(True,False,"HTTP 응답 이미지의 처리 가능 여부 판정; identify/MagickImage는 조사·질문"),
31:(True,True,"SVG use 입력이 브라우저 3원·IM 1원으로 렌더된 실패 보고"),
32:(True,True,"Magick::Image→QImage 픽셀 변환 함수와 녹색 오류"),
33:(True,True,"scale 3000x3000^ zsh 실패와 quotes 시도"),
34:(True,True,"기존 crop 명령을 여러 부분 composite로 확장; 임시 파일 회피"),
35:(True,True,"logo crop에 이전 parenthesis gravity가 누수하는 출력 오류"),
36:(True,True,"3장 composite/flatten 모두 원 중첩 목표 실패"),
37:(True,True,"layers merge 현재 결과와 중심 정렬 목표"),
38:(True,True,"PNG→SVG 전처리 kmeans/morphology 등 구체 시도"),
39:(True,True,"링크 답을 실제 사용하고 비율별 여백 실패 출력 명시"),
40:(True,True,"Lightroom JPEG EXIF ImageDescription 및 49개 값에서 Title 미발견"),
41:(True,False,"투명 PNG 가장자리 검정/회색만 제거; 특정 호출 없음"),
42:(False,True,"Plesk 서버 설치·컴파일; 이미지 입력·출력 목표 없음"),
43:(True,True,"PCD→TIF 및 colorspace rgb 시도, 색/암부 실패"),
44:(True,False,"흑백 이미지 외곽의 최소 시계방향 꼭짓점 추출; 호출 없음"),
45:(True,True,"montage filename label 절단에서 shell 파이프 실패"),
46:(True,True,"흰 도형 PNG alpha 소실 및 define/colorspace 대조 시도"),
47:(True,True,"두 장 게임 스크린샷 ChangeMask/fuzz 시도·불충족 출력"),
48:(True,True,"웹캠 JPEG imgcat 실패, PNG 성공·JPEG 재변환 실패"),
49:(True,False,"JPEG clipping path 수 추출; exifread 시도 언급뿐 구체 호출·오류 출력 없음"),
50:(True,True,"HEIF byte array→MagickImage에서 DllNotFoundException; PNG 변환 목표"),
51:(True,True,"Imagick polygon 생성 호출의 배치·성능 목표"),
52:(False,True,"MoviePy 동영상 자막 합성; 이미지/문서 출력 범위 밖"),
53:(True,True,"TIF→JP2 lossless 비교 magick compare 명령 오류"),
54:(True,False,"여러 이미지의 빨간 배경 title 영역 crop; 호출 없음"),
55:(True,False,"원 도안→투명 SVG 목표, 찾은 repair SVG를 인용; 실행 여부 미확인"),
56:(True,False,"고정 위치 텍스트 제거·hole filling 문서 언급; 실행 여부 미확인"),
57:(True,True,"SoftLight 50% 합성 두 명령 동작 보고·효율 개선 목표"),
58:(True,True,"image format identify에 두 glob 표기 및 zsh 실패"),
59:(True,True,"blurred frame 생성 명령 실행 후 원본과 동일 출력"),
60:(True,True,"grayscale PNG resize 경고와 두 define 위치 시도"),
}
slots = {77774582:"IM-A1",77797007:"IM-A2",77743451:"IM-U1",77776955:"IM-U2"}

frame=[]
for x in items:
    q=x["current_metadata"]; r=x["first_revision"]; rank=x["rank"]
    eligible,attempt,reason=review[rank]
    row={"tag":"imagemagick","window":"2024-H1","frame_rank":rank,"question_id":q["question_id"],"created_at":datetime.datetime.fromtimestamp(q["creation_date"],datetime.timezone.utc).isoformat(),"initial_revision_url":f"https://stackoverflow.com/revisions/{q['question_id']}/1","initial_revision_guid":r["revision_guid"],"initial_body_sha256":x["raw_first_body_sha256"],"initial_available":True,"current_title":html.unescape(q["title"]),"initial_title":html.unescape(r.get("title","")),"title_changed":html.unescape(q["title"])!=html.unescape(r.get("title","")),"current_tags":";".join(q["tags"]),"initial_tags":";".join(r.get("tags",[])),"tags_changed":q["tags"]!=r.get("tags"),"initial_target_tag_present":"imagemagick" in r.get("tags",[]),"eligible":eligible,"specific_attempt":attempt,"stratum":"attempt" if attempt else "unspecified","selected_slot":slots.get(q["question_id"],""),"review_reason":reason,"disposition":"selected" if q["question_id"] in slots else "ineligible" if not eligible else "eligible_but_stratum_already_full","duplicate_or_cross_tag":"none"}
    frame.append(row)
with (OUT/'frame-part.csv').open('w',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=list(frame[0]));writer.writeheader();writer.writerows(frame)

details={
77743451:{"input_state":"본문의 qr.png 링크가 가리키는 회색조 이미지 안에 숨은 QR","purpose":"일반 QR 리더가 읽을 수 있는 결과 이미지로 드러내기","required_output":"common QR readers가 읽는 QR 이미지","requested_step":"숨은 QR를 드러내는 영상 처리 단계","tool_version":"OpenCV 또는 ImageMagick 언급; 판 미확인","actual_used_products":[],"operation_attempted":"인터넷의 불특정 방법들을 시도했다는 보고만 있음","arguments":"미확인","reported_output_error":"어떤 방법도 작동하지 않았다는 일반 보고; 실제 출력·오류 미제시","allowed_changes":"OpenCV 또는 ImageMagick을 사용할 수 있다는 질문","known_values":"원 입력 URL, 목표 판독기 종류","unknown":"실제로 쓴 제품·방법·인수·판·QR payload·판독기·실패 출력","history":[{"code":"mention_only","subject":"OpenCV / ImageMagick","location":"HTML p1 마지막 질문"},{"code":"failure_reported","subject":"unspecified internet methods","location":"HTML p1 두 번째 문장","specific_operation":False}],"evidence_quotes":["I tried some methods on internet","readable from common qr code readers"],"location":"최초 HTML p1 입력/불특정 시도/도구 언급; p2 목표","initial_later_sensitive":"특정 호출을 안 썼다는 뜻이 아니라 공개 최초판만으로 식별할 수 없음"},
77774582:{"input_state":"remote_image.path로 지정한 이미지; 원문에 픽셀 입력이나 원 파일 미첨부","purpose":"Ruby QuickMagick 또는 RMagick으로 이미지의 회색 부분 제거","required_output":"회색을 제거한 이미지; 인용된 원 방식은 out.png alpha 출력","requested_step":"기존 ImageMagick 처리식을 Ruby wrapper에서 실행하는 구문","tool_version":"QuickMagick / RMagick / ImageMagick; 판 미확인","actual_used_products":["QuickMagick","ImageMagick (convert command executed via QuickMagick.exec3)"],"operation_attempted":"QuickMagick.exec3(command)에 convert 문자열을 전달. +clone부터 threshold 15%까지 그룹 괄호가 빠진 문자열을 실제 시도","arguments":"colorspace=HCL; channel=G; separate; threshold=15%; alpha=off; compose=CopyOpacity; composite","reported_output_error":"오류를 얻었다고 보고; 오류 문자열 없음","allowed_changes":"Ruby의 QuickMagick 또는 RMagick으로 호출을 고치는 것은 허용된 목표","known_values":"인터넷의 원 ImageMagick 파이프라인을 이미 인용했고 그 안에는 escaped parentheses가 있음","unknown":"판·오류 내용·원 픽셀·작동한 괄호 포함 호출을 실행해 봤는지·회색 범위의 수치 정의","history":[{"code":"third_party_suggestion","subject":"forum t=36051의 괄호 포함 clone/mask/CopyOpacity 파이프라인","location":"HTML p1 링크와 pre1"},{"code":"attempted","subject":"괄호 없는 convert 문자열을 QuickMagick.exec3(command)로 실행","location":"HTML p2와 pre2"},{"code":"failure_reported","subject":"해당 실제 실행에서 오류","location":"HTML p3"}],"evidence_quotes":["QuickMagick.exec3(command)","but I got an error"],"location":"최초 HTML p1/pre1 타인 제안; p2/pre2 실제 시도; p3 오류 보고","initial_later_sensitive":"원 정상 그룹 구문을 이미 보았음과 그 구문대로 실행했음은 다르다"},
77776955:{"input_state":"직사각형 사진을 다시 찍은 사진. 원 평면이 굽었을 수 있고 카메라 각도 왜곡도 있음. 예시 링크 2개","purpose":"사진의 사진에서 왜곡 보정을 자동화","required_output":"원 사진의 굽힘 및 카메라 각도에 의한 왜곡을 바로잡은 결과","requested_step":"자동 de-skew/unwarp 단계","tool_version":"제목/태그 ImageMagick; 본문 deskew 언급. 판 미확인","actual_used_products":[],"operation_attempted":"특정 실행 없음; deskew가 flatbed scanner용 같다고 추측","arguments":"미확인","reported_output_error":"실행 또는 실패 출력 없음","allowed_changes":"자동 처리가 목표; 수동 제어점 허용 여부는 미확인","known_values":"입력은 대체로 직사각형, 평면 굽힘·카메라 각도 둘 다 가능","unknown":"실제 사용 도구·판·시도·좌표·자동 코너 검출 조건·굽힘 정도","history":[{"code":"mention_only","subject":"deskew의 적용범위에 대한 추측","location":"HTML p4"},{"code":"not_stated","subject":"actual execution","location":"최초 본문 전체"}],"evidence_quotes":["I don't think deskew applies"],"location":"최초 HTML p1–p3 입력/목표, p4 언급만, p6/p7 예시 링크","initial_later_sensitive":"현재 제목은 2D Object지만 최초 제목은 photo of a photo; 본문 후대 차이는 미열람"},
77797007:{"input_state":"main image와 coords 배열. crop 두 개를 색 제목/테두리와 합성하는 기존 shell 반복문","purpose":"convert 명령 내부 조건으로 스크립트를 단순화하며 원 crop/composite 결과 보존","required_output":"val>300이면 70x50 white patch와 +851+0, 아니면 30x40와 +840+0을 쓰는 합성 출력","requested_step":"바깥 if/else에서 중복되는 convert 파이프라인을 내부 조건으로 통합","tool_version":"ImageMagick 7.0.10-61 / Cygwin","actual_used_products":["ImageMagick"],"operation_attempted":"기존 shell if/else를 convert의 연속 인수 사이에 그대로 삽입한 명령","arguments":"val=300; white patch sizes 70x50 vs 30x40; geometry +851+0 vs +840+0; crop coords[1]/[2]; smush/resize pipeline","reported_output_error":"내부 if/else 시도는 작동하지 않는다고 명시; stderr·실제 출력 없음","allowed_changes":"중복 구문을 줄여 단순화; 필수인지 제안인지 모호한 명령 내부 조건 요구","known_values":"원판, Cygwin, val 조건·두 크기·위치; 기존 바깥 분기 구문","unknown":"원 이미지/coords 실제 값·실패 stderr·내부 조건 자체가 강한 제약인지·후속 실행","history":[{"code":"attempted","subject":"이미 쓰는 crop/merge 스크립트","location":"HTML p1/pre1"},{"code":"failure_reported","subject":"convert 인수 사이의 shell if/else 삽입","location":"HTML 마지막 p와 마지막 pre"}],"evidence_quotes":["below attempt doesn't work"],"location":"최초 HTML p1/pre1 기존 동작, 중간 두 pre의 크기/geometry, 마지막 p/pre 실패 시도","initial_later_sensitive":"기존 외부 분기를 이미 아는 것과 내부 조건 제안을 새로 아는 것은 분리해야 함"}
}
selected=[];sources=[]
for qid,slot in slots.items():
    x=next(x for x in items if x['current_metadata']['question_id']==qid);q=x['current_metadata'];r=x['first_revision']
    body=r['body']; d=details[qid]
    d.update({"case_id":slot,"question_id":qid,"tag":"imagemagick","stratum":"attempt" if '-A' in slot else "unspecified","selection_rank":x['rank'],"within_stratum_rank":int(slot[-1]),"source_id":"SO-IM-"+str(qid),"question_url":q['link'],"initial_revision_url":f"https://stackoverflow.com/revisions/{qid}/1","initial_revision_guid":r['revision_guid'],"created_at":datetime.datetime.fromtimestamp(q['creation_date'],datetime.timezone.utc).isoformat(),"initial_body_sha256":x['raw_first_body_sha256'],"first_revision_author":{"display_name":r['user'].get('display_name'),"user_id":r['user'].get('user_id')},"initial_title":html.unescape(r['title']),"current_title":html.unescape(q['title']),"initial_tags":r.get('tags'),"current_tags":q['tags'],"title_changed":html.unescape(q['title'])!=html.unescape(r['title']),"tags_changed":q['tags']!=r.get('tags'),"initial_body_line_count":len(body.splitlines()),"sealed_at":UTC})
    selected.append(d)
    sources.append({"id":d['source_id'],"questions":["Q1","Q2"],"case_id":slot,"original_url":q['link'],"directly_opened_url":acq[1]['url'],"pinned_url":d['initial_revision_url'],"confirmation_utc":acq[1]['utc'],"author_publisher":d['first_revision_author']['display_name']+' / Stack Overflow (Stack Exchange API)',"lineage":"Stack Overflow question "+str(qid),"version_section":'public revision_number=1; revision_guid='+r['revision_guid']+'; '+d['location'],"fingerprint":{"algorithm":"sha256","body_html":x['raw_first_body_sha256'],"response":acq[1]['sha256']},"observed":d['purpose']+'; '+d['operation_attempted']+'; '+d['reported_output_error'],"claim_relation":"supports first-revision attempt stratum and known-versus-unreported distinction","limitations":d['unknown']+'; revision HTML web open DisabledError; API first revision read successfully; original attached image bytes not opened in phase 1','counted':True,'count_category':'selected_request','duplicate_reason':None})
(OUT/'initial-part.json').write_text(json.dumps(sorted(selected,key=lambda d:d['case_id']),ensure_ascii=False,indent=2))
(OUT/'sources-part.jsonl').write_text(''.join(json.dumps(d,ensure_ascii=False)+'\n' for d in sources))
exposure={"stage":1,"actor":"/root/recruit_imagemagick","reviewed_at":UTC,"machine_received":"questions default included answer_count/accepted_answer_id/is_answered/score; revisions pages included all later revisions and user metadata","model_received":"only masked current ID/creation/title/tags and revision_number=1 bodies for 60 questions; selected revision user metadata briefly displayed names/user IDs and current reputation, not answer/acceptance status","model_not_received":["answer counts","acceptance status","answer or comment bodies","later question revision body","author followups","current question body"],"status_values_used_for_selection":False,"first_page_count":60,"has_more":True,"revision_pages":2,"first_revision_missing":0,"cross_tag_count":0,"h2_extension":"not required: both strata filled in H1","current_title_changed_count":sum(x['title_changed'] for x in frame),"current_tags_changed_count":sum(x['tags_changed'] for x in frame),"target_tag_absent_in_initial_ids":[x['question_id'] for x in frame if not x['initial_target_tag_present']],"selected_ids":list(slots),"scope_sensitivity":{"question_id":77772356,"decision":"exclude","reason":"PNG→CR2 is a failure example; primary requested output is capabilities enumeration, not an image/document result","counterfactual":"If software-format introspection were eligible, it would become IM-A1 and displace 77797007 from first two attempt slots","review":"root independently read first-revision projection and agreed before seal"},"blindness_limit":"not fully blind to current title/tags or author metadata; no outcome fields displayed"}
(OUT/'exposure.json').write_text(json.dumps(exposure,ensure_ascii=False,indent=2))
print(json.dumps({"frame_rows":len(frame),"selected":[(x['case_id'],x['question_id'],x['selection_rank']) for x in selected],"eligibility":sum(x['eligible'] for x in frame),"title_changes":exposure['current_title_changed_count'],"tag_changes":exposure['current_tags_changed_count'],"sealed_at":UTC},ensure_ascii=False))
