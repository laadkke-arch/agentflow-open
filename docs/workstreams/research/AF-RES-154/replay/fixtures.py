import argparse
import hashlib
import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from tempfile import TemporaryDirectory

from PIL import Image, ImageDraw, ImageFont
from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter
from pyhanko.pdf_utils.reader import PdfFileReader
from pyhanko.sign import fields, signers, validation
from pyhanko_certvalidator import ValidationContext
from pyhanko.keys import load_cert_from_pemder
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen.canvas import Canvas


NAMES = {
    "UT": "ut-text.pdf",
    "UI": "ui-image.pdf",
    "ST": "st-signed-text.pdf",
    "SI": "si-signed-image.pdf",
    "WT": "wt-write-retry.pdf",
}
TEXT = (
    "AgentFlow synthetic invoice QA",
    "Reference Alpha Seven Four Two",
    "The original must remain readable after the transfer.",
    "Please retain the unmodified document for review.",
)
TITLE = b"AF154 QA Immutable Title A"


def command(*args, cwd=None):
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True, check=False, timeout=90)


def checked(*args, cwd=None):
    result = command(*args, cwd=cwd)
    result.check_returncode()
    return result.stdout


def fingerprint(data):
    return {"sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}


def described_command(result):
    return {
        "argv": [str(arg) for arg in result.args],
        "exit_code": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


def inspect_pdf(path, root, moment):
    signature_profiles = {}
    for name, roots in (("fixture_ca", [root]), ("no_anchors", [])):
        with path.open("rb") as pdf:
            reader = PdfFileReader(pdf)
            signatures = []
            for sig in reader.embedded_signatures:
                context = ValidationContext(
                    trust_roots=roots, moment=moment, allow_fetching=False
                )
                status = validation.validate_pdf_signature(sig, signer_validation_context=context)
                signatures.append({
                    "intact": status.intact,
                    "valid": status.valid,
                    "trusted": status.trusted,
                    "coverage": status.coverage.name,
                    "docmdp_ok": status.docmdp_ok,
                    "signer_cert_sha256": status.signing_cert.sha256.hex(),
                })
            signature_profiles[name] = signatures
    sig_output = command("pdfsig", "-nocert", path)
    text_output = command("pdftotext", "-layout", path, "-")
    text_output.check_returncode()
    pages = text_output.stdout.split("\f")
    if pages and pages[-1] == "":
        pages.pop()
    return {
        **fingerprint(path.read_bytes()),
        "signatures": signature_profiles,
        "pdfsig": described_command(sig_output),
        "pdftotext": described_command(text_output),
        "page_text": [page.strip() for page in pages],
    }


def draw_pdf(path, title, raster):
    canvas = Canvas(str(path), pagesize=(612, 792), invariant=1, pageCompression=0)
    canvas.setTitle(title)
    if raster:
        image = Image.new("RGB", (1700, 2200), "white")
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default(size=53)
        for i, line in enumerate(TEXT):
            draw.text((120, 165 + 94 * i), line, fill="black", font=font)
        canvas.drawImage(ImageReader(image), 0, 0, width=612, height=792)
    else:
        canvas.setFont("Helvetica", 15)
        for i, line in enumerate(TEXT):
            canvas.drawString(48, 735 - 25 * i, line)
    canvas.showPage()
    canvas.save()


def sign_fixtures(folder):
    with TemporaryDirectory(prefix="af154-sign-") as temp:
        temp = Path(temp)
        root_key, signer_key = temp / "ca.key", temp / "signer.key"
        csr, signer_cert, extensions = temp / "signer.csr", temp / "signer.pem", temp / "x509.cnf"
        root_cert = folder / "qa-root.crt"
        checked(
            "openssl", "req", "-x509", "-newkey", "rsa:2048", "-nodes", "-days", "3650",
            "-subj", "/CN=AF154 Synthetic QA Root", "-keyout", root_key, "-out", root_cert,
            "-addext", "basicConstraints=critical,CA:TRUE,pathlen:0",
            "-addext", "keyUsage=critical,keyCertSign,cRLSign",
        )
        checked(
            "openssl", "req", "-new", "-newkey", "rsa:2048", "-nodes",
            "-subj", "/CN=AF154 Synthetic QA Signer", "-keyout", signer_key, "-out", csr,
        )
        extensions.write_text(
            "basicConstraints=critical,CA:FALSE\n"
            "keyUsage=critical,digitalSignature,nonRepudiation\n"
            "subjectKeyIdentifier=hash\n"
            "authorityKeyIdentifier=keyid,issuer\n",
        )
        checked(
            "openssl", "x509", "-req", "-in", csr, "-CA", root_cert, "-CAkey", root_key,
            "-set_serial", "15401", "-days", "3650", "-sha256", "-extfile", extensions,
            "-out", signer_cert,
        )
        signer = signers.SimpleSigner.load(
            str(signer_key), str(signer_cert), ca_chain_files=(str(root_cert),),
        )
        if signer is None:
            raise RuntimeError("Could not load synthetic signer")
        for plain, signed in (("UT", "ST"), ("UI", "SI")):
            with (folder / NAMES[plain]).open("rb") as source, (folder / NAMES[signed]).open("wb") as target:
                writer = IncrementalPdfFileWriter(source)
                signers.sign_pdf(
                    writer,
                    signers.PdfSignatureMetadata(field_name="AF154SyntheticSignature"),
                    signer=signer,
                    new_field_spec=fields.SigFieldSpec(sig_field_name="AF154SyntheticSignature"),
                    output=target,
                )
    moment = datetime.now(UTC).replace(microsecond=0)
    (folder / "validation-time.txt").write_text(moment.isoformat() + "\n")
    signed_bytes = (folder / NAMES["ST"]).read_bytes()
    before, title, after = signed_bytes.rpartition(TITLE)
    if not title:
        raise RuntimeError("Missing metadata title inside signed bytes")
    (folder / "invalid-metadata-control.pdf").write_bytes(before + title[:-1] + b"B" + after)


def inspect_inputs(folder, ledger):
    root = load_cert_from_pemder(str(folder / "qa-root.crt"))
    moment = datetime.fromisoformat((folder / "validation-time.txt").read_text().strip())
    rows = []
    names = {**NAMES, "INVALID": "invalid-metadata-control.pdf"}
    for key, name in names.items():
        output = inspect_pdf(folder / name, root, moment)
        signed = key in {"ST", "SI", "INVALID"}
        raster = key in {"UI", "SI"}
        sources = ["T03", "T04"]
        if raster:
            sources.append("T05")
        if signed:
            sources.extend(("T06", "X05"))
        if len(output["page_text"]) != 1 or bool(output["page_text"][0]) == raster:
            raise RuntimeError(f"{key} unexpected page text")
        profiles = output["signatures"]
        if key in {"ST", "SI"}:
            trusted, = profiles["fixture_ca"]
            untrusted, = profiles["no_anchors"]
            if not (trusted["intact"] and trusted["valid"] and trusted["trusted"]
                    and trusted["coverage"] == "ENTIRE_FILE"
                    and untrusted["intact"] and untrusted["valid"] and not untrusted["trusted"]):
                raise RuntimeError(f"{key} failed signature preflight")
        elif key == "INVALID":
            altered, = profiles["fixture_ca"]
            if altered["intact"]:
                raise RuntimeError("Tampered control unexpectedly intact")
        elif profiles["fixture_ca"]:
            raise RuntimeError(f"{key} unexpectedly signed")
        rows.append({
            "fixture_id": key,
            "file": f"replay/fixtures/{name}",
            "usage": "matrix" if key in {"UT", "UI", "ST", "SI"} else "control",
            "generator": "metadata byte control after signing" if key == "INVALID"
                         else "Canvas raster image" if raster else "Canvas selectable text",
            "source_ids": sources,
            "qa_ca_sha256": root.sha256.hex(),
            "verification_time": moment.isoformat(),
            "extractable": not raster,
            "signed": signed,
            **output,
        })
    ledger.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixtures", required=True, type=Path)
    parser.add_argument("--ledger", required=True, type=Path)
    parser.add_argument("--generate", action="store_true")
    args = parser.parse_args()
    folder = args.fixtures.resolve()
    if args.generate:
        folder.mkdir(parents=True, exist_ok=False)
        draw_pdf(folder / NAMES["UT"], TITLE.decode(), raster=False)
        draw_pdf(folder / NAMES["UI"], "AF154 QA Raster Invoice", raster=True)
        draw_pdf(folder / NAMES["WT"], "AF154 QA Store-Retry Invoice", raster=False)
        sign_fixtures(folder)
    inspect_inputs(folder, args.ledger)


if __name__ == "__main__":
    main()
