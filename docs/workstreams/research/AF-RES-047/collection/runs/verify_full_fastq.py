"""Optional follow-up: stream both complete RUN02 R1 objects without storing them.

Not run during AF-RES-047. Requires about 0.9 GB transfer, decompression and
network time. It checks present bytes/decoded content, not historical use.
The --perform flag prevents accidental bulk transfer when inspecting the script.
"""
import argparse
import datetime
import gzip
import hashlib
import io
import json
from pathlib import Path
import urllib.request
import zipfile

ARCHIVE = "https://zenodo.org/api/records/12622362/files/wetlab2variations_full.zip/content"
ARCHIVE_SIZE = 4051896220
MEMBER = "inputs/U5c_CCGTCC_L001_R1_001.fastq.gz"
PUBLISHER = "https://ftp-trace.ncbi.nlm.nih.gov/giab/ftp/data/NA12878/NIST_NA12878_HG001_HiSeq_300x/140407_D00360_0017_BH947YADXX/Project_RM8398/Sample_U5c/U5c_CCGTCC_L001_R1_001.fastq.gz"
EXPECTED_ARCHIVED_SHA256 = "4cd8ae63bb5fb67e714c3182bb3035df9d0e83edd26cc51d4439cd44c3015316"
EXPECTED_PUBLISHER_MD5 = "52f3ed344d88278c703faa1280818ce1"
RECEIPTS = []


class RemoteZip(io.RawIOBase):
    """One cached range; seeks outside it perform a bounded HTTP range read."""
    def __init__(self):
        self.pos, self.start, self.cache = 0, 0, b""

    def readable(self):
        return True

    def seekable(self):
        return True

    def tell(self):
        return self.pos

    def seek(self, offset, whence=0):
        self.pos = offset if whence == 0 else self.pos + offset if whence == 1 else ARCHIVE_SIZE + offset
        return self.pos

    def read(self, size=-1):
        if size < 0:
            size = ARCHIVE_SIZE - self.pos
        size = min(size, ARCHIVE_SIZE - self.pos)
        if size <= 0:
            return b""
        if size > 16 * 1024 * 1024:
            raise ValueError("unexpected oversized ZIP range")
        if not (self.start <= self.pos and self.pos + size <= self.start + len(self.cache)):
            a = self.pos
            b = min(ARCHIVE_SIZE, a + max(size, 8 * 1024 * 1024)) - 1
            request = urllib.request.Request(ARCHIVE, headers={"Range": f"bytes={a}-{b}"})
            stamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
            with urllib.request.urlopen(request, timeout=60) as response:
                if response.status != 206 or response.headers.get("Content-Range") != f"bytes {a}-{b}/{ARCHIVE_SIZE}":
                    raise ValueError("archive range or size changed")
                self.cache = response.read(b - a + 2)
                if len(self.cache) != b - a + 1:
                    raise ValueError("archive range length mismatch")
                RECEIPTS.append({"checked_utc": stamp, "url": response.url, "content_range": response.headers.get("Content-Range")})
            self.start = a
        begin = self.pos - self.start
        result = self.cache[begin:begin + size]
        self.pos += len(result)
        return result


class HashingReader:
    def __init__(self, stream):
        self.stream, self.sha256, self.md5, self.size = stream, hashlib.sha256(), hashlib.md5(), 0

    def read(self, size=-1):
        block = self.stream.read(size)
        self.sha256.update(block)
        self.md5.update(block)
        self.size += len(block)
        return block


def inspect(stream):
    wrapped = HashingReader(stream)
    decoded_hash, decoded_size = hashlib.sha256(), 0
    with gzip.GzipFile(fileobj=wrapped, mode="rb") as decoded:
        while True:
            block = decoded.read(1024 * 1024)
            if not block:
                break
            decoded_hash.update(block)
            decoded_size += len(block)
    # Reach EOF and include any bytes left in the stored gzip object.
    while wrapped.read(1024 * 1024):
        pass
    return {"stored_bytes": wrapped.size, "stored_sha256": wrapped.sha256.hexdigest(), "stored_md5": wrapped.md5.hexdigest(), "decoded_bytes": decoded_size, "decoded_sha256": decoded_hash.hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--perform", action="store_true")
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("wetlab-full-fastq-comparison.json"))
    args = parser.parse_args()
    if not args.perform:
        parser.error("Inspect the fixed URLs and transfer size, then pass --perform to execute")
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    with zipfile.ZipFile(RemoteZip()) as archive:
        with archive.open(MEMBER) as member:
            archived = inspect(member)
    stamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    with urllib.request.urlopen(PUBLISHER, timeout=60) as source:
        RECEIPTS.append({"checked_utc": stamp, "url": source.url, "content_length": source.headers.get("Content-Length"), "last_modified": source.headers.get("Last-Modified")})
        publisher = inspect(source)
    result = {"started_utc": started, "finished_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "archive_url": ARCHIVE, "member": MEMBER, "publisher_url": PUBLISHER, "archive": archived, "publisher": publisher, "archive_matches_declared_sha256": archived["stored_sha256"] == EXPECTED_ARCHIVED_SHA256, "publisher_matches_read_checksum_list": publisher["stored_md5"] == EXPECTED_PUBLISHER_MD5, "decoded_content_equal": archived["decoded_sha256"] == publisher["decoded_sha256"] and archived["decoded_bytes"] == publisher["decoded_bytes"], "range_receipts": RECEIPTS, "limitation": "Current-byte comparison only. Equality does not independently prove that the historical workflow read this publisher object, and does not independently reproduce CHROM=1."}
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in ["archive_matches_declared_sha256", "publisher_matches_read_checksum_list", "decoded_content_equal"]}, indent=2))


if __name__ == "__main__":
    main()
