"""Exercise released consumer paths with fixed normal and boundary inputs."""

import argparse
import ast
import hashlib
import json
import os
import platform
import runpy
from pathlib import Path

import numpy as np
import scipy
import skimage


def summarize(array):
    values = np.asarray(array)
    return {
        "type": type(array).__name__,
        "shape": list(values.shape),
        "dtype": str(values.dtype),
        "minimum": float(values.min()),
        "maximum": float(values.max()),
        "sum": float(values.sum()),
        "values": values.tolist() if values.size < 25 else None,
    }


def gap(a, b):
    return float(np.max(np.abs(np.asarray(a) - np.asarray(b))))


def pixels(spec, repeat):
    from skimage.graph import central_pixel, pixel_graph

    mask = np.array(spec["mask"], dtype=bool)
    expected = np.array(spec["expected_adjacency"])
    nodes_expected = spec["expected_nodes"]
    modes = {"default": {}, "matrix": {"sparse_type": "matrix"}, "array": {"sparse_type": "array"}}
    outputs, rows = {}, []
    for name, settings in modes.items():
        values = [pixel_graph(mask, connectivity=spec["connectivity"], **settings) for _ in range(repeat)]
        graph, nodes = values[0]
        dense = graph.toarray()
        assert np.array_equal(dense, expected)
        assert np.array_equal(nodes, nodes_expected)
        assert all(type(g) is type(graph) and np.array_equal(g.toarray(), dense)
                   and np.array_equal(n, nodes) for g, n in values)
        assert type(graph).__name__ == ("csr_array" if name == "array" else "csr_matrix")
        center, total_lengths = central_pixel(graph, nodes, shape=mask.shape)
        outputs[name] = (graph, dense)
        rows.append({
            "case": name, "input": "pixel_graph.mask", "nodes": nodes.tolist(),
            "graph_type": type(graph).__name__, "adjacency": summarize(dense),
            "star": summarize((graph * graph).toarray()), "at": summarize((graph @ graph).toarray()),
            "center_pixel": list(map(int, center)), "path_sums": total_lengths.tolist(),
            "repeat_count": repeat, "repeat_equal": True,
        })
    matrix, mdense = outputs["matrix"]
    array, adense = outputs["array"]
    assert np.array_equal((matrix @ matrix).toarray(), (array @ array).toarray())
    assert not np.array_equal((matrix * matrix).toarray(), (array * array).toarray())
    rows.append({
        "case": "matrix-array-delta", "input": "pixel_graph.mask",
        "adjacency_linf": gap(mdense, adense),
        "star_linf": gap((matrix * matrix).toarray(), (array * array).toarray()),
        "at_linf": gap((matrix @ matrix).toarray(), (array @ array).toarray()),
    })
    errors = []
    for _ in range(repeat):
        try:
            pixel_graph(mask, connectivity=spec["connectivity"], sparse_type=spec["invalid_sparse_type"])
        except ValueError as err:
            errors.append(str(err))
    assert len(errors) == repeat and len(set(errors)) == 1
    rows.append({"case": "invalid", "input": "pixel_graph.mask", "sparse_type": spec["invalid_sparse_type"],
                 "exception": "ValueError", "message": errors[0], "repeat_count": repeat, "repeat_equal": True})
    dia = scipy.sparse.dia_array(([1, 2, 3], 1), shape=(3, 3))
    diagonals = scipy.sparse.diags([1, 2, 3], 1, shape=(3, 3))
    rows.append({
        "case": "off-diagonal", "input": "values [1, 2, 3], offset 1, shape (3, 3)",
        "dia_array": summarize(dia.toarray()), "diags_matrix": summarize(diagonals.toarray()),
        "diags_array_available": hasattr(scipy.sparse, "diags_array"),
    })
    return rows


def legacy_pixels(spec, repeat):
    from skimage.graph import pixel_graph

    mask = np.array(spec["mask"], dtype=bool)
    results = [pixel_graph(mask, connectivity=spec["connectivity"]) for _ in range(repeat)]
    graph, nodes = results[0]
    dense = graph.toarray()
    assert type(graph).__name__ == "csr_matrix"
    assert np.array_equal(dense, spec["expected_adjacency"])
    assert np.array_equal(nodes, spec["expected_nodes"])
    assert all(np.array_equal(other.toarray(), dense) and np.array_equal(other_nodes, nodes)
               for other, other_nodes in results)
    errors = []
    for _ in range(repeat):
        try:
            pixel_graph(mask, sparse_type="array")
        except TypeError as err:
            errors.append(str(err))
    assert len(errors) == repeat and len(set(errors)) == 1
    return [
        {"case": "legacy-default", "input": "pixel_graph.mask", "graph_type": type(graph).__name__,
         "nodes": nodes.tolist(), "adjacency": summarize(dense),
         "star": summarize((graph * graph).toarray()), "at": summarize((graph @ graph).toarray()),
         "repeat_count": repeat, "repeat_equal": True},
        {"case": "legacy-array", "input": "pixel_graph.mask", "exception": "TypeError",
         "message": errors[0], "repeat_count": repeat, "repeat_equal": True},
    ]


