"""Fixed-data CPython calls. The outer driver supplies controlling terminals and X."""
import io
import json
import os
from pathlib import Path
import subprocess
import sys


def check_call(function):
    try:
        return function()
    except Exception as error:
        return type(error).__name__


def heapq():
    from heapq import nlargest
    data = ["a", "bbb", "cc"]
    return nlargest(2, data, key=len), nlargest(0, data, key=len), {}


def imap():
    import imaplib
    import socket
    import ssl
    import threading

    fixtures = Path(os.environ["AF028_FIXTURES"])
    key = fixtures / "agent1-key.pem"
    cert = fixtures / "agent1-cert.pem"
    server = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    server.load_cert_chain(cert, key)
    server.load_verify_locations(fixtures / "ca1-cert.pem")
    server.verify_mode = ssl.CERT_REQUIRED

    def exchange(use_context=False, missing=False):
        peer = []
        exit_reason = []
        with socket.socket() as listener:
            listener.settimeout(2)
            listener.bind(("127.0.0.1", 0))
            listener.listen(1)

            def serve():
                try:
                    raw, _ = listener.accept()
                    raw.settimeout(2)
                    with server.wrap_socket(raw, server_side=True) as conn, conn.makefile("rb") as commands:
                        peer.append(bool(conn.getpeercert()))
                        conn.sendall(b"* OK AF028 IMAP fixture\r\n")
                        for line in commands:
                            tag, cmd = line.split(maxsplit=2)[:2]
                            cmd = cmd.strip().upper()
                            if cmd == b"CAPABILITY":
                                conn.sendall(b"* CAPABILITY IMAP4rev1\r\n")
                            if cmd == b"LOGOUT":
                                conn.sendall(b"* BYE closing fixture\r\n")
                            conn.sendall(tag + b" OK handled\r\n")
                            if cmd == b"LOGOUT":
                                return
                except (OSError, ValueError) as error:
                    exit_reason.append(type(error).__name__)

            thread = threading.Thread(target=serve, daemon=True)
            thread.start()

            if use_context:
                context = ssl._create_unverified_context()
                context.load_cert_chain(cert, key)
                kwargs = {"ssl_context": context}
            else:
                kwargs = {"keyfile": str(key), "certfile": "missing-cert.pem" if missing else str(cert)}
            try:
                with imaplib.IMAP4_SSL("127.0.0.1", listener.getsockname()[1], timeout=2, **kwargs) as client:
                    response = {"state": client.state, "noop": client.noop()[0],
                                "client_certificate": bool(peer and peer[0])}
            except (OSError, TypeError, ValueError, imaplib.IMAP4.error) as error:
                response = type(error).__name__
                print(repr(error), file=sys.stderr)
            # A constructor can fail before connecting. The daemon accept has a bounded timeout.
            thread.join(timeout=2.2)
        return response, exit_reason

    main, main_server = exchange()
    boundary, boundary_server = exchange(missing=True)
    context, context_server = exchange(use_context=True)
    return main, boundary, dict(context=context, server_exceptions=[main_server, boundary_server, context_server])


def loader():
    from importlib.machinery import SourceFileLoader
    path = Path("af_module.py")
    path.write_text("VALUE = 41 + 1\n")
    if not hasattr(SourceFileLoader, "load_module"):
        return "AttributeError", "AttributeError", {}
    mod = SourceFileLoader("af_module", str(path)).load_module()
    missing = check_call(SourceFileLoader("af_missing", "missing.py").load_module)
    return {"value": mod.VALUE, "registered": sys.modules["af_module"] is mod}, missing, {}


def trace():
    from trace import Trace
    name = "af_trace_fixture.py"
    code = compile("for af_i in range(2):\n    af_value = af_i\n", name, "exec")

    def count(mode):
        trace = Trace(count=mode, trace=0)
        trace.run(code)
        return [trace.results().counts.get((name, line), 0) for line in (1, 2)]

    return count(1), count(0), {}


def netrc():
    from netrc import netrc
    path = Path(os.environ["HOME"]) / ".netrc"
    path.write_text("machine fixture.invalid login dummy password pseudo-token\n")
    path.chmod(0o644)
    insecure = check_call(netrc)
    path.chmod(0o600)
    user, _, value = netrc().authenticators("fixture.invalid")
    return type(insecure).__name__ if not isinstance(insecure, str) else insecure, [user, value], {
        "euid_is_owner": path.stat().st_uid == os.geteuid(),
        "permission_comparison": ["0644", "0600"],
    }


def distutils():
    text = "ANSWER = 42\n"
    Path("af_dist_fixture.py").write_text(text)
    Path("setup.py").write_text(
        "from distutils.core import setup\n"
        "setup(name='af028fixture', version='1.0', py_modules=['af_dist_fixture'])\n"
    )

    def command(*args):
        cmd = [sys.executable, "-I", "-W", "default", "setup.py", *args]
        cp = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        print(json.dumps(dict(argv=cmd[1:], rc=cp.returncode, stdout=cp.stdout, stderr=cp.stderr)),
              file=sys.stderr)
        return cp.returncode

    def installed():
        return any(p.read_text() == text for p in Path("stage").rglob("af_dist_fixture.py"))

    build = {"build_artifact": command("build") == 0 and
             any(p.read_text() == text for p in Path("build").rglob("af_dist_fixture.py")),
             "installed": installed()}
    ok = command("install", "--root", "stage", "--prefix", "/af028") == 0 and installed()
    return ok, build, {"interpreter_isolated": bool(sys.flags.isolated)}


