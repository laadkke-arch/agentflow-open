"""Reference-edition controls for the four prespecified calibration seats."""

import argparse
import json
import platform
import warnings
from importlib.metadata import version


def exception_info(exc):
    return {} if exc is None else {"type": type(exc).__name__, "message": str(exc)}


def click_result(runner, cmd, args):
    result = runner.invoke(cmd, args, prog_name="probe")
    try:
        stderr = result.stderr
    except ValueError:
        stderr = None
    return {"args": args, "exit_code": result.exit_code, "output": result.output,
            "stderr": stderr, "error": exception_info(result.exception)}


def cc01(mode):
    import click
    from click.testing import CliRunner

    if mode == "boundary":
        try:
            click.version_option(version="alpha", param_decls="-V")(lambda: None)
        except TypeError as exc:
            return {"attempted_call": "version and param_decls by keyword", "invoked": False,
                    "error": exception_info(exc)}
        return {"attempted_call": "version and param_decls by keyword", "invoked": False, "error": {}}

    @click.command()
    @click.version_option("alpha", "-V")
    def app():
        click.echo("normal command")

    runner = CliRunner()
    return {"selected_flag": click_result(runner, app, ["-V"]),
            "ordinary": click_result(runner, app, []),
            "default_flag": click_result(runner, app, ["--version"])}


def cc02(mode):
    import click
    from click.testing import CliRunner

    @click.command()
    def child():
        click.echo("child")

    with warnings.catch_warnings(record=True) as captured:
        warnings.simplefilter("always", DeprecationWarning)

        class CustomCli(click.MultiCommand):
            def list_commands(self, ctx):
                return ["child"]

            def get_command(self, ctx, name):
                return child if name == "child" else None

            def show_version(self, ctx, param, value):
                if value and not ctx.resilient_parsing:
                    click.echo("cli 0.1")
                    ctx.exit()

        app = CustomCli(name="probe")
        if mode == "positive":
            app.params = [click.Option(["--version", "-v"], is_flag=True, is_eager=True,
                                       expose_value=False, callback=app.show_version)]
        else:
            app.params = [click.version_option("0.1")]
        runner = CliRunner()
        outcome = {"version_flag": click_result(runner, app, ["--version"])}
        if mode == "positive":
            outcome["child"] = click_result(runner, app, ["child"])
        outcome["deprecations"] = [str(item.message) for item in captured]
    return outcome


def registry_example(*, slots, attrs_hook):
    import attr

    registry = {}
    registrations = []

    def display_key(key):
        return "NOTHING" if key is attr.NOTHING else key

    def register(cls):
        key = attr.fields(cls).name.default
        registrations.append([cls.__name__, display_key(key)])
        registry[key] = cls

    if attrs_hook:
        @attr.define(slots=slots)
        class Base:
            name: str

            @classmethod
            def __attrs_init_subclass__(cls):
                register(cls)
    else:
        @attr.define(slots=slots)
        class Base:
            name: str

            def __init_subclass__(cls, **kwargs):
                super().__init_subclass__(**kwargs)
                register(cls)

    @attr.define(slots=slots)
    class Int(Base):
        name: str = "int"

    @attr.define(slots=slots)
    class IntRange(Int):
        name: str = "int-range"

    def lookup(key):
        matched = registry.get(key)
        if matched is None:
            return {"exception": "KeyError"}
        obj = matched()
        return {"class": type(obj).__name__, "name": obj.name,
                "is_final_class": matched in (Int, IntRange)}

    return {
        "registrations": registrations, "call_count": len(registrations),
        "int_lookup": lookup("int"), "range_lookup": lookup("int-range"),
        "original_class_defaults": [display_key(attr.fields(cls).name.default)
                                    for cls in (Base, Int, IntRange)],
    }


def ac01(mode):
    if mode == "positive":
        return {"reported_unslotted": registry_example(slots=False, attrs_hook=False),
                "documented_attrs_hook": registry_example(slots=True, attrs_hook=True)}
    return {"original_slotted": registry_example(slots=True, attrs_hook=False)}


def ac02(mode):
    import attr
    import attrs

    @attrs.define
    class AT_Base:
        marker: str

    if mode == "positive":
        @attrs.define
        class Owner:
            AT_Base: AT_Base
    else:
        @attr.s
        class Owner:
            AT_Base: AT_Base = attr.ib()

    origin = AT_Base("keep")
    before = origin.marker
    owner = Owner(origin)
    described = attrs.fields(Owner).AT_Base
    return {
        "field_name": described.name, "reports_original_type": described.type is AT_Base,
        "reported_type_kind": type(described.type).__name__,
        "owner_value_is_original": owner.AT_Base is origin,
        "original_before": before, "original_after": origin.marker, "exception": None,
    }


def main():
    probes = {"CC01": ("click", cc01), "CC02": ("click", cc02),
              "AC01": ("attrs", ac01), "AC02": ("attrs", ac02)}
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("seat", choices=probes)
    parser.add_argument("mode", choices=("positive", "boundary"))
    args = parser.parse_args()
    package, run = probes[args.seat]
    print(json.dumps({"seat": args.seat, "mode": args.mode, "package": package,
                      "version": version(package), "python": platform.python_version(),
                      "result": run(args.mode)}, sort_keys=True))


if __name__ == "__main__":
    main()
