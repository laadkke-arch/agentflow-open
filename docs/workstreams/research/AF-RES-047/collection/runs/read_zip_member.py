"""Read an explicitly named public ZIP member with HTTP Range; never execute it."""
import datetime, hashlib, io, json, pathlib, sys, urllib.request, zipfile

URL, SIZE, PREFIX = sys.argv[1], int(sys.argv[2]), pathlib.Path(sys.argv[3])
RECEIPTS = []

class Remote(io.RawIOBase):
    def __init__(self): self.pos = 0
    def seekable(self): return True
    def readable(self): return True
    def tell(self): return self.pos
    def seek(self, offset, whence=0):
        self.pos = offset if whence == 0 else self.pos + offset if whence == 1 else SIZE + offset
        return self.pos
    def read(self, size=-1):
        if size < 0: size = SIZE - self.pos
        size = min(size, SIZE - self.pos)
        if size <= 0: return b""
        if size > 4_000_000: raise ValueError("Member/range exceeds 4 MB review limit")
        a, b = self.pos, self.pos + size - 1
        t = datetime.datetime.now(datetime.timezone.utc).isoformat()
        req = urllib.request.Request(URL, headers={"Range": f"bytes={a}-{b}"})
        with urllib.request.urlopen(req, timeout=35) as r:
            if r.status != 206 or r.headers.get("Content-Range") != f"bytes {a}-{b}/{SIZE}":
                raise ValueError("Range not honored; refusing full archive download")
            data = r.read(size + 1)
            if len(data) != size: raise ValueError("Unexpected range length")
            RECEIPTS.append({"opened_utc": t, "range": r.headers.get("Content-Range"), "status": r.status})
        self.pos += len(data)
        return data

with zipfile.ZipFile(Remote()) as z:
    entries = [{"name": x.filename, "size": x.file_size, "compressed": x.compress_size, "crc32": f"{x.CRC:08x}"} for x in z.infolist()]
    PREFIX.with_suffix(".listing.json").write_text(json.dumps(entries, indent=2)+"\n")
    print(json.dumps(entries, ensure_ascii=False))
    for name in sys.argv[4:]:
        b = z.read(name)
        dst = PREFIX.parent / (PREFIX.name + "-" + name.replace("/", "__"))
        dst.write_bytes(b)
        print(json.dumps({"member": name, "saved": str(dst), "size": len(b), "sha256": hashlib.sha256(b).hexdigest()}))
PREFIX.with_suffix(".receipt.json").write_text(json.dumps({"url":URL,"archive_size":SIZE,"range_requests":RECEIPTS,"full_archive_hash":"not computed"}, indent=2)+"\n")