def load_gallery_nodes(path):
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    normalize = next(item for item in tree.body if isinstance(item, ast.AugAssign)
                     and isinstance(item.target, ast.Name) and item.target.id == "astro_noisy")
    call = next(item for item in tree.body if isinstance(item, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id == "deconvolved_RL" for t in item.targets))
    assert isinstance(call.value, ast.Call)
    return normalize, call


def image_case(path, spec, repeat, original):
    os.environ["MPLBACKEND"] = "Agg"
    from skimage.restoration import richardson_lucy

    image = np.array(spec["post_noise_image"], dtype=np.float64)
    psf = np.array(spec["psf_numerators"], dtype=np.float64) / spec["psf_divisor"]
    control = image / spec["control_divisor"]
    assert psf.sum() == 1.0 and control.max() == 1.0
    rows, outputs = [], {}
    if original:
        example = runpy.run_path(str(path))
        native = example["deconvolved_RL"]
        repeated = richardson_lucy(example["astro_noisy"], example["psf"], num_iter=spec["num_iter"])
        assert np.array_equal(repeated, native)
        rows.append({
            "case": "unmodified-gallery", "input": "released astronaut example and unseeded Poisson",
            "ast_extraction": False, "rng_seed": None, "input_max": float(example["astro_noisy"].max()),
            "output": summarize(native), "repeat_count": repeat, "repeat_equal": True,
        })
    for axis, input_image in (("control", control), ("boundary", image)):
        for normalize in (False, True):
            for clip in (False, True):
                normalization, call = load_gallery_nodes(path)
                iterations = next(k.value.value for k in call.value.keywords if k.arg == "num_iter")
                assert iterations == spec["num_iter"]
                assert all(k.arg != "clip" for k in call.value.keywords)
                call.value.keywords.append(ast.keyword(arg="clip", value=ast.Constant(clip)))
                nodes = [normalization, call] if normalize else [call]
                program = compile(ast.fix_missing_locations(ast.Module(body=nodes, type_ignores=[])),
                                  str(path), "exec")
                repeated_outputs = []
                for _ in range(repeat):
                    context = {"np": np, "ski": skimage, "psf": psf.copy(), "astro_noisy": input_image.copy()}
                    exec(program, context)
                    repeated_outputs.append(context["deconvolved_RL"])
                output = repeated_outputs[0]
                assert all(np.array_equal(output, value) for value in repeated_outputs)
                default_gap = None
                if clip:
                    default = richardson_lucy(context["astro_noisy"], psf, num_iter=iterations)
                    default_gap = gap(output, default)
                    assert default_gap == 0.0 and output.max() <= 1.0 and output.min() >= -1.0
                outputs[axis, normalize, clip] = output
                rows.append({
                    "case": axis, "input": "richardson_lucy.post_noise_image", "normalize": normalize,
                    "clip": clip, "psf_shape": list(psf.shape), "num_iter": iterations,
                    "input_max": float(context["astro_noisy"].max()), "output": summarize(output),
                    "delta_default": default_gap, "repeat_count": repeat, "repeat_equal": True,
                })
    for row in rows:
        if row["case"] in ("control", "boundary"):
            reference = outputs[row["case"], True, True]
            current = outputs[row["case"], row["normalize"], row["clip"]]
            row["delta_normalize_true_clip_true"] = gap(current, reference)
    assert gap(outputs["control", False, True], outputs["control", True, True]) == 0.0
    assert gap(outputs["boundary", False, False], outputs["boundary", True, True]) > 0.0
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("axis", choices=("sparse", "sparse-before", "image"))
    parser.add_argument("inputs", type=Path)
    parser.add_argument("--gallery", type=Path, help="plot_deconvolution.py extracted from the pinned sdist")
    parser.add_argument("--run-original", action="store_true", help="run the complete published gallery example")
    args = parser.parse_args()
    specs = json.loads(args.inputs.read_text())
    if args.axis == "image" and args.gallery is None:
        parser.error("--gallery is required for image")
    receipt = {
        "python": platform.python_version(), "platform": platform.platform(),
        "numpy": np.__version__, "scipy": scipy.__version__, "scikit_image": skimage.__version__,
        "axis": args.axis, "input_sha256": hashlib.sha256(args.inputs.read_bytes()).hexdigest(),
    }
    if args.axis == "image":
        receipt["gallery_sha256"] = hashlib.sha256(args.gallery.read_bytes()).hexdigest()
        receipt["rows"] = image_case(args.gallery, specs["richardson_lucy"], specs["repetitions"], args.run_original)
    elif args.axis == "sparse-before":
        receipt["rows"] = legacy_pixels(specs["pixel_graph"], specs["repetitions"])
    else:
        receipt["rows"] = pixels(specs["pixel_graph"], specs["repetitions"])
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
