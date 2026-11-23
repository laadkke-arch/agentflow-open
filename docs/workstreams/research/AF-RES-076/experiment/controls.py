"""Run fixed-edition positive/negative controls and two contextual probes."""
import io
import json
import platform
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

import duckdb
from PIL import Image, ImageColor, __version__ as pillow_version, features

assert pillow_version == "12.0.0"
assert duckdb.__version__ == "1.4.3"

DUCK = "https://github.com/duckdb/duckdb/blob/d1dc88f950d456d72493df452dabdcd13aa413dd/"
PILLOW = "https://github.com/python-pillow/Pillow/blob/693df7b42c666f88c719f9973be0ad71607328e0/"


def row(test, request, target, source, fixture, expected, observed, c1, c2, kind):
    assert observed == expected, (test, expected, observed)
    return {
        "id": test, "request": request, "candidate": target, "kind": kind, "source_url": source,
        "fixture": fixture, "expected": expected, "observed": observed, "c1": c1, "c2": c2,
    }


def thumbnail():
    im = Image.new("L", (256, 128))
    im.thumbnail((100, 100))
    size = list(im.size)
    return row("T-01", "CP01", "P01", PILLOW + "Tests/test_image_thumbnail.py#L24-L47",
               "Upstream test_aspect subcase L 256x128, thumbnail bound 100x100.",
               [100, 50], size, size[0] == 2 * size[1], max(size) <= 100, "positive")


def color():
    colors = ["#f00", "#ff0000cc"]
    observed = [list(ImageColor.getrgb(color)) for color in colors]
    return row("T-02", "CP02", "P04", PILLOW + "Tests/test_imagecolor.py#L8-L29",
               colors, [[255, 0, 0], [255, 0, 0, 204]], observed, True, True, "positive")


def crop():
    im = Image.new("RGB", (4, 2), "black")
    im.putpixel((3, 1), (255, 0, 0))
    data = io.BytesIO()
    im.crop((0, 0, 2, 2)).save(data, "PNG")
    data.seek(0)
    with Image.open(data) as saved:
        clipped = list(saved.size)
        outside = (255, 0, 0) in saved.getdata()
    preserved = list(im.size)
    observed = {"saved_extent": clipped, "sentinel_in_saved": outside, "source_extent": preserved}
    return row("T-03", "CP03", "P01", PILLOW + "Tests/test_image_crop.py#L10-L31",
               "Standing RGB raster 4x2 with sentinel at (3,1), crop a 2x2 corner and serialize only it.",
               {"saved_extent": [2, 2], "sentinel_in_saved": False, "source_extent": [4, 2]},
               observed, True, False, "scope_counterexample")


def rejects(directory):
    file = directory / "fixture.csv"
    file.write_text("name,age\nok,7\nbad,notnum\n", encoding="utf-8")
    with duckdb.connect() as con:
        valid = con.execute(
            "SELECT * FROM read_csv(?, columns={'name':'VARCHAR','age':'INTEGER'},"
            "auto_detect=false, header=true, store_rejects=true)", [str(file)],
        ).fetchall()
        errors = con.execute("SELECT error_type::VARCHAR, csv_line FROM reject_errors").fetchall()
        temporary = con.execute(
            "SELECT temporary FROM duckdb_tables() WHERE table_name='reject_errors'"
        ).fetchone()[0]
        observed = {"rows": valid, "rejects": errors, "temporary": temporary}
    return row("T-04", "CD01", "D03", DUCK + "test/sql/copy/csv/rejects/csv_rejects_read.test#L9-L21",
               "Three lines: name,age / ok,7 / bad,notnum. The explicit age type is INTEGER.",
               {"rows": [("ok", 7)], "rejects": [("CAST", "bad,notnum")], "temporary": True},
               observed, True, True, "positive")


def exclude():
    with duckdb.connect() as con:
        con.execute("CREATE TABLE integers(i INTEGER, j INTEGER, k INTEGER)")
        con.execute("INSERT INTO integers VALUES (1,2,3)")
        projected = con.execute("SELECT * EXCLUDE i FROM integers")
        columns = [column[0] for column in projected.description]
        result = projected.fetchall()
        base = con.execute("SELECT * FROM integers")
        original = [column[0] for column in base.description]
        observed = {"columns": columns, "rows": result, "base_columns": original,
                    "base_rows": base.fetchall()}
    return row("T-05", "CD02", "D05", DUCK + "test/sql/projection/select_star_exclude.test#L8-L27",
               "Use upstream table integers(i,j,k), row (1,2,3) and exclude i; then read the base table.",
               {"columns": ["j", "k"], "rows": [(2, 3)], "base_columns": ["i", "j", "k"],
                "base_rows": [(1, 2, 3)]}, observed, True, True, "positive")


