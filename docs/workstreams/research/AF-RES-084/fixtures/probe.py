"""Run one prespecified AF-RES-084 input against the installed package."""

import argparse
from importlib.metadata import version
import inspect
import json
from pathlib import Path
import platform
import shlex
import subprocess
import sys
from typing import Optional


NAMES_LINE = "probe names = "


def cn01_command(mode):
    import click

    if mode == "positive":
        @click.command()
        def app():
            click.echo(NAMES_LINE + json.dumps(shlex.split(click.prompt("Names"))))
    else:
        @click.command()
        @click.option("--names", multiple=True, prompt="Names")
        def app(names):
            click.echo(NAMES_LINE + json.dumps(names))

    app(args=[], prog_name="probe")


def cn01(mode):
    cmd = [sys.executable, "-I", str(Path(__file__).resolve()), "CN01", mode, "--native-prompt"]
    run = subprocess.run(cmd, input="foo bar\n", stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT, text=True, timeout=10)
    transcript = run.stdout
    lines = [line.split(NAMES_LINE, 1)[1] for line in transcript.splitlines() if NAMES_LINE in line]
    names = json.loads(lines[0]) if lines else []
    return {"cli_exit": run.returncode, "names": names, "transcript": transcript,
            "prompt_seen": "Names:" in transcript,
            "iterable_error": "Value must be an iterable." in transcript}


def an01(mode):
    import attrs

    @attrs.define
    class Example:
        a: int
        b: int
        sum: Optional[int] = attrs.field(default=None, init=mode == "boundary")

    instance = Example(11, 23)
    return {"parameters": list(inspect.signature(Example).parameters),
            "sum": instance.sum, "field_present": hasattr(instance, "sum")}


def cc01(mode):
    import click
    from click.testing import CliRunner

    if mode == "boundary":
        try:
            click.version_option(version="alpha", param_decls="-V")(lambda: None)
        except TypeError as error:
            return {"registered": False, "error": type(error).__name__, "detail": str(error)}
        return {"registered": True, "error": None}

    @click.command()
    @click.version_option("alpha", "-V")
    def app():
        click.echo("normal command")

    runner = CliRunner()
    selected_flag = runner.invoke(app, ["-V"], prog_name="probe")
    default_flag = runner.invoke(app, ["--version"], prog_name="probe")
    return {"registered": any("-V" in option.opts for option in app.params),
            "cli_exit": selected_flag.exit_code, "stdout": selected_flag.output,
            "default_cli_exit": default_flag.exit_code}


def ac01(mode):
    import attr
    import attrs

    registrations = []

    def register(cls, registry):
        key = attr.fields(cls).name.default
        registrations.append([cls.__name__, "NOTHING" if key is attr.NOTHING else key])
        registry[key] = cls

    if mode == "positive":
        @attr.define(slots=False, auto_attribs=False)
        class Base:
            name: str = attr.field()
            registry: dict[str, type] = {}

            def __init_subclass__(cls, **kwargs):
                super().__init_subclass__(**kwargs)
                register(cls, cls.registry)

        registry = Base.registry
    else:
        registry = {}

        @attr.define
        class Base:
            name: str

            def __init_subclass__(cls, **kwargs):
                super().__init_subclass__(**kwargs)
                register(cls, registry)

    @attr.define(slots=mode == "boundary")
    class Int(Base):
        name: str = "int"

    @attr.define(slots=mode == "boundary")
    class IntRange(Int):
        name: str = "int-range"

    def lookup(key, expected_class):
        try:
            found = registry[key]
        except KeyError:
            return {"error": "KeyError"}
        instance = found()
        return {"class": type(instance).__name__, "name": instance.name,
                "matches_requested_final_class": type(instance) is expected_class}

    return {"registrations": registrations, "call_count": len(registrations),
            "define_alias_identity": attr.define is attrs.define,
            "int_lookup": lookup("int", Int), "range_lookup": lookup("int-range", IntRange)}


PROBES = {"CN01": ("click", cn01), "AN01": ("attrs", an01),
          "CC01": ("click", cc01), "AC01": ("attrs", ac01)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case", choices=PROBES)
    parser.add_argument("mode", choices=("positive", "boundary"))
    parser.add_argument("--native-prompt", action="store_true")
    args = parser.parse_args()
    if args.native_prompt:
        if args.case != "CN01":
            parser.error("--native-prompt is only supported by CN01")
        cn01_command(args.mode)
        return
    package, probe = PROBES[args.case]
    print(json.dumps({
        "case": args.case, "mode": args.mode, "package": package,
        "version": version(package), "python": platform.python_version(),
        "implementation": platform.python_implementation(), "platform": platform.platform(),
        "observed": probe(args.mode),
    }, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
