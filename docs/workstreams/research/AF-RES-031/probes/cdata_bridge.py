"""Import PyArrow C Data into Arrow Java in one embedded JVM."""
import argparse
import ctypes
import gc
import json
import os
from pathlib import Path
import struct
import sys
import weakref

import jpype
import pyarrow as pa


class CArray(ctypes.Structure):
    _fields_ = [
        ("length", ctypes.c_int64), ("null_count", ctypes.c_int64), ("offset", ctypes.c_int64),
        ("n_buffers", ctypes.c_int64), ("n_children", ctypes.c_int64), ("buffers", ctypes.c_void_p),
        ("children", ctypes.c_void_p), ("dictionary", ctypes.c_void_p),
        ("release", ctypes.c_void_p), ("private_data", ctypes.c_void_p),
    ]


class CSchema(ctypes.Structure):
    _fields_ = [
        ("format", ctypes.c_void_p), ("name", ctypes.c_void_p), ("metadata", ctypes.c_void_p),
        ("flags", ctypes.c_int64), ("n_children", ctypes.c_int64), ("children", ctypes.c_void_p),
        ("dictionary", ctypes.c_void_p), ("release", ctypes.c_void_p), ("private_data", ctypes.c_void_p),
    ]


def load_ipc(path, name):
    with pa.ipc.open_stream(path) as reader:
        return reader.read_all().column(name).combine_chunks()


def release_if_owned(value):
    if value.release:
        callback = ctypes.CFUNCTYPE(None, ctypes.POINTER(type(value)))(value.release)
        callback(ctypes.byref(value))
        assert not value.release, "producer release did not clear callback"


def vector_from(source, allocator):
    if pa.types.is_list(source.type) or pa.types.is_large_list(source.type):
        address = source.values.buffers()[1].address
    else:
        address = source.buffers()[2].address
    owner = weakref.ref(source)
    array, schema = CArray(), CSchema()
    arrow_array = jpype.JClass("org.apache.arrow.c.ArrowArray")
    arrow_schema = jpype.JClass("org.apache.arrow.c.ArrowSchema")
    java_array = arrow_array.wrap(ctypes.addressof(array))
    java_schema = arrow_schema.wrap(ctypes.addressof(schema))
    vector = None
    ready = False
    try:
        source._export_to_c(ctypes.addressof(array), ctypes.addressof(schema))
        del source
        gc.collect()
        assert owner() is None, "producer Python object is still live before import"
        assert array.release and schema.release
        vector = jpype.JClass("org.apache.arrow.c.Data").importVector(
            allocator, java_array, java_schema, None, False
        )
        assert not array.release and not schema.release, "C Data release was not consumed or moved"
        assert owner() is None
        try:
            actual_data = vector.getDataVector().getDataBuffer()
        except AttributeError:
            actual_data = vector.getDataBuffer()
        assert actual_data.memoryAddress() == address, "foreign data buffer was replaced"
        ready = True
        return vector
    finally:
        if vector is not None and not ready:
            vector.close()
        release_if_owned(array)
        release_if_owned(schema)
        java_array.close()
        java_schema.close()


def rss_bytes():
    for line in Path("/proc/self/status").read_text().splitlines():
        if line.startswith("VmRSS:"):
            return int(line.split()[1]) * 1024
    raise RuntimeError("VmRSS unavailable")


def large_binary(capacity, high_offset, tail, fill_byte):
    data = pa.allocate_buffer(capacity)
    ctypes.memset(data.address, fill_byte, capacity)
    ctypes.memmove(data.address + high_offset, tail, len(tail))
    offsets = pa.py_buffer(struct.pack("<3q", 0, high_offset, capacity))
    return pa.Array.from_buffers(pa.large_binary(), 2, [None, offsets, data])