def deletion(directory):
    file = str(directory / "persistent.duckdb")
    with duckdb.connect(file) as con:
        con.execute("CREATE TABLE t (id INTEGER)")
        con.execute("INSERT INTO t VALUES (1),(2)")
        filtered = con.execute("SELECT * FROM t WHERE id <> 2 ORDER BY id").fetchall()
    with duckdb.connect(file) as con:
        after_filter = con.execute("SELECT * FROM t ORDER BY id").fetchall()
        con.execute("DELETE FROM t WHERE id = 2")
    with duckdb.connect(file) as con:
        after_delete = con.execute("SELECT * FROM t ORDER BY id").fetchall()
    observed = {"view": filtered, "after_reopen": after_filter, "after_delete_reopen": after_delete}
    return row("T-06", "CD03", "D07", DUCK + "test/sql/delete/test_delete.test#L8-L34",
               "Persist rows 1,2. Use WHERE to display row 1, reopen, then run DELETE comparator and reopen.",
               {"view": [(1,)], "after_reopen": [(1,), (2,)], "after_delete_reopen": [(1,)]},
               observed, True, False, "scope_counterexample")


def pdf_probe():
    data = io.BytesIO()
    Image.new("RGBA", (2, 2), (255, 0, 0, 111)).save(data, "PDF")
    pdf = data.getvalue()
    observed = {"pdf": pdf.startswith(b"%PDF-"), "jpx": b"/JPXDecode" in pdf,
                "alpha_in_stream": b"/SMaskInData 1" in pdf}
    return row("T-07", "NP02", "P01", PILLOW + "src/PIL/PdfImagePlugin.py#L118-L154",
               "Synthetic 2x2 RGBA generated raster, local Linux wheel JPEG 2000 encoder; no original JP2.",
               {"pdf": True, "jpx": True, "alpha_in_stream": True}, observed, True, True,
               "context_only")


def table_probe(directory):
    csv = directory / "my_file_a=1,b=2,c=3.csv"
    csv.write_text("id\n9\n", encoding="utf-8")
    parquet = csv.with_suffix(".parquet")
    expression = "list_string_agg([lower(s) for s in ['a=1','b=2','c=3']])"
    with duckdb.connect() as con:
        con.execute("CREATE TABLE probe(id INTEGER)")
        con.execute("INSERT INTO probe VALUES (9)")
        con.execute("COPY probe TO ? (FORMAT PARQUET)", [str(parquet)])
        val = con.execute("SELECT " + expression).fetchone()[0]
        paths = [str(directory / "my_file_"), ".csv"]
        csv_rows = con.execute("SELECT id FROM read_csv(? || " + expression + " || ?)", paths).fetchall()
        paths[1] = ".parquet"
        pq_rows = con.execute("SELECT id FROM read_parquet(? || " + expression + " || ?)", paths).fetchall()
    observed = {"standalone": val, "local_csv": csv_rows, "local_parquet": pq_rows}
    return row("T-08", "ND02", "D06", DUCK + "test/sql/function/list/lambdas/table_functions.test#L66-L76",
               "Use computed filename in two local table functions, based on the published non-httpfs test.",
               {"standalone": "a=1,b=2,c=3", "local_csv": [(9,)], "local_parquet": [(9,)]},
               observed, True, True, "context_only")


def main():
    with TemporaryDirectory(prefix="af076-controls-") as tmp:
        directory = Path(tmp)
        results = [thumbnail(), color(), crop(), rejects(directory), exclude(), deletion(directory),
                   pdf_probe(), table_probe(directory)]
    print(json.dumps({"environment": {"python": platform.python_version(),
                                      "platform": sys.platform, "arch": platform.machine(),
                                      "pillow": pillow_version, "duckdb": duckdb.__version__,
                                      "jpeg2000": features.check_codec("jpg_2000")},
                      "results": results}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
