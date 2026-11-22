"""Apply the approved full-input observation to records, without running research code.

The before-full-fastq snapshots and raw comparison output remain unchanged.
Only the selected Zenodo action receives the publisher-fingerprint R linkage.
"""
import csv
import datetime
import json
from pathlib import Path

P = Path(__file__).parent
full = json.loads((P / "wetlab-full-fastq-comparison.json").read_text())
manifest = json.loads((P / "wetlab-full-checksum-revisit.json").read_text())
interpretation = json.loads((P / "wetlab-full-fastq-interpretation.json").read_text())
assert full["archive_matches_declared_sha256"] and full["decoded_content_equal"]
assert interpretation["R_external_after"] and not interpretation["V_after"]
archive_md5 = full["archive"]["stored_md5"]
archive_sha = full["archive"]["stored_sha256"]
publisher_md5 = full["publisher"]["stored_md5"]
publisher_sha = full["publisher"]["stored_sha256"]
decoded_sha = full["archive"]["decoded_sha256"]
assert manifest["selected_lines"][0]["text"].endswith(" = " + archive_md5)
new_ids = ["R-WETLAB-FULL-ARCHIVE", "R-GIAB-FULL-FILE", "R-GIAB-MD5-REVISIT"]
now = datetime.datetime.now(datetime.timezone.utc).isoformat()


