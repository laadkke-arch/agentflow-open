"""Alternative calculation using SQLite and indexed plain lines from the frozen fixtures."""

import sqlite3
from contextlib import closing


def records(root, path, fields):
    source = (root / path).read_text(encoding="utf-8").splitlines()
    header = source[0].split(",")
    indices = [header.index(field) for field in fields]
    result = []
    for line_number, raw in enumerate(source[1:], 2):
        if '"' in raw:
            raise ValueError(f"The independent plain-line check cannot interpret quotes in {path}:{line_number}")
        values = raw.split(",")
        result.append((line_number, *(values[index] for index in indices)))
    return result


def stats(db, root, spec):
    fields = ["date_of_interest", "BX_CASE_COUNT", "BK_CASE_COUNT"]
    db.execute("CREATE TABLE cases (line INT, date_key TEXT, bx TEXT, bk TEXT)")
    db.executemany("INSERT INTO cases VALUES (?, ?, ?, ?)", records(root, "statistics.csv", fields))
    date_key = spec["date"][5:7] + "/" + spec["date"][8:10] + "/" + spec["date"][:4]
    row = db.execute("SELECT line, bx, bk FROM cases WHERE date_key = ?", (date_key,)).fetchall()
    if len(row) > 1:
        raise ValueError("A duplicate date would make the frozen statistics selection ambiguous")
    raw, valid = db.execute(
        """
        WITH values_for_date(v) AS (
          SELECT bx FROM cases WHERE date_key = ?
          UNION ALL
          SELECT bk FROM cases WHERE date_key = ?
        ), accepted(n) AS (
          SELECT CAST(v AS INT) FROM values_for_date WHERE v NOT IN ('', 'NA', ':')
        )
        SELECT SUM(n), COUNT(*) FROM accepted
        """, (date_key, date_key)).fetchone()
    # For these nonnegative case counts, integer quotients implement half-up rounding.
    report = None if raw is None else 100 * (raw // 100 + int(raw % 100 >= 50))
    return {"raw": raw, "report": report, "valid": valid,
            "location": "statistics.csv", "line": row[0][0] if row else None,
            "field_values": dict(zip(fields[1:], row[0][1:])) if row else {}}


SERVICE_SQL = """
WITH params(day, period) AS (VALUES (?,?)),
regular AS (
  SELECT service FROM calendar, params
  WHERE period BETWEEN begin AND end
    AND CASE strftime('%w', day) WHEN '0' THEN sun WHEN '1' THEN mon
        WHEN '2' THEN tue WHEN '3' THEN wed WHEN '4' THEN thu
        WHEN '5' THEN fri WHEN '6' THEN sat END = '1'
),
kept AS (
  SELECT service FROM regular
  EXCEPT SELECT service FROM exceptions, params WHERE date_key=period AND kind='2'
)
SELECT service FROM kept
UNION SELECT service FROM exceptions, params WHERE date_key=period AND kind='1'
ORDER BY service
"""


def transit(db, root, spec):
    db.execute("CREATE TABLE routes (line INT, route TEXT)")
    db.executemany("INSERT INTO routes VALUES (?,?)", records(root, "routes.txt", ["route_id"]))
    db.execute("CREATE TABLE calendar (line INT, service TEXT, begin TEXT, end TEXT, "
               "mon TEXT, tue TEXT, wed TEXT, thu TEXT, fri TEXT, sat TEXT, sun TEXT)")
    fields = ["service_id", "start_date", "end_date", "monday", "tuesday", "wednesday",
              "thursday", "friday", "saturday", "sunday"]
    if "calendar.txt" in spec["paths"]:
        db.executemany("INSERT INTO calendar VALUES (?,?,?,?,?,?,?,?,?,?,?)", records(root, "calendar.txt", fields))
    db.execute("CREATE TABLE exceptions (line INT, service TEXT, date_key TEXT, kind TEXT)")
    if "calendar_dates.txt" in spec["paths"]:
        db.executemany("INSERT INTO exceptions VALUES (?,?,?,?)",
                       records(root, "calendar_dates.txt", ["service_id", "date", "exception_type"]))
    db.execute("CREATE TABLE trips (line INT, route TEXT, service TEXT, trip TEXT, direction TEXT)")
    db.executemany("INSERT INTO trips VALUES (?,?,?,?,?)",
                   records(root, "trips.txt", ["route_id", "service_id", "trip_id", "direction_id"]))
    day = spec["date"]
    active = [item[0] for item in db.execute(SERVICE_SQL, (day, day.replace("-", "")))]
    db.execute("CREATE TABLE active (service TEXT PRIMARY KEY)")
    db.executemany("INSERT INTO active VALUES (?)", [(service,) for service in active])
    selected = db.execute(
        "SELECT trips.line, trip FROM trips JOIN active USING (service) JOIN routes USING (route) "
        "WHERE route=? AND direction=? ORDER BY trips.line",
        (spec["route"], spec["direction"])).fetchall()
    ids = sorted({row[1] for row in selected})
    return {"raw": len(ids), "report": len(ids), "trips": ids, "active": active,
            "location": "trips.txt", "lines": [row[0] for row in selected]}


def calculate(root, spec):
    with closing(sqlite3.connect(":memory:")) as db:
        return (stats if spec["domain"] == "S" else transit)(db, root, spec)
