"""Run released yq builds and independently read the emitted YAML nodes."""
import platform
import yaml

from fixtures import blob, catalog
from harness import Probe, options, runtime

LOCALE = "C.UTF-8"
MERGE = ". as $item ireduce ({}; . * $item )"
LOAD = '.values |= load_str("2.yaml")'


def node_metadata(node):
    record = {"tag": node.tag, "kind": node.id}
    if isinstance(node, yaml.ScalarNode):
        record.update(value=node.value, style=node.style)
    elif isinstance(node, yaml.SequenceNode):
        record.update(items=[node_metadata(child) for child in node.value], flow=node.flow_style)
    else:
        record.update(items=[[node_metadata(key), node_metadata(value)] for key, value in node.value], flow=node.flow_style)
    return record


def read_nodes(output):
    contents = {}
    try:
        loader = yaml.CSafeLoader
        contents["nodes"] = [node_metadata(node) for node in yaml.compose_all(output, Loader=loader)]
        contents["values"] = list(yaml.load_all(output, Loader=loader))
    except yaml.YAMLError as error:
        contents["parse_error"] = str(error)
    return contents


def parser_identity(info):
    if not yaml.__with_libyaml__ or yaml.__version__ != "6.0.2":
        raise ValueError("Expected PyYAML 6.0.2 with libyaml")
    return {**info, "independent_reader": f"PyYAML {yaml.__version__} CSafeLoader", "reader_python": platform.python_version()}


def fixture_data(fixture, name):
    return bytes.fromhex(fixture["files"][name]["hex"])


def merges(fixtures, opts):
    upstream = {
        "null-times-map": 'null * {"some": "thing"}',
        "map-times-null": '{"some": "thing"} * null',
        "null-times-array": 'null * ["some"]',
        "array-times-null": '["some"] * null',
        "null-times-null": "null * null",
    }
    for version in ("4.30.5", "4.30.6", "4.30.7"):
        bin_dir, info = runtime(opts.installation, "yq", version)
        info = parser_identity(info)
        for fixture in fixtures:
            if fixture["source_id"] == "R-Y2-null":
                for name, expression in upstream.items():
                    probe = Probe(fixture, name, version, LOCALE, opts.workspace, bin_dir, info)
                    output, rc = probe.command("yq_linux_amd64", "--null-input", expression)
                    probe.finish(read_nodes(output) if rc == 0 else {})
                continue
            variants = [("merge", MERGE)]
            if fixture["id"] in {"y2-lf3", "y2-null"}:
                variants.append(("drop-top-level-null", 'select(tag != "!!null") | ' + MERGE))
            for name, expression in variants:
                probe = Probe(fixture, name, version, LOCALE, opts.workspace, bin_dir, info)
                output, rc = probe.command("yq_linux_amd64", "ea", expression, "blank.yaml", "notempty.yaml")
                parsed = {"inputs": {name: read_nodes(fixture_data(fixture, name)) for name in fixture["files"]}}
                if rc == 0:
                    parsed["output"] = read_nodes(output)
                probe.finish(parsed)


def char_metrics(value):
    return {
        "length": len(value), "codepoints": [f"U+{ord(char):04X}" for char in value],
        "CR": value.count("\r"), "LF": value.count("\n"),
        "terminal": "CRLF" if value.endswith("\r\n") else "LF" if value.endswith("\n") else "none",
    }


def loads(fixtures, opts):
    version = "4.30.6"
    bin_dir, info = runtime(opts.installation, "yq", version)
    info = parser_identity(info)
    default_variants = [
        ("default", []), ("literal", []), ("flow", []), ("lf-copy", []), ("in-place", ["-i"]),
    ]
    for fixture in fixtures:
        payload = fixture_data(fixture, "2.yaml")
        for name, flags in default_variants:
            probe = Probe(fixture, name, version, LOCALE, opts.workspace, bin_dir, info)
            expression = LOAD
            source = payload
            parsed = {"original_string": char_metrics(payload.decode())}
            if name in {"literal", "flow"}:
                expression += f' | .values style="{name}"'
            if name == "lf-copy":
                source = payload.replace(b"\r\n", b"\n")
                (probe.directory / "2-normalized.yaml").write_bytes(source)
                parsed["derived_input"] = {"path": "2-normalized.yaml", **blob(source)}
                expression = LOAD.replace("2.yaml", "2-normalized.yaml") + ' | .values style="literal"'
            stdout, rc = probe.command("yq_linux_amd64", *flags, expression, "1.yml")
            if rc == 0:
                output = (probe.directory / "1.yml").read_bytes() if flags else stdout
                parsed["output"] = read_nodes(output)
                values = parsed["output"].get("values")
                if values and isinstance(values[0].get("values"), str):
                    value = values[0]["values"]
                    parsed["scalar"] = {"value": value, **char_metrics(value),
                                        "equals_original_bytes": value.encode() == payload,
                                        "equals_loaded_bytes": value.encode() == source}
            probe.finish(parsed)


def arrays(fixtures, opts):
    version = "4.30.6"
    bin_dir, info = runtime(opts.installation, "yq", version)
    info = parser_identity(info)
    variants = (
        ("prepend", '["a"] + .'),
        ("prepend-assign", '. = ["a"] + .'),
        ("append", '. += "a"'),
        ("replace", '.[0] = "a"'),
    )
    for fixture in fixtures:
        data = fixture_data(fixture, "data1.yaml")
        for name, expression in variants:
            probe = Probe(fixture, name, version, LOCALE, opts.workspace, bin_dir, info)
            output, rc = probe.command("yq_linux_amd64", expression, "data1.yaml")
            parsed = {"input": read_nodes(data)}
            if rc == 0:
                reread = read_nodes(output)
                parsed.update(output=reread, same_input_bytes=data == output,
                              matches_requested_order=reread.get("values") == [["a", "b", "c", "d"]])
            probe.finish(parsed)


if __name__ == "__main__":
    opts = options(__doc__)
    fixtures = catalog()
    merges([row for row in fixtures if row["case"] == "Y2"], opts)
    loads([row for row in fixtures if row["case"] == "Y3"], opts)
    arrays([row for row in fixtures if row["case"] == "Y4"], opts)
