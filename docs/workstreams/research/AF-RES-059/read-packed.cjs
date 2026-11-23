"use strict";

const crypto = require("node:crypto");
const fs = require("node:fs");
const path = require("node:path");
const { createRequire } = require("node:module");

const job = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
const root = fs.realpathSync(job.root);
const localRequire = createRequire(path.join(root, "probe.cjs"));

function readMember(file) {
    const real = fs.realpathSync(file);
    if (!real.startsWith(root + path.sep)) {
        throw new Error("Loaded a module outside the isolated extraction: " + real);
    }
    const data = fs.readFileSync(real);
    return {
        path: real,
        member: path.relative(root, real),
        bytes: data.length,
        sha256: crypto.createHash("sha256").update(data).digest("hex"),
    };
}

function hostRow(input) {
    const options = {
        timeZone: input.zone,
        year: "numeric", month: "2-digit", day: "2-digit",
        hour: "2-digit", minute: "2-digit", second: "2-digit", hourCycle: "h23",
    };
    const instant = new Date(input.unix_seconds * 1000);
    const long = new Intl.DateTimeFormat("en-GB", {
        ...options, timeZoneName: "longOffset",
    }).formatToParts(instant);
    const parts = Object.fromEntries(long.map(part => [part.type, part.value]));
    const token = /^GMT([+-])(\d{2}):(\d{2})(?::(\d{2}))?$/.exec(parts.timeZoneName);
    const offset = token
        ? (token[1] === "+" ? 1 : -1) * (+token[2] * 3600 + +token[3] * 60 + +(token[4] || 0))
        : 0;
    const short = new Intl.DateTimeFormat("en-US", {
        ...options, timeZoneName: "short",
    }).formatToParts(instant).find(part => part.type === "timeZoneName").value;
    return {
        ...input,
        value: {
            offset_s: offset,
            wall: `${parts.year}-${parts.month}-${parts.day}T${parts.hour}:${parts.minute}:${parts.second}`,
            abbr: short,
        },
        abbreviation_kind: "Intl localized short display token",
    };
}

const runtime = {
    executable: process.execPath,
    node: process.versions.node,
    icu: process.versions.icu,
    runtime_tz: process.versions.tz,
    platform: process.platform,
};
if (job.mode === "intl") {
    console.log(JSON.stringify({ runtime, records: job.inputs.map(hostRow) }));
    process.exit(0);
}

const packageJson = localRequire.resolve("moment-timezone/package.json");
const packageRoot = path.dirname(packageJson);
const packageEntry = localRequire.resolve("moment-timezone");
const momentMain = localRequire.resolve("moment");
const modeFile = job.bundle ? path.join(packageRoot, job.bundle) : packageEntry;
const moment = localRequire(modeFile);
const packedFile = path.join(packageRoot, "data", "packed", "latest.json");
const packed = require.cache[packedFile]?.exports;
const codeFiles = Object.keys(require.cache).filter(
    file => file.startsWith(packageRoot + path.sep) && file.endsWith(".js")
);
const selectedFile = packed ? packedFile : modeFile;

const records = job.inputs.map(input => {
    const zone = moment.tz.zone(input.zone);
    if (!zone) {
        return { ...input, missing: "zone absent in loaded dataset" };
    }
    const clock = job.mode === "wall-as-utc"
        ? moment.tz(input.utc.slice(0, -1), "YYYY-MM-DDTHH:mm:ss", true, input.zone)
        : moment.utc(input.unix_seconds * 1000).tz(input.zone);
    if (!clock.isValid()) {
        throw new Error("Invalid input: " + input.utc);
    }
    const ms = clock.valueOf();
    const westMinutes = zone.utcOffset(ms);
    const eastSeconds = Math.round(-westMinutes * 60);
    if (eastSeconds !== Math.round(clock.utcOffset() * 60) || zone.abbr(ms) !== clock.zoneAbbr()) {
        throw new Error("Zone/clock offset or abbreviation disagreement");
    }
    return {
        ...input,
        evaluated_unix_seconds: ms / 1000,
        evaluated_utc: new Date(ms).toISOString(),
        west_minutes: westMinutes,
        value: {
            offset_s: eastSeconds,
            wall: clock.format("YYYY-MM-DDTHH:mm:ss"),
            abbr: clock.zoneAbbr(),
        },
    };
});
console.log(JSON.stringify({
    runtime,
    moment: { version: moment.version, ...readMember(momentMain) },
    moment_timezone: {
        package_version: localRequire(packageJson).version,
        package_json: readMember(packageJson),
        version: moment.tz.version,
        data_version: moment.tz.dataVersion,
        entry: readMember(modeFile),
        bundle: job.bundle || null,
        packed_loaded: Boolean(packed),
        packed_zones: packed?.zones.length ?? null,
        code: codeFiles.map(readMember),
    },
    loaded: readMember(selectedFile),
    records,
}));
