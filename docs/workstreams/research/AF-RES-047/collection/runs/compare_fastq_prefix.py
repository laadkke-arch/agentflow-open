"""Compare only first gzip/FASTQ records from a crate member and publisher.

No complete-file checksum is asserted. This limits transfer to HTTP ranges,
and preserves the exact range receipts and gzip headers for later auditing.
"""
import datetime, hashlib, io, json, pathlib, urllib.request, zipfile, zlib

P = pathlib.Path(__file__).parent
URL = "https://zenodo.org/api/records/12622362/files/wetlab2variations_full.zip/content"
SIZE = 4051896220
MEMBER = "inputs/U5c_CCGTCC_L001_R1_001.fastq.gz"
PUBLISHER = "https://ftp-trace.ncbi.nlm.nih.gov/giab/ftp/data/NA12878/NIST_NA12878_HG001_HiSeq_300x/140407_D00360_0017_BH947YADXX/Project_RM8398/Sample_U5c/U5c_CCGTCC_L001_R1_001.fastq.gz"
receipts = []

class Remote(io.RawIOBase):
    def __init__(self): self.pos = 0
    def seekable(self): return True
    def readable(self): return True
    def tell(self): return self.pos
    def seek(self, offset, whence=0):
        self.pos = offset if whence == 0 else self.pos + offset if whence == 1 else SIZE + offset
        return self.pos
    def read(self, size=-1):
        if size < 0 or size > 1_000_000: raise ValueError("refuse large range")
        size = min(size, SIZE-self.pos)
        if size <= 0: return b""
        a,b = self.pos,self.pos+size-1
        q = urllib.request.Request(URL, headers={"Range":f"bytes={a}-{b}"})
        t = datetime.datetime.now(datetime.timezone.utc).isoformat()
        with urllib.request.urlopen(q, timeout=35) as r:
            if r.status != 206: raise ValueError("range not honored")
            raw = r.read(size+1)
            if len(raw) != size: raise ValueError("unexpected range length")
            receipts.append(dict(url=URL,opened_utc=t,status=r.status,range=r.headers.get("Content-Range")))
        self.pos += size
        return raw

with zipfile.ZipFile(Remote()) as z:
    info = z.getinfo(MEMBER)
    with z.open(MEMBER) as f: crate = f.read(65536)
t = datetime.datetime.now(datetime.timezone.utc).isoformat()
req = urllib.request.Request(PUBLISHER, headers={"Range":"bytes=0-65535"})
with urllib.request.urlopen(req,timeout=35) as r:
    if r.status != 206: raise ValueError("publisher range not honored")
    publisher = r.read(65537)
    if len(publisher) != 65536: raise ValueError("publisher range length mismatch")
    receipts.append(dict(url=PUBLISHER,opened_utc=t,status=r.status,range=r.headers.get("Content-Range"),last_modified=r.headers.get("Last-Modified")))

def inspect(b):
    d = zlib.decompressobj(31).decompress(b,65536)
    lines = d.decode().splitlines()
    return dict(compressed_prefix_bytes=len(b),compressed_prefix_sha256=hashlib.sha256(b).hexdigest(),gzip_header_hex=b[:32].hex(),first_fastq_record=lines[:4],first_20_records_sha256=hashlib.sha256("\n".join(lines[:80]).encode()).hexdigest(),decoded_prefix_bytes=len(d))

a,b = inspect(crate),inspect(publisher)
result = dict(checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),crate_member=MEMBER,crate_member_complete_size=info.file_size,publisher_url=PUBLISHER,range_receipts=receipts,crate_prefix=a,publisher_prefix=b,first_record_equal=a["first_fastq_record"]==b["first_fastq_record"],first_20_records_equal=a["first_20_records_sha256"]==b["first_20_records_sha256"],full_file_equality="unconfirmed; only prefix read; source modification or recompression not established")
(P/"wetlab-fastq-prefix-comparison.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