def check_threshold(allocator, fixture):
    high_offset = fixture["offset_bytes"]
    tail = bytes.fromhex(fixture["tail_hex"])
    capacity = high_offset + len(tail)
    limit = int(Path("/sys/fs/cgroup/memory.max").read_text())
    current = int(Path("/sys/fs/cgroup/memory.current").read_text())
    cap = fixture["allocator_cap_bytes"]
    print(json.dumps({"stage": "capacity_gate", "memory_max": limit, "memory_current": current,
                      "allocator_cap": cap, "requested": capacity, "offset": high_offset}), file=sys.stderr, flush=True)
    assert limit - current >= fixture["minimum_available_bytes"], "insufficient cgroup headroom"
    assert 2**31 < capacity < cap
    pool = pa.default_memory_pool()
    allocated_before = pool.bytes_allocated()
    rss_before = rss_bytes()
    vector = vector_from(large_binary(capacity, high_offset, tail, fixture["fill_byte"]), allocator)
    try:
        allocated = pool.bytes_allocated() - allocated_before
        rss_delta = rss_bytes() - rss_before
        print(json.dumps({"stage": "foreign_imported", "arrow_pool_delta": allocated, "rss_delta": rss_delta}),
              file=sys.stderr, flush=True)
        assert allocated >= capacity and rss_delta >= capacity - 64 * 2**20
        assert vector.getClass().getSimpleName() == "LargeVarBinaryVector"
        assert vector.getValueCount() == 2 and vector.getNullCount() == 0
        assert vector.getDataBuffer().capacity() == capacity
        assert vector.getOffsetBuffer().getLong(8) == high_offset
        assert vector.getOffsetBuffer().getLong(16) == capacity
        assert vector.getDataBuffer().getByte(high_offset - 1) == fixture["fill_byte"]
        observed_tail = bytes(vector.get(1))
        assert observed_tail == tail
        print(json.dumps({"tail_hex": observed_tail.hex(), "offset_bytes": high_offset,
                          "terminal_offset_bytes": capacity, "consumer_buffer_capacity": vector.getDataBuffer().capacity(),
                          "allocated_pool_delta": allocated, "touched_bytes": capacity,
                          "class": str(vector.getClass().getSimpleName()), "same_pid": True}, sort_keys=True))
    finally:
        vector.close()
    assert pool.bytes_allocated() == allocated_before, "export did not release the PyArrow payload"


def check_small(allocator, path, large):
    baseline = pa.total_allocated_bytes()
    binary = vector_from(load_ipc(path, "payload"), allocator)
    try:
        items = vector_from(load_ipc(path, "items"), allocator)
        try:
            observed = jpype.JClass("ArrowConsumer").observe(binary, items, large)
            print(json.dumps({**json.loads(str(observed)), "same_pid": True,
                              "foreign_buffer_addresses_equal": True, "source_wrappers_gone": True,
                              "source_release_slots_cleared": True}, sort_keys=True))
        finally:
            items.close()
    finally:
        binary.close()
    assert pa.total_allocated_bytes() == baseline, "export did not release the PyArrow arrays"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--jvm", required=True)
    parser.add_argument("--jni-library-dir", required=True, type=Path)
    parser.add_argument("--classpath-file", type=Path, required=True)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--ipc", type=Path)
    group.add_argument("--threshold-fixture", type=Path)
    parser.add_argument("--type", choices=("large", "stored"))
    args = parser.parse_args()
    assert pa.__version__ == "21.0.0" and jpype.__version__ == "1.6.0"
    fixture = json.loads(args.threshold_fixture.read_bytes())["large_buffer"] if args.threshold_fixture else None
    cap = fixture["allocator_cap_bytes"] if fixture else 64 << 20
    jpype.startJVM(
        "-Xms32m", "-Xmx256m", "--add-opens=java.base/java.nio=ALL-UNNAMED",
        f"-Darrow.cdata.library.path={args.jni_library_dir}",
        jvmpath=args.jvm, classpath=args.classpath_file.read_text().strip().split(os.pathsep),
    )
    try:
        java_pid = jpype.JClass("java.lang.ProcessHandle").current().pid()
        assert java_pid == os.getpid(), "C Data importer must share the producer address space"
        print(json.dumps({"stage": "embedded", "python_pid": os.getpid(), "java_pid": java_pid}), file=sys.stderr)
        allocator = jpype.JClass("org.apache.arrow.memory.RootAllocator")(cap)
        try:
            if fixture:
                check_threshold(allocator, fixture)
            else:
                assert args.type, "small bridge requires --type"
                check_small(allocator, args.ipc, args.type == "large")
        finally:
            allocator.close()
    finally:
        jpype.shutdownJVM()


if __name__ == "__main__":
    main()