def write_json(name, value):
    (P / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def read_csv(name):
    with (P / name).open() as stream:
        reader = csv.DictReader(stream)
        return list(reader.fieldnames), list(reader)


def write_csv(name, columns, rows):
    columns = columns + [key for row in rows for key in row if key not in columns]
    columns = list(dict.fromkeys(columns))
    with (P / name).open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


cases = json.loads((P / "cases.json").read_text())
c = next(case for case in cases if case["case_id"] == "RUN02")
c.update(
    run_link=True,
    publisher_bytes_match=False,
    publisher_declared_representation_match=True,
    publisher_decoded_content_match=True,
    publisher_current_matches_own_manifest=False,
    value_checked=False,
    strict_positive=False,
    full_input_check_completed=True,
    full_input_check_evidence="wetlab-full-fastq-comparison.json; wetlab-full-checksum-revisit.json line388; wetlab-full-fastq-interpretation.json",
    run_link_scope="Selected Zenodo action#bdfcc6a4 → local R1 with verified SHA256 → independent publisher MD5 manifest line388. Party run declaration plus independently matched publisher fingerprint; not kernel-I/O attestation.",
    publisher_locator="HG001-part2.md5 line388 exact flow-cell/R1 path; complete current gzip streamed; separate checksum-described representation and current served bytes",
    publisher_edition="NIST HG001 HiSeq300x full flow-cell/R1; publisher manifest MD5 " + archive_md5 + " matches archived gzip487611787bytes. Current publisher gzip413005346bytes has measured MD5 " + publisher_md5 + "; no named successor release established.",
    publisher_value="선정 CHROM은 raw FASTQ에 없는 출력 필드라 독립 검증 미확인. 두 R1의 전체 decoded1409966879bytes/SHA256 " + decoded_sha + "는 동일하며 원 입력 내용 대조는 성공했다.",
    usage_edition="archive inputs/U5c_CCGTCC_L001_R1_001.fastq.gz; same-archive File.sha256=" + archive_sha + "; actual complete memberSHA256 agrees, MD5=" + archive_md5 + " agrees with publisher full-path manifest line388",
    usage_evidence="Zenodo archive action#bdfcc6a4-3bf4-4fd7-9e8c-cc6b0deaa43d → Collection#dcc0e6bb-4888-4bee-bc06-e995b5d18538 → R1 File. Complete member hash matches its declared SHA256; independently published NIST line388 MD5 matches that complete archived gzip. Current served gzip is a different representation.",
    run_input_evidence="Same-archive action→Collection→R1 and stderr cutadapt/BWA file commands; complete local R1SHA256=" + archive_sha + ", MD5=" + archive_md5 + ". Publisher HG001-part2.md5 line388 supplies the same MD5 for the exact source path. This supplies the external-object link for the recorded run; output CHROM remains author-record rereading.",
    current_correction="공식 수정/재압축 시점과 명령은 미확인. Current publisher gzip413005346bytes와 archived gzip487611787bytes는 다르지만 전체 decoded1409966879bytes가 동일하다. Publisher MD5목록은 현재 gzip과 불일치하고 archived gzip과 일치한다. 이 R1 쌍에서 decoded 내용 정정은 관측되지 않았다.",
    missing_reason="획득/재압축 시점·명령과 명명된 다음 발행판은 미확인. 다만 원 archive R1은 publisher full-path MD5가 지목한 표현과 전체 hash로 연결됐다. 독립 machine-I/O 증명은 없으나 요구한 당사자 runID/input 명세 연결은 충족한다. CHROM1은 raw FASTQ 필드가 아니며 독립 원 컨테이너 출력 재실행은 미실시이므로 V는0이다.",
    strongest_claim="특정 Zenodo 원 실행 기록이 지목한 R1의 전체 바이트가 독립 발행자 checksum 목록의 정확 경로·MD5와 일치한다. 현재 publisher gzip은 다른 바이트 표현이지만 전체 decoded 내용은 같다. 따라서 기록상 발행자 입력 연결 R은 확인했으며, 선택 CHROM 출력의 독립 검증 V는 미확인이다.",
)
c["source_ids"] = list(dict.fromkeys(c["source_ids"] + new_ids))
c["B"]["evidence"] = "A + publisher raw-read 객체, HG001-part2.md5 line388와 current gzip의 전체 checksum. C의 archived input/실행 연결은 이 구성에 포함하지 않는다."
c["B"]["new_fact"] = "B−A: 정확한 source path와 publisher MD5가 있으며 current served gzip의 실제 MD5는 목록과 다르다. 이 구성만으로 목록이 어느 소비 파일과 일치하는지는 모른다."
c["B"]["publisher_current_matches_own_manifest"] = False
c["C"].update(
    run_link=True,
    record_run_link=True,
    publisher_bytes_match=False,
    publisher_declared_representation_match=True,
    publisher_decoded_content_match=True,
    value_checked=False,
    evidence="B + 같은 Zenodo archive action,input,stdout/stderr,VCF 및 완전 R1 스트리밍 대조. 독립 publisher manifest line388 MD5가 archived R1 실측과 일치한다. 다른 GitHub UUID는 합치지 않는다.",
    new_fact="C−B: complete archived R1SHA256이 당대 File 선언과 일치하고 MD5가 독립 publisher 목록의 full path/line388과 일치하여 R_external이 확인된다. 현재 gzip은 다르지만 전체 decoded 내용은 같다. CHROM1은 C 기록 재독이며 독립 V는 미확인이다.",
    judgment="입력 사용 기록의 외부 객체 연결은 확인(R=1); 선택 CHROM 출력의 독립 검증은 보류(V=0).",
)
if manifest["source_url"] not in c["C"]["visible_urls"]:
    c["C"]["visible_urls"].append(manifest["source_url"])
if full["archive_url"] + "#" + full["member"] not in c["C"]["visible_urls"]:
    c["C"]["visible_urls"].append(full["archive_url"] + "#" + full["member"])
write_json("cases.json", cases)

columns, rows = read_csv("readings.csv")
for row in rows:
    if row["case_id"] != "RUN02":
        continue
    cfg = row["composition"]
    view = c[cfg]
    row["evidence"], row["new_fact"], row["judgment"] = view["evidence"], view["new_fact"], view["judgment"]
    row["visible_urls"] = " ; ".join(view["visible_urls"])
    row["publisher_object_run_link"] = cfg == "C"
    row["same_field_value_checked"] = False
    row["publisher_declared_representation_match"] = True if cfg == "C" else "미확인: archived input 미포함"
    row["publisher_decoded_content_match"] = True if cfg == "C" else "미확인: archived input 미포함"
    row["publisher_bytes_match"] = False if cfg == "C" else "미확인: archived input 미포함"
    row["missing_reason"] = c["missing_reason"] if cfg == "C" else view["judgment"]
    row["audit_only_full_missing_reason"] = c["missing_reason"]
    if cfg == "C":
        row["source_ids"] = ";".join(c["source_ids"])
write_csv("readings.csv", columns, rows)

columns, rows = read_csv("runs.csv")
for row in rows:
    if row["case_id"] != "RUN02":
        continue
    if row["run_record_id"] == "Wetlab-Zenodo-archive":
        row["publisher_object_run_link"] = True
        row["publisher_declared_representation_match"] = True
        row["publisher_decoded_content_match"] = True
        row["publisher_bytes_match"] = False
        row["input_hash_and_scope"] = "Complete R1SHA256=" + archive_sha + " matches this archive File; computed R1MD5=" + archive_md5 + " matches independent publisher manifest line388; complete decodedSHA256=" + decoded_sha
        row["verified_scope"] = c["run_link_scope"]
        row["missing_link"] = c["missing_reason"]
        row["source_ids"] = ";".join(c["source_ids"])
    else:
        # This metadata export has a different action UUID. No cross-export lift.
        row["publisher_object_run_link"] = False
        row["publisher_declared_representation_match"] = "not independently applied to this export"
        row["publisher_decoded_content_match"] = "not independently applied to this export"
        row["publisher_bytes_match"] = False
        row["missing_link"] = "Different GitHub action UUID; the complete-byte comparison audited the named Zenodo archive action only. No automatic cross-export identity or external-link promotion. Independent CHROM reproduction remains unperformed."
write_csv("runs.csv", columns, rows)

columns, rows = read_csv("editions.csv")
rows = [row for row in rows if row["role"] != "publisher_checksum_representation"]
for row in rows:
    if row["case_id"] != "RUN02":
        continue
    if row["role"] == "publisher":
        row["edition"] = "Current served NIST R1 gzip; distinct from manifest-described compressed representation"
        row["locator"] = "Complete current R1 gzip; source HTTP headers; HG001-part2.md5 line388 compared separately"
        row["value"] = "stored413005346bytes; decoded1409966879bytes; selected output CHROM absent"
        row["checksum"] = "computed stored MD5=" + publisher_md5 + "; SHA256=" + publisher_sha + "; decoded SHA256=" + decoded_sha
        row["correction"] = "Current compressed bytes differ from publisher manifest and archive, but complete decoded content is identical to the archived input. No biological value correction observed in this pair."
        row["limitation"] = "No named successor release/recompression timestamp established. Full content equality is not independent CHROM output reproduction."
        row["source_ids"] = "R-GIAB-README;R-GIAB-MD5;R-GIAB-FULL-FILE;R-GIAB-MD5-REVISIT"
    elif row["role"] == "consumer_artifact":
        row["locator"] = "complete inputs/U5c_CCGTCC_L001_R1_001.fastq.gz; same-archive action#bdfcc6a4 and FileSHA; first gVCF record"
        row["checksum"] = "computed inputSHA256=" + archive_sha + ", MD5=" + archive_md5 + "; matches same-archive SHA declaration and publisher manifest MD5 line388; computed outputSHA25679c41a5e... remains a same-author check"
        row["correction"] = "Archived gzip matches publisher checksum-described representation; current served gzip differs while complete decoded bytes match."
        row["limitation"] = "R applies to this archived input and action. Compression history and independent output CHROM calculation remain unconfirmed."
        row["source_ids"] = ";".join(c["source_ids"])
rows.append(dict(case_id="RUN02", role="publisher_checksum_representation", edition="NIST HG001-part2.md5 full-path R1 representation identified by MD5 " + archive_md5, publication_date="미확인: HTTP Last-Modified is not publication proof", modified_date="2014-09-19T12:07:11GMT (manifest HTTP header)", reference_period="flowcell140407_D00360_0017_BH947YADXX; run2023-08-29", source_url=manifest["source_url"], locator="line388; different same-basename flowcells in lines116/254", field="publisher compressed-object fingerprint; CHROM output absent", value="manifest MD5=" + archive_md5 + "; matches complete archived gzip487611787bytes", checksum="manifest file actualSHA256=" + manifest["sha256"] + "; archived member actualMD5=" + archive_md5, correction="The current file served at the corresponding download path does not match this published MD5; complete decoded contents agree.", limitation="Publisher-described byte representation is matched; its exact release/acquisition/recompression date and a named next edition are not established.", source_ids="R-GIAB-MD5;R-GIAB-MD5-REVISIT;R-WETLAB-FULL-ARCHIVE;R-GIAB-FULL-FILE"))
write_csv("editions.csv", columns, rows)

summary = json.loads((P / "summary-counts.json").read_text())
summary.update(checked_utc=now, R_independent_publisher_object=1, R_positive_case_ids=["RUN02"], R_positive_run_record_ids=["Wetlab-Zenodo-archive"], V_authentic_used_edition_selected_field=0, strict_positive=0, conditional_V_given_canonical_R="0/1", conditional_V_given_canonical_R_detail={"numerator": 0, "denominator": 1, "unit": "cases"}, publisher_declared_representation_match_cases=1, publisher_decoded_content_match_cases=1, amendment="root A10 / full FASTQ follow-up; prior counts preserved in summary-counts-before-full-fastq.json")
write_json("summary-counts.json", summary)
print("Applied full FASTQ evidence: R_external1/2, V0/2, V|R0/1; selected Zenodo record only")
