"""Verify an archived SciPy distribution against its download receipt and read its headers."""
import argparse
import base64
import csv
import gzip
import hashlib
import io
import json
import tarfile
from email import policy
from email.parser import BytesParser
from pathlib import Path
from zipfile import ZipFile


def fingerprint(body):
    return {"size": len(body), "sha256": hashlib.sha256(body).hexdigest()}


def wheel_observation(artifact, receipt):
    distribution, version = artifact.name.split("-")[:2]
    prefix = f"{distribution}-{version}.dist-info/"
    metadata_path, wheel_path = prefix + "METADATA", prefix + "WHEEL"
    with ZipFile(artifact) as bundle:
        metadata, wheel = bundle.read(metadata_path), bundle.read(wheel_path)
        records = list(csv.reader(io.StringIO(bundle.read(prefix + "RECORD").decode("utf-8"))))
    for member, content in [(metadata_path, metadata), (wheel_path, wheel)]:
        digest = base64.urlsafe_b64encode(hashlib.sha256(content).digest()).rstrip(b"=").decode("ascii")
        assert [row for row in records if row[0] == member] == [[member, "sha256=" + digest, str(len(content))]], member
    with receipt.with_suffix(".WHEEL").open("wb") as stream:
        stream.write(wheel)
    sidecar = gzip.decompress(receipt.with_suffix(".metadata.gz").read_bytes())
    assert sidecar == metadata, "the .metadata response differs from ZIP METADATA"
    wheel_msg = BytesParser(policy=policy.default).parsebytes(wheel)
    return metadata, metadata_path, {
        "wheel_member": wheel_path,
        "wheel_fingerprint": fingerprint(wheel),
        "wheel_tags": wheel_msg.get_all("Tag", []),
        "generator": wheel_msg["Generator"],
        "wheel_version": wheel_msg["Wheel-Version"],
        "root_is_purelib": wheel_msg["Root-Is-Purelib"],
        "record_members_verified": [metadata_path, wheel_path],
        "sidecar_matches_zip": True,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifact", type=Path)
    parser.add_argument("receipt", type=Path)
    args = parser.parse_args()
    artifact, receipt = args.artifact, args.receipt
    transport = json.loads(receipt.with_suffix(".transport.json").read_bytes())
    with artifact.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    size = artifact.stat().st_size
    assert transport["exit_code"] == 0 and transport["curl"]["response_code"] == 200
    assert (digest, size) == (transport["body_sha256"], transport["body_bytes"])

    if artifact.name.endswith(".whl"):
        metadata, member, extra = wheel_observation(artifact, receipt)
    else:
        member = artifact.name.removesuffix(".tar.gz") + "/PKG-INFO"
        with tarfile.open(artifact, mode="r:gz") as bundle:
            with bundle.extractfile(member) as stream:
                metadata = stream.read()
        extra = {"wheel_tags": [], "wheel_status": "out_of_scope_sdist"}
        receipt.with_suffix(".pkg-info.gz").write_bytes(gzip.compress(metadata, mtime=0))

    message = BytesParser(policy=policy.default).parsebytes(metadata, headersonly=True)
    data = {
        "filename": artifact.name, "artifact_sha256": digest, "artifact_size": size,
        "metadata_member": member, "metadata_fingerprint": fingerprint(metadata),
        "metadata_version": message["Metadata-Version"], "name": message["Name"],
        "version": message["Version"], "requires_python": message["Requires-Python"],
        "requires_dist": message.get_all("Requires-Dist", []),
        "python_classifiers": [v for v in message.get_all("Classifier", []) if v.startswith("Programming Language :: Python")],
        **extra,
    }
    output = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    receipt.with_suffix(".inspection.json").write_text(output, encoding="utf-8")
    print(output, end="")


if __name__ == "__main__":
    main()
