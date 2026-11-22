"""Send real execute requests to a minimal ipykernel Kernel subclass."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
from time import monotonic

import ipykernel
from ipykernel.kernelapp import IPKernelApp
from ipykernel.kernelbase import Kernel
from jupyter_client import BlockingKernelClient, write_connection_file
import jupyter_client
import nbformat


ABSENT = object()


class Receiver(Kernel):
    implementation = "af-res-031"
    implementation_version = "1"
    language = "synthetic"
    language_info = {"name": language, "mimetype": "text/plain", "file_extension": ".txt"}
    banner = "AF-RES-031 receiver"

    def do_execute(
        self, code, silent, store_history=True, user_expressions=None, allow_stdin=False,
        *, cell_meta=ABSENT, cell_id=ABSENT,
    ):
        parent = self.get_parent()
        data = {
            "request_id": parent["header"]["msg_id"],
            "code": code,
            "wire_root": parent["metadata"],
            "has_wire_content_metadata": "metadata" in parent["content"],
            "wire_content_metadata": parent["content"].get("metadata"),
            "cell_meta_supplied": cell_meta is not ABSENT,
            "cell_meta": None if cell_meta is ABSENT else cell_meta,
            "cell_id_supplied": cell_id is not ABSENT,
            "cell_id": None if cell_id is ABSENT else cell_id,
        }
        with Path("received.jsonl").open("a", encoding="utf-8") as output:
            output.write(json.dumps(data, sort_keys=True) + "\n")
        return {"status": "ok", "execution_count": self.execution_count, "payload": [], "user_expressions": {}}


def compare(child, label, msg_id, expected_wire, expected_kwargs, received):
    assert child.poll() is None
    assert received["request_id"] == msg_id, received
    assert received["code"] == label, received
    assert received["wire_root"] == expected_wire[0], received
    assert received["has_wire_content_metadata"] == (expected_wire[1] is not None), received
    assert received["wire_content_metadata"] == expected_wire[1], received
    assert received["cell_meta_supplied"] == expected_kwargs[0], received
    assert received["cell_meta"] == expected_kwargs[1], received
    assert received["cell_id_supplied"] == expected_kwargs[2], received
    assert received["cell_id"] == expected_kwargs[3], received


def run(fixture, version):
    assert ipykernel.__version__ == version, ipykernel.__version__
    assert jupyter_client.__version__ == "8.6.0", jupyter_client.__version__
    notebook = nbformat.v4.new_notebook(
        cells=[nbformat.v4.new_code_cell("notebook_only", id="af031-file-id", metadata=fixture["notebook"])]
    )
    nbformat.write(notebook, "fixture.ipynb")
    cell = nbformat.read("fixture.ipynb", as_version=4).cells[0]
    assert dict(cell.metadata) == fixture["notebook"], cell.metadata
    write_connection_file("connection.json", ip="127.0.0.1", key=os.urandom(32).hex().encode("ascii"))
    client = BlockingKernelClient(connection_file=str(Path("connection.json").resolve()))
    client.load_connection_file()
    with Path("kernel.stdout").open("wb") as stdout, Path("kernel.stderr").open("wb") as stderr:
        child = subprocess.Popen(
            [sys.executable, "-B", str(Path(__file__).resolve()), "--receiver", "connection.json"],
            stdout=stdout, stderr=stderr,
        )
        try:
            client.start_channels()
            client.wait_for_ready(timeout=20)
            print(json.dumps({"stage": "ready", "kernel": version, "client": jupyter_client.__version__}), flush=True)
            shapes = {
                "both": (fixture["root"], fixture["content"]),
                "root_only": (fixture["root"], None),
                "content_only": ({}, fixture["content"]),
                "neither": ({}, None),
                "notebook_only": ({}, None),
                "adapter": (dict(cell.metadata), None),
            }
            assert shapes["adapter"][0] == fixture["notebook"]
            for label in fixture["cases"]:
                root, content_metadata = shapes[label]
                code = cell.source if label == "notebook_only" else label
                if label in ("neither", "notebook_only"):
                    msg_id = client.execute(code, silent=True, store_history=False, allow_stdin=False)
                else:
                    content = {
                        "code": code, "silent": True, "store_history": False,
                        "user_expressions": {}, "allow_stdin": False, "stop_on_error": True,
                    }
                    if content_metadata is not None:
                        content["metadata"] = content_metadata
                    message = client.session.msg("execute_request", content=content, metadata=dict(root))
                    client.shell_channel.send(message)
                    msg_id = message["header"]["msg_id"]
                print(json.dumps({"stage": "sent", "label": label, "request_id": msg_id}), file=sys.stderr, flush=True)
                deadline = monotonic() + 10
                while True:
                    reply = client.get_shell_msg(timeout=max(0.0, deadline - monotonic()))
                    if reply.get("parent_header", {}).get("msg_id") == msg_id:
                        break
                assert reply["msg_type"] == "execute_reply" and reply["content"]["status"] == "ok", reply["content"]
                received = json.loads(Path("received.jsonl").read_text().splitlines()[-1])
                enabled = version == "6.27.0"
                expected = (enabled, root if enabled else None, True, root.get("cellId"))
                compare(child, code, msg_id, (root, content_metadata), expected, received)
                print(
                    json.dumps({"stage": "reply_joined", "label": label, "request_id": msg_id,
                                "reply_parent_id": reply["parent_header"]["msg_id"], "status": "ok"}),
                    file=sys.stderr, flush=True,
                )
                del received["request_id"]
                print(json.dumps({"label": label, **received}, sort_keys=True), flush=True)
        finally:
            client.stop_channels()
            child.terminate()
            try:
                child.wait(timeout=10)
            except subprocess.TimeoutExpired:
                child.kill()
                child.wait()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receiver")
    parser.add_argument("--version", choices=("6.26.0", "6.27.0"))
    parser.add_argument("--fixture", type=Path)
    args = parser.parse_args()
    if args.receiver:
        IPKernelApp.launch_instance(argv=["-f", args.receiver], kernel_class=Receiver)
    else:
        run(json.loads(args.fixture.read_bytes())["jupyter"], args.version)
