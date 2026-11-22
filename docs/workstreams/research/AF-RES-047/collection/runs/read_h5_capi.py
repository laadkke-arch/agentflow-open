"""Read small HDF5 arrays through the installed HDF5 C API; no pickle loading.

Only primitive/fixed string/compound/array data types are decoded. Variable
length/object payloads remain unread. Source workflow code is never executed.
"""
import ctypes as C
import ctypes.util
import datetime
import hashlib
import json
import pathlib
import sys
import numpy as np

lib = C.CDLL(ctypes.util.find_library("hdf5_serial"))
hid = C.c_longlong
def api(name, ret, *args):
    f = getattr(lib, name); f.restype = ret; f.argtypes = args
    return f
api("H5open", C.c_int)()
api("H5Eset_auto2", C.c_int, hid, C.c_void_p, C.c_void_p)(0, None, None)
fopen = api("H5Fopen", hid, C.c_char_p, C.c_uint, hid)
dopen = api("H5Dopen2", hid, hid, C.c_char_p, hid)
gettype = api("H5Dget_type", hid, hid)
getspace = api("H5Dget_space", hid, hid)
tclass = api("H5Tget_class", C.c_int, hid)
tsize = api("H5Tget_size", C.c_size_t, hid)
torder = api("H5Tget_order", C.c_int, hid)
tsign = api("H5Tget_sign", C.c_int, hid)
tnmembers = api("H5Tget_nmembers", C.c_int, hid)
tmname = api("H5Tget_member_name", C.c_void_p, hid, C.c_uint)
tmtype = api("H5Tget_member_type", hid, hid, C.c_uint)
tmoffset = api("H5Tget_member_offset", C.c_size_t, hid, C.c_uint)
tclose = api("H5Tclose", C.c_int, hid)
freemem = api("H5free_memory", C.c_int, C.c_void_p)
tarrayndims = api("H5Tget_array_ndims", C.c_int, hid)
tarraydims = api("H5Tget_array_dims2", C.c_int, hid, C.POINTER(C.c_ulonglong))
tsuper = api("H5Tget_super", hid, hid)

def dtype(t):
    cl, size = tclass(t), tsize(t)
    order = ">" if torder(t) == 1 else "<"
    if cl == 0: return np.dtype(order + ("i" if tsign(t) == 1 else "u") + str(size))
    if cl == 4: return np.dtype(order + "u" + str(size))
    if cl == 1: return np.dtype(order + "f" + str(size))
    if cl == 3:
        if api("H5Tis_variable_str", C.c_int, hid)(t): raise ValueError("variable string skipped")
        return np.dtype("S" + str(size))
    if cl == 6:
        names, formats, offsets = [], [], []
        for i in range(tnmembers(t)):
            ptr = tmname(t, i); names.append(C.string_at(ptr).decode()); freemem(ptr)
            mt = tmtype(t, i); formats.append(dtype(mt)); tclose(mt)
            offsets.append(tmoffset(t, i))
        return np.dtype(dict(names=names, formats=formats, offsets=offsets, itemsize=size))
    if cl == 10:
        n = tarrayndims(t); a = (C.c_ulonglong * n)(); tarraydims(t, a)
        mt = tsuper(t); dt = dtype(mt); tclose(mt)
        return np.dtype((dt, tuple(a)))
    raise ValueError(f"HDF5 class {cl} skipped; no unsafe/object decoding")

def plain(x):
    if isinstance(x, bytes): return x.decode(errors="replace")
    if isinstance(x, np.void): return {n: plain(x[n]) for n in x.dtype.names}
    if isinstance(x, np.ndarray): return [plain(y) for y in x]
    if isinstance(x, np.generic): return plain(x.item())
    if isinstance(x, tuple): return [plain(y) for y in x]
    return x

path = pathlib.Path(sys.argv[1]); f = fopen(str(path).encode(), 0, 0)
if f < 0: raise ValueError("HDF5 file cannot be opened")
names = []
CB = C.CFUNCTYPE(C.c_int, hid, C.c_char_p, C.c_void_p, C.c_void_p)
@CB
def callback(g, name, info, data): names.append(name.decode()); return 0
visit = api("H5Lvisit2", C.c_int, hid, C.c_int, C.c_int, CB, C.c_void_p)
visit(f, 0, 0, callback, None)
out = []
for name in names:
    d = dopen(f, name.encode(), 0)
    if d < 0: continue
    t, sp = gettype(d), getspace(d)
    n = api("H5Sget_simple_extent_ndims", C.c_int, hid)(sp)
    dims = (C.c_ulonglong * n)()
    api("H5Sget_simple_extent_dims", C.c_int, hid, C.POINTER(C.c_ulonglong), C.c_void_p)(sp, dims, None)
    row = dict(path=name, shape=list(dims), type_class=tclass(t), type_size=tsize(t))
    if name.endswith("/table"):
        anames = []
        ACB = C.CFUNCTYPE(C.c_int, hid, C.c_char_p, C.c_void_p, C.c_void_p)
        @ACB
        def acb(g, aname, info, data): anames.append(aname.decode()); return 0
        ai = C.c_ulonglong(0)
        api("H5Aiterate2", C.c_int, hid, C.c_int, C.c_int, C.POINTER(C.c_ulonglong), ACB, C.c_void_p)(d,0,0,C.byref(ai),acb,None)
        attrs = {}
        for aname in anames:
            a = api("H5Aopen", hid, hid, C.c_char_p, hid)(d,aname.encode(),0)
            at = api("H5Aget_type", hid, hid)(a)
            asp = api("H5Aget_space", hid, hid)(a)
            acount = api("H5Sget_simple_extent_npoints", C.c_longlong, hid)(asp)
            try:
                adt = dtype(at); ab = C.create_string_buffer(acount * adt.itemsize)
                if api("H5Aread", C.c_int, hid,hid,C.c_void_p)(a,at,ab) < 0: raise ValueError("read failed")
                attrs[aname] = plain(np.frombuffer(ab.raw,dtype=adt))
            except Exception as e: attrs[aname] = {"unread_reason":str(e)}
            tclose(at); api("H5Sclose",C.c_int,hid)(asp); api("H5Aclose",C.c_int,hid)(a)
        row["attributes"] = attrs
    try:
        dt = dtype(t); count = int(np.prod(dims)) if n else 1; size = count * dt.itemsize
        if size > 4_000_000: raise ValueError("array exceeds 4 MB read limit")
        b = C.create_string_buffer(size)
        rc = api("H5Dread", C.c_int, hid, hid, hid, hid, hid, C.c_void_p)(d,t,0,0,0,b)
        if rc < 0: raise ValueError("H5Dread failed")
        a = np.frombuffer(b.raw, dtype=dt).reshape(tuple(dims) or ())
        row.update(dtype=str(dt), first_values=plain(a.reshape(-1)[:8]), data_sha256=hashlib.sha256(b.raw).hexdigest())
    except Exception as e: row["unread_reason"] = str(e)
    out.append(row)
    tclose(t); api("H5Sclose", C.c_int, hid)(sp); api("H5Dclose", C.c_int, hid)(d)
api("H5Fclose", C.c_int, hid)(f)
result = dict(read_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),file=str(path),file_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),method="installed libhdf5 read-only C API; name-index order; no workflow rerun; no object/pickle decoding",datasets=out)
dst = path.with_suffix(".inspection.json"); dst.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n")
print(json.dumps(result, ensure_ascii=False, indent=2))
