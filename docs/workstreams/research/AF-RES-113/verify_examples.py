"""Post-seal checks of explicit constructed inputs, not full project acceptance.

The source fragment is the unmodified __affinity_bandwidth function from the
fixed librosa commit. Only its function definition is compiled. ParameterError
is a local stand-in class; the surrounding public recurrence API is not run.
No original MKV, tokenizer, s390x machine, or full skimage installation is used.
"""
from __future__ import annotations

import ast
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import urllib.request

import numpy as np
import scipy
from scipy import ndimage, sparse

ROOT = Path(__file__).resolve().parent
SOURCE_URL = (
    "https://raw.githubusercontent.com/librosa/librosa/"
    "9caf46a4ecaeb8ea24bb541231065c9f761174ae/librosa/segment.py"
)


def main():
    source_cache = ROOT / "evidence/cache/LIB-COMMON-RECURRENCE-DOCSTRING.raw"
    if source_cache.exists():
        raw = source_cache.read_bytes()
        retrieval = "previously fetched fixed source cache"
    else:
        with urllib.request.urlopen(SOURCE_URL, timeout=35) as response:
            raw = response.read()
        retrieval = "new fetch of fixed source"
    assert hashlib.sha256(raw).hexdigest() == "6f5fc0aa99569f0e1d2f1d42d82b12eb49158243f4736d76b6c26408c0f97f5f", "fixed source bytes changed"
    tree = ast.parse(raw.decode())
    fn = next(
        n for n in tree.body
        if isinstance(n, ast.FunctionDef) and n.name == "__affinity_bandwidth"
    )
    future = ast.ImportFrom(
        module="__future__", names=[ast.alias(name="annotations")], level=0
    )
    module = ast.fix_missing_locations(ast.Module(body=[future, fn], type_ignores=[]))
    local_error = type("ParameterError", (ValueError,), {})
    env = {"np": np, "scipy": scipy, "ParameterError": local_error}
    exec(compile(module, SOURCE_URL, "exec"), env)
    affinity = env["__affinity_bandwidth"]
    graph = sparse.csr_array([[0.0, 0.1, 0.0], [0.1, 0.0, 0.0], [0.0, 0.0, 0.0]])
    graph_results = []
    for name, value, mode in [
        ("partial-med", graph, "med_k_scalar"),
        ("partial-mean", graph, "mean_k"),
        ("partial-gmean", graph, "gmean_k"),
        ("all-empty-med", sparse.csr_array((3, 3)), "med_k_scalar"),
    ]:
        try:
            result = affinity(value, mode, 1)
            graph_results.append({"input_id": name, "value": float(result)})
        except local_error as exc:
            graph_results.append({"input_id": name, "error": str(exc)})

    image = np.array([[7]], dtype=np.uint8)
    footprint = np.array([[1, 0, 1]], dtype=bool)
    boundary = {
        "reflect": ndimage.grey_dilation(image, footprint=footprint, mode="reflect").tolist(),
        "dtype_min": ndimage.grey_dilation(image, footprint=footprint, mode="constant", cval=0).tolist(),
        "literal_doc_max": ndimage.grey_dilation(image, footprint=footprint, mode="constant", cval=255).tolist(),
    }
    block_length, frame_length, hop = 256, 4096, 1024
    samples = (block_length - 1) * hop + frame_length
    default_starts = list(range(0, samples - 2048 + 1, 512))
    aligned_starts = list(range(0, samples - frame_length + 1, hop))
    advance = block_length * hop
    frames = {
        "samples_in_full_stream_block": samples,
        "block_advance": advance,
        "default_stft_frames": len(default_starts),
        "aligned_stft_frames": len(aligned_starts),
        "duplicate_starts_across_two_full_blocks_default": sorted(set(default_starts) & {advance + v for v in default_starts}),
        "duplicate_starts_across_two_full_blocks_aligned": sorted(set(aligned_starts) & {advance + v for v in aligned_starts}),
    }
    assert graph_results[0]["value"] == 0.1
    assert "no neighbors" in graph_results[1]["error"]
    assert "no neighbors" in graph_results[2]["error"]
    assert "empty graph" in graph_results[3]["error"]
    assert boundary == {"reflect": [[7]], "dtype_min": [[0]], "literal_doc_max": [[255]]}
    assert frames["default_stft_frames"] == 515 and frames["aligned_stft_frames"] == 256
    assert len(frames["duplicate_starts_across_two_full_blocks_default"]) == 3
    assert not frames["duplicate_starts_across_two_full_blocks_aligned"]
    result = {
        "checked_utc": datetime.now(timezone.utc).isoformat(),
        "phase": "postseal_verification",
        "reader": "root",
        "python": platform.python_version(),
        "numpy": np.__version__, "scipy": scipy.__version__,
        "installed_target_libraries": {x: importlib.util.find_spec(x) is not None for x in ["librosa", "skimage"]},
        "source_url": SOURCE_URL, "source_sha256": hashlib.sha256(raw).hexdigest(),
        "source_lines": [fn.lineno, fn.end_lineno], "source_retrieval": retrieval,
        "R1_window_arithmetic": frames,
        "R3_isolated_source_function": graph_results,
        "R5_scipy_backend": boundary,
        "limitations": [
            "Window starts are arithmetic, not an audio decode or full STFT execution.",
            "R3 uses a supplied CSR graph and a local exception class; public recurrence graph construction is not executed.",
            "R5 executes the installed SciPy backend on a symmetric odd footprint, not the complete fixed skimage API.",
            "No original MKV, tokenizer, original Csync, 64-bit morphology exhaustive input, or s390x regression was executed.",
            "These constructed inputs are post-seal verification; none is an extra-link discovery.",
        ],
    }
    output = ROOT / "evidence/verification/project/executed-checks.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