def pydoc():
    needle = "AF028DOCSENTINEL"
    Path("af_doc_fixture.py").write_text('"""' + needle + '"""\n')

    def docs(name):
        cp = subprocess.run([sys.executable, "-m", "pydoc", name], capture_output=True, text=True, timeout=5)
        print(json.dumps(dict(name=name, rc=cp.returncode, stdout=cp.stdout, stderr=cp.stderr)), file=sys.stderr)
        return cp.stdout + cp.stderr

    yes, no = docs("af_doc_fixture"), docs("af_nonexistent_doc_fixture")
    return needle in yes, {"sentinel": needle in no, "missing": "No Python documentation found" in no}, {}


def venv():
    import sysconfig
    from venv import EnvBuilder

    marker = "af028_std_site_fixture"
    path = Path(sysconfig.get_path("purelib")) / (marker + ".py")

    def run(value):
        folder = "venv_with" if value else "venv_without"
        EnvBuilder(system_site_packages=value).create(folder)
        cmd = [str(Path(folder) / "bin/python"), "-I", "-B", "-c", f"import {marker}; print({marker}.VALUE)"]
        cp = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        cfg = Path(folder, "pyvenv.cfg").read_text()
        print(json.dumps(dict(argv=cmd, rc=cp.returncode, stdout=cp.stdout, stderr=cp.stderr, config=cfg)),
              file=sys.stderr)
        return cp.stdout.strip() if cp.returncode == 0 else cp.stderr.splitlines()[-1].split(":")[0]

    if not path.parent.is_dir():
        raise RuntimeError("missing isolated installed base site-packages directory")
    with path.open("x") as fixture:
        fixture.write('VALUE = "af028 marker"\n')
    try:
        return run(True), run(False), {}
    finally:
        path.unlink()


def imghdr():
    def usage():
        import imghdr
        return imghdr

    mod = check_call(usage)
    if isinstance(mod, str):
        return mod, mod, {}

    def checker(header, stream):
        return "af028type" if stream is None and header == b"AF028-fixture" else None

    mod.tests.append(checker)
    try:
        return mod.what(None, h=b"AF028-fixture"), mod.what(None, h=b"AF028-other"), {}
    finally:
        mod.tests.remove(checker)


def tar():
    import tarfile
    name = "af028_" + ("long" * 31)
    data = b"AF028"

    def archive(fmt):
        out = io.BytesIO()
        with tarfile.open(fileobj=out, mode="w", **fmt) as tf:
            info = tarfile.TarInfo(name)
            info.size = len(data)
            tf.addfile(info, io.BytesIO(data))
        flag = chr(out.getvalue()[156])
        out.seek(0)
        with tarfile.open(fileobj=out, mode="r:") as tf:
            value = tf.extractfile(name).read()
        return flag, value == data

    flag, equal = archive({})
    gflag, gequal = archive({"format": tarfile.GNU_FORMAT})
    return {"default_is_pax": tarfile.DEFAULT_FORMAT == tarfile.PAX_FORMAT, "has_pax": flag == "x",
            "roundtrip": equal}, {"has_gnu": gflag == "L", "roundtrip": gequal}, {}


def winreg():
    def connect():
        import winreg
        with winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER) as handle:
            return "handle" if int(handle) else "zero handle"

    isolated = subprocess.run([sys.executable, "-S", "-c", "import winreg"], capture_output=True, text=True, timeout=6)
    print(isolated.stderr, file=sys.stderr)
    boundary = isolated.stderr.splitlines()[-1].split(":")[0] if isolated.returncode else "imported"
    return check_call(connect), boundary, {"platform": sys.platform}


def binhex():
    import binascii
    if not hasattr(binascii, "a2b_hqx"):
        return "AttributeError", "AttributeError", {}
    result, done = binascii.a2b_hqx(b"!!!!:")
    return [result.hex(), done], check_call(lambda: binascii.a2b_hqx(b"~")), {}


def site():
    def inspect(*flags):
        cp = subprocess.run([sys.executable, *flags, "-c", "print(copyright)"],
                            capture_output=True, text=True, timeout=5)
        print(json.dumps(dict(flags=flags, rc=cp.returncode, stdout=cp.stdout, stderr=cp.stderr)), file=sys.stderr)
        return cp

    result = inspect()
    no_site = inspect("-S")
    return "Copyright" in result.stdout, no_site.stderr.splitlines()[-1].split(":")[0], {}


def lasttype():
    statements = ('import sys; print("FIRST", hasattr(sys, "last_type"))\n'
                  'raise ValueError("af028 fixture")\n'
                  'print("LAST", sys.last_type.__name__)\n'
                  'exit()\n')
    cp = subprocess.run([sys.executable, "-I", "-i", "-q"], input=statements,
                        capture_output=True, text=True, timeout=7)
    print(cp.stderr, file=sys.stderr)
    print(cp.stdout, file=sys.stderr)
    last = next((line.split()[-1] for line in cp.stdout.splitlines() if line.startswith("LAST ")), None)
    return {"type": last, "traceback": "ValueError: af028 fixture" in cp.stderr}, "FIRST True" in cp.stdout, {
        "rc": cp.returncode
    }


PROBES = {fun.__name__: fun for fun in (heapq, imap, loader, trace, netrc, distutils, pydoc, venv,
                                        imghdr, tar, winreg, binhex, site, lasttype)}
if __name__ == "__main__":
    positive, boundary, diagnostic = PROBES[sys.argv[1]]()
    print("AF028_JSON " + json.dumps(dict(positive=positive, boundary=boundary, diagnostic=diagnostic)))
