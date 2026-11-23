#!/usr/bin/env python3
"""Build deterministic, answer-free catalogs from pinned upstream Git trees."""

from __future__ import annotations

import argparse
import ast
import doctest
import hashlib
import json
from pathlib import Path
import re
import subprocess
import textwrap


REMOTES = {
    "click": "pallets/click",
    "attrs": "python-attrs/attrs",
}
NAMESPACES = {"click", "attr", "attrs"}
NARROW = (
    r"README\.(?:rst|md)",
    r"docs/index\.(?:rst|md)",
)
BROAD = {
    "click": (
        r"docs/api\.(?:rst|md)",
        r"docs/options\.(?:rst|md)",
        r"docs/option-decorators\.(?:rst|md)",
        r"docs/arguments\.(?:rst|md)",
        r"docs/parameters\.(?:rst|md)",
        r"docs/parameter-types\.(?:rst|md)",
        r"docs/commands(?:-and-groups)?\.(?:rst|md)",
        r"docs/advanced\.(?:rst|md)",
        r"docs/complex\.(?:rst|md)",
        r"docs/testing\.(?:rst|md)",
        r"docs/click-concepts\.(?:rst|md)",
        r"docs/extending-click\.(?:rst|md)",
        r"docs/quickstart\.(?:rst|md)",
        r"(?:src/)?click/.*\.py",
        r"tests/.*\.py",
    ),
    "attrs": (
        r"docs/api[^/]*\.(?:rst|md)",
        r"docs/examples\.(?:rst|md)",
        r"docs/init\.(?:rst|md)",
        r"docs/types\.(?:rst|md)",
        r"docs/extending\.(?:rst|md)",
        r"docs/glossary\.(?:rst|md)",
        r"docs/names\.(?:rst|md)",
        r"docs/overview\.(?:rst|md)",
        r"docs/how-does-it-work\.(?:rst|md)",
        r"(?:src/)?attr/.*\.py",
        r"(?:src/)?attrs/.*\.py",
        r"tests/.*\.py",
    ),
}
# A menu link enumerates its literal parent topic only.
MENU = {
    "click": {
        "parameters": "click.Parameter", "options": "click.option",
        "option-decorators": "click.guide.option-decorators",
        "arguments": "click.argument", "commands": "click.command",
        "commands-and-groups": "click.guide.commands-and-groups",
        "prompts": "click.guide.prompts", "handling-files": "click.guide.handling-files",
        "shell-completion": "click.guide.shell-completion",
        "exceptions": "click.guide.exceptions",
    },
    "attrs": {
        "types": "attrs.guide.types", "init": "attrs.guide.initialization",
        "comparison": "attrs.guide.comparison", "hashing": "attrs.guide.hashing",
        "extending": "attrs.guide.extending",
    },
}
BULLETS = {
    "click": {
        "arbitrary nesting of commands": "click.command.nesting",
        "automatic help page generation": "click.help.auto-generation",
        "supports lazy loading of subcommands at runtime": "click.command.lazy-loading",
    },
    "attrs": {
        "a concise and explicit overview of the class's attributes": "attrs.guide.field-declarations",
        "a nice human-readable `__repr__`": "attrs.guide.repr",
        "equality-checking methods": "attrs.guide.comparison",
        "an initializer": "attrs.guide.initialization",
    },
}
ATTRS_BARE_README = {
    "attrib": "attr.attrib", "define": "attrs.define", "frozen": "attrs.frozen",
    "field": "attrs.field",
}
ATTRS_ANCHORS = {
    "hooking-yourself-into-initialization": "attrs.guide.initialization-hooks",
    "customization": "attrs.guide.comparison-customization",
}
ATTRS_HOOKS = {
    "__attrs_pre_init__": "attrs.hook.__attrs_pre_init__",
    "__attrs_post_init__": "attrs.hook.__attrs_post_init__",
    "__attrs_init_subclass__": "attrs.hook.__attrs_init_subclass__",
    "__attrs_init__": "attrs.generated.__attrs_init__",
}
ROLE = re.compile(r"(?::(?:py:)?(?:class|func|meth|mod|attr|data|obj):|\{(?:py:)?(?:class|func|meth|mod|attr|data|obj)\})`([^`]+)`")
INLINE = re.compile(r"(?<!`)`{1,2}(~?(?:click|attr|attrs)\.[\w.]+(?:\(\))?)`{1,2}(?!`)")
DIRECTIVE = re.compile(r"^\s*(?:\.\.\s+|\x60{3,}\{)(?:py:)?(?P<kind>currentmodule|module|autoclass|autofunction|autodata|automethod|class|function|data|method|attribute|autoattribute)(?:::|\})\s+(?P<value>\S+)")
RST_PY = re.compile(r"^(\s*)\.\.\s+(?:(?:code-block|code)::\s*(?:python|py|pycon)\b|doctest::|testcode::|click:example::)")
MD_FENCE = re.compile(r"^\s*(`{3,}|~{3,}|:{3,})\s*(\S*)")
PUBLIC_COMPAT = re.compile(r"^[A-Za-z][\w-]*(?:\.[A-Za-z][\w-]*)*$")


def git(repo, *args):
    return subprocess.check_output(["git", "-C", str(repo), *args])


def read_tree(repo, sha):
    paths = {}
    for raw in git(repo, "ls-tree", "-r", "-z", sha).split(b"\0"):
        if not raw:
            continue
        meta, name = raw.split(b"\t", 1)
        _, kind, oid = meta.decode("ascii").split()
        if kind == "blob":
            paths[name.decode()] = oid
    return paths


def module_name(path):
    if path.startswith("src/"):
        path = path[4:]
    if not path.endswith(".py") or path.split("/")[0] not in NAMESPACES:
        return None
    return path.removesuffix(".py").removesuffix("/__init__").replace("/", ".")


def by_path(path, start, end=None, **kw):
    row = {"path": path, "line_start": start, "line_end": end or start}
    row.update(kw)
    return row


def ast_ref(node):
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        parent = ast_ref(node.value)
        if parent:
            return f"{parent}.{node.attr}"
    return None


def import_prefix(node, package):
    if node.level:
        parts = package.split(".")[: len(package.split(".")) - node.level + 1]
        if node.module:
            parts.append(node.module)
        return ".".join(parts)
    return node.module or ""


def assigned_names(node):
    if isinstance(node, ast.Assign):
        return [target.id for target in node.targets if isinstance(target, ast.Name)]
    if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
        return [node.target.id]
    return []


def public_name(value):
    return bool(PUBLIC_COMPAT.fullmatch(value)) and value.split(".")[0] in NAMESPACES


def doc_ref(raw, namespace):
    if "<" in raw and raw.rstrip().endswith(">"):
        raw = raw.rsplit("<", 1)[1].rstrip().removesuffix(">")
    symbol = raw.strip().lstrip("~.").split("(", 1)[0]
    if public_name(symbol):
        return symbol
    candidate = f"{namespace}.{symbol}"
    return candidate if namespace and public_name(candidate) else None


def official_markup(text, default_namespace):
    namespace = default_namespace
    for line_number, line in enumerate(text.splitlines(), 1):
        directive = DIRECTIVE.match(line)
        if directive:
            ref = directive["value"].split("(", 1)[0]
            if directive["kind"] in ("module", "currentmodule"):
                namespace = ref
            else:
                feature = doc_ref(ref, namespace)
                if feature:
                    yield feature, line_number, "api-directive"
        for raw in ROLE.findall(line):
            feature = doc_ref(raw, namespace)
            if feature:
                yield feature, line_number, "api-reference"
        for raw in INLINE.findall(line):
            feature = doc_ref(raw, namespace)
            if feature:
                yield feature, line_number, "inline-api"


def exports(tree, path, name):
    package = name if path.endswith("/__init__.py") else name.rpartition(".")[0]
    bindings, definitions = {}, {}
    explicit_all, star = None, []
    root_package = name in NAMESPACES
    for node in tree.body:
        if isinstance(node, ast.ImportFrom):
            prefix = import_prefix(node, package)
            for alias in node.names:
                if prefix.split(".")[0] not in NAMESPACES:
                    continue
                if alias.name == "*":
                    star.append((prefix, node.lineno))
                    continue
                key = alias.asname or alias.name
                bindings[key] = (f"{prefix}.{alias.name}", node.lineno, "export-import")
        elif isinstance(node, (ast.ClassDef, ast.AsyncFunctionDef, ast.FunctionDef)):
            definitions[node.name] = node
        for key in assigned_names(node):
            if key == "__all__" and isinstance(node.value, (ast.List, ast.Set, ast.Tuple)):
                items = node.value.elts
                if all(isinstance(x, ast.Constant) and isinstance(x.value, str) for x in items):
                    explicit_all = {x.value for x in items}
                continue
            value = ast_ref(node.value)
            if value and value in bindings:
                value = bindings[value][0]
            elif value and "." not in value:
                value = f"{name}.{value}"
            if value and value.split(".")[0] in NAMESPACES:
                bindings[key] = (value, node.lineno, "export-assignment")
            else:
                definitions[key] = node
    if explicit_all is not None:
        names = explicit_all
    elif root_package:
        names = set(definitions) | set(bindings)
    else:
        names = set()
    return definitions, bindings, star, sorted(k for k in names if not k.startswith("_"))


class Catalog:
    def __init__(self, package, sha, contents, trees, narrow):
        self.package = package
        self.sha = sha
        self.contents = contents
        self.trees = trees
        self.narrow = narrow
        self.locations = {}
        self.alias_edges = {}
        self.explicit_menu = set()
        self.incomplete = set()
        self.forward = {}
        self.forward_rejections = {}
        self.protocols = set()
        self.explicit_exclusions = []
        self.class_paths = {}
        self.params = {}
        self.doc_issues = []
        self.aliases = {}
        self.groups = {}

    def add(self, feature, path, line, kind, end=None, **kw):
        evidence = by_path(path, line, end, kind=kind, **kw)
        items = self.locations.setdefault(feature, [])
        if evidence not in items:
            items.append(evidence)

    def build_aliases(self):
        modules = {}
        for path, tree in self.trees.items():
            name = module_name(path)
            if name:
                modules[name] = (path, exports(tree, path, name))
        self.modules = modules
        # The modern attr/attrs star-reexports are resolved only when the
        # original module supplies an explicit static export set.
        for module, (path, (definitions, bindings, stars, names)) in modules.items():
            for source, line in stars:
                if source in modules:
                    source_names = modules[source][1][3]
                    if source_names:
                        for key in source_names:
                            bindings[key] = (f"{source}.{key}", line, "star-reexport")
                            if key not in names:
                                names.append(key)
                    else:
                        self.incomplete.add(f"export:{path}:{line}:star-target-without-static-set")
                else:
                    self.incomplete.add(f"export:{path}:{line}:star-target-missing")
            for key, (target, line, kind) in bindings.items():
                feature = f"{module}.{key}"
                if feature == target:
                    continue
                if key in names or target.rpartition(".")[0] in modules:
                    self.alias_edges[feature] = target
                if key in names:
                    self.add(feature, path, line, kind)
            for key in names:
                if key in definitions:
                    self.add(f"{module}.{key}", path, definitions[key].lineno, "public-declaration")
                elif key not in bindings:
                    self.incomplete.add(f"export:{path}:{key}:unresolved-public-binding")

        def origin(key):
            seen = set()
            while key in self.alias_edges and key not in seen:
                seen.add(key)
                key = self.alias_edges[key]
            return key

        documented = []
        for path, text in self.contents.items():
            if path.startswith("docs/") and re.search(r"/api[^/]*\.(?:rst|md)$", path):
                for symbol, line, kind in official_markup(text, self.package):
                    if kind == "api-directive":
                        self.add(symbol, path, line, kind)
                        documented.append(symbol)
        groups = {}
        for key in sorted(set(self.locations) | set(self.alias_edges) | set(documented)):
            if key in self.locations:
                groups.setdefault(origin(key), set()).add(key)
            # Include forwarding import sites only when a listed binding has
            # the same origin. The source's private spelling stays internal.
        for source_key, keys in groups.items():
            ordered = sorted(keys, key=lambda x: (x.count("."), x.startswith("attr."),
                                                   x not in ("attr.ib", "attr.s"), x))
            canonical = ordered[0]
            self.groups[canonical] = (source_key, ordered)
            for key in ordered:
                self.aliases[key] = canonical
        # Retain aliases in public submodules even if first observed via their
        # top-level export or an explicit API directive elsewhere.
        for key in self.alias_edges:
            source_key = origin(key)
            choices = groups.get(source_key, set())
            if choices and public_name(key) and "._" not in key:
                self.aliases[key] = self.aliases[sorted(choices)[0]]

    def narrow_list(self):
        for path in sorted(self.narrow):
            text = self.contents[path]
            in_rst_menu = False
            fence = None
            for idx, line in enumerate(text.splitlines(), 1):
                stripped = line.strip()
                boundary = MD_FENCE.match(line)
                if boundary:
                    if fence is None:
                        fence = boundary[2]
                    else:
                        fence = None
                    continue
                if fence is not None and fence != "{toctree}":
                    continue
                if path.endswith(".rst"):
                    if re.match(r"^\s*\.\.\s+toctree::", line):
                        in_rst_menu = True
                        continue
                    if stripped and not line[0].isspace():
                        in_rst_menu = False
                bullet = re.match(r"^\s*[-*+]\s+(.+)$", line)
                if bullet:
                    key = bullet[1].casefold().rstrip(" ,.")
                    feature = BULLETS[self.package].get(key)
                    if feature:
                        self.add(feature, path, idx, "menu-feature", label=bullet[1])
                        self.explicit_menu.add(feature)
                target = None
                if fence == "{toctree}" or (in_rst_menu and line[:1].isspace()):
                    if re.fullmatch(r"[a-z][a-z-]+", stripped):
                        target = stripped
                doc_link = re.search(r"(?:\{doc\}|:doc:)`([a-z][a-z-]+)`", line)
                if doc_link:
                    target = doc_link[1]
                if not target:
                    link = re.search(r"\]\((?:\./)?([a-z][a-z-]+)\.(?:rst|md|html)\)", line)
                    if link:
                        target = link[1]
                if target and target in MENU[self.package]:
                    feature = MENU[self.package][target]
                    dest = next((f"docs/{target}.{ext}" for ext in ("md", "rst")
                                 if f"docs/{target}.{ext}" in self.all_paths), None)
                    self.add(feature, path, idx, "menu-direct-link", target=dest,
                             destination_exists=bool(dest))
                    if dest:
                        self.explicit_menu.add(feature)
                    else:
                        self.incomplete.add(f"menu-target:{path}:{idx}:{target}")
                # Plain names from example bodies do not become
                # menu listings. Only explicitly marked inline API names.
                for raw in INLINE.findall(line):
                    feature = doc_ref(raw, self.package)
                    if feature:
                        self.add(feature, path, idx, "menu-inline-api")
                        self.explicit_menu.add(feature)
                if self.package == "attrs":
                    for name in re.findall(r"(?<!`)`(attrib|define|frozen|field)`(?!`)", line):
                        feature = ATTRS_BARE_README[name]
                        self.add(feature, path, idx, "menu-inline-api", label=name)
                        self.explicit_menu.add(feature)
                    for anchor, feature in ATTRS_ANCHORS.items():
                        if f"#{anchor})" in line:
                            self.add(feature, path, idx, "menu-direct-link", fragment=anchor,
                                     target="docs/init" if anchor != "customization" else "docs/comparison")
                            self.explicit_menu.add(feature)

    def declaration(self, feature, path, node):
        self.add(feature, path, node.lineno, "definition", end=node.lineno)
        if isinstance(node, ast.ClassDef):
            self.class_paths[feature] = (path, node)
            for method in node.body:
                if isinstance(method, (ast.AsyncFunctionDef, ast.FunctionDef)):
                    if method.name == "__init__":
                        self.signature(feature, path, method, method=True)
                    elif not method.name.startswith("_"):
                        key = f"{feature}.{method.name}"
                        self.add(key, path, method.lineno, "public-method")
                        self.signature(key, path, method, method=True)
            if any(isinstance(x, ast.FunctionDef) and x.name == "__init__" for x in node.body):
                self.add(feature, path, node.lineno, "class-constructor")
        elif isinstance(node, (ast.AsyncFunctionDef, ast.FunctionDef)):
            self.signature(feature, path, node)

    def signature(self, feature, path, node, method=False):
        # Positional-only settings remain choices, but cannot be used as keywords.
        params = (*node.args.posonlyargs, *node.args.args, *node.args.kwonlyargs)
        local = self.params.setdefault(feature, set())
        implicit_first = method and not any(ast_ref(d) == "staticmethod" for d in node.decorator_list)
        for index, arg in enumerate(params):
            if (implicit_first and index == 0) or arg.arg.startswith("_"):
                continue
            local.add(arg.arg)
            self.add(f"{feature}.{arg.arg}", path, arg.lineno, "parameter-declaration", api=feature)
        if node.args.vararg and not node.args.vararg.arg.startswith("_"):
            arg = node.args.vararg
            self.add(f"{feature}.{arg.arg}", path, arg.lineno, "variadic-positional-declaration", api=feature)
        raw = ast.get_docstring(node, clean=False) or ""
        for raw_ref, line, kind in official_markup(raw, self.package):
            if raw_ref in self.aliases:
                self.add(self.aliases[raw_ref], path, node.body[0].lineno + line - 1,
                         "signature-doc-reference")
        if self.package == "click" and node.args.kwarg:
            self.decorator_forwarding(feature, path, node, raw)

    def decorator_forwarding(self, feature, path, node, raw):
        """Resolve documented decorator settings through old/new constructor routes."""
        keyword_maps = {node.args.kwarg.arg}
        assignments = [sub for sub in ast.walk(node) if isinstance(sub, ast.Assign)]
        for sub in assignments:
            if (isinstance(sub.value, ast.Call) and
                    ast_ref(sub.value.func) == f"{node.args.kwarg.arg}.copy"):
                keyword_maps.update(ast_ref(target) for target in sub.targets if isinstance(target, ast.Name))
        for candidate in ("Option", "Argument"):
            documented_cls = re.search(r":param cls:[\s\S]*?:class:`" + candidate + r"`", raw)
            if not documented_cls:
                continue
            classes = set()
            pop_line = None
            for sub in assignments:
                if ast_ref(sub.value) == candidate:
                    if any(ast_ref(target) == "cls" for target in sub.targets):
                        classes.add("cls")
                elif (isinstance(sub.value, ast.Call)
                      and ast_ref(sub.value.func) in {f"{key}.pop" for key in keyword_maps}
                      and len(sub.value.args) == 2
                      and isinstance(sub.value.args[0], ast.Constant)
                      and sub.value.args[0].value == "cls"
                      and ast_ref(sub.value.args[1]) == candidate):
                    classes.update(ast_ref(target) for target in sub.targets if isinstance(target, ast.Name))
                    pop_line = sub.lineno
            for use in ast.walk(node):
                if (isinstance(use, ast.Call) and ast_ref(use.func) in classes and
                        any(kw.arg is None and ast_ref(kw.value) in keyword_maps for kw in use.keywords)):
                    self.forward[feature] = (f"click.{candidate}", path, use.lineno)
                    if pop_line:
                        self.params[feature].add("cls")
                        self.add(f"{feature}.cls", path, pop_line, "documented-keyword-pop", api=feature)
                    break

    def direct_exclusions(self):
        # Recognize upstream diagnostics that explicitly name both public
        # settings. These are evidence of a boundary, never eligible pairs.
        for path, text in self.contents.items():
            if self.package == "click" and path.endswith("/core.py"):
                for line_no, line in enumerate(text.splitlines(), 1):
                    match = re.search(r"'count' is not valid with '(multiple|is_flag)'", line)
                    if match:
                        for owner in ("click.Option", "click.option"):
                            settings = sorted(f"{owner}.{key}" for key in ("count", match[1]))
                            if all(key in self.locations for key in settings):
                                self.explicit_exclusions.append(by_path(
                                    path, line_no, features=settings,
                                    observation=f"The default Option constructor rejects count=True and {match[1]}=True.",
                                    outcome="conditional-refutation"))
            elif self.package == "attrs" and path.endswith("/_make.py"):
                for line_no, line in enumerate(text.splitlines(), 1):
                    if "default` and `factory` arguments are mutually exclusive" in line:
                        for owner in ("attr.ib", "attrs.field"):
                            settings = sorted(f"{owner}.{key}" for key in ("default", "factory"))
                            if all(key in self.locations for key in settings):
                                self.explicit_exclusions.append(by_path(
                                    path, line_no, features=settings,
                                    observation="Passing both an explicit default and a factory is rejected.",
                                    outcome="conditional-refutation"))

    def public_protocols(self):
        if self.package != "attrs":
            return
        for path in self.contents:
            if path not in ("docs/init.md", "docs/init.rst", "docs/examples.md", "docs/examples.rst"):
                continue
            for line_no, line in enumerate(self.contents[path].splitlines(), 1):
                for spelling, feature in ATTRS_HOOKS.items():
                    if f"`{spelling}`" not in line:
                        continue
                    self.protocols.add(spelling)
                    self.add(feature, path, line_no, "documented-class-protocol", spelling=spelling,
                             api_role="generated-method" if spelling == "__attrs_init__" else "user-hook")
                    if (spelling == "__attrs_post_init__" and "cache_hash=True" in line
                            and re.search(r"must not|can not|cannot", line, re.I)):
                        self.explicit_exclusions.append(by_path(
                            path, line_no, features=sorted((feature, "attrs.define.cache_hash")),
                            observation="Reading the instance hash from this hook with cache_hash=True is explicitly disallowed.",
                            outcome="conditional-refutation"))
        for path, text in self.contents.items():
            if not (path.endswith("/_make.py") or path.endswith("/_next_gen.py")):
                continue
            for line_no, line in enumerate(text.splitlines(), 1):
                for spelling in sorted(self.protocols):
                    if spelling in line:
                        self.add(ATTRS_HOOKS[spelling], path, line_no, "documented-protocol-implementation",
                                 spelling=spelling)

    def declaration_map(self):
        for feature, (source, _) in self.groups.items():
            module, _, key = source.rpartition(".")
            if module in self.modules and key in self.modules[module][1][0]:
                path, (definitions, _, _, _) = self.modules[module]
                self.declaration(feature, path, definitions[key])

        # Observe pass-through only when a source class has one known base
        # and an explicit super().__init__(**same_kwarg) call.
        for feature, (path, node) in self.class_paths.items():
            if len(node.bases) != 1:
                continue
            base = ast_ref(node.bases[0])
            if not base:
                continue
            if "." not in base:
                base = f"{self.package}.{base}"
            base = self.aliases.get(base, base)
            for method in node.body:
                if not isinstance(method, ast.FunctionDef) or method.name != "__init__" or not method.args.kwarg:
                    continue
                for call in ast.walk(method):
                    if (isinstance(call, ast.Call) and isinstance(call.func, ast.Attribute)
                            and call.func.attr == "__init__" and isinstance(call.func.value, ast.Call)
                            and ast_ref(call.func.value.func) == "super"
                            and any(w.arg is None and ast_ref(w.value) == method.args.kwarg.arg
                                    for w in call.keywords)):
                        self.forward[feature] = (base, path, call.lineno)
                        rejects = self.forward_rejections.setdefault(feature, set())
                        for guard in ast.walk(method):
                            if not (isinstance(guard, ast.If) and isinstance(guard.test, ast.Compare)
                                    and len(guard.test.ops) == 1 and isinstance(guard.test.ops[0], ast.In)
                                    and len(guard.test.comparators) == 1
                                    and ast_ref(guard.test.comparators[0]) == method.args.kwarg.arg
                                    and isinstance(guard.test.left, ast.Constant)
                                    and isinstance(guard.test.left.value, str)
                                    and any(isinstance(sub, ast.Raise) for sub in guard.body)):
                                continue
                            rejects.add(guard.test.left.value)
        for api, (target, path, line) in self.forward.items():
            seen = {api}
            exclusions = set(self.forward_rejections.get(api, ()))
            self.params.setdefault(api, set()).update(self.params.get(target, set()) - exclusions)
            while target in self.forward and target not in seen:
                seen.add(target)
                exclusions.update(self.forward_rejections.get(target, ()))
                target = self.forward[target][0]
                self.params[api].update(self.params.get(target, set()) - exclusions)
            for arg in sorted(self.params[api]):
                if f"{api}.{arg}" not in self.locations:
                    self.add(f"{api}.{arg}", path, line, "parameter-forwarding", api=api, target=target)

    def api_for(self, symbol, imported):
        if not symbol:
            return None
        root, dot, suffix = symbol.partition(".")
        ref = imported.get(root, root) + dot + suffix
        if ref in self.aliases:
            return self.aliases[ref]
        if ref in self.locations and public_name(ref):
            return ref
        parent, _, child = ref.rpartition(".")
        canonical = self.aliases.get(parent)
        full = f"{canonical}.{child}"
        return full if canonical and full in self.locations else None

    def remember_imports(self, tree, imported):
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                prefix = node.module or ""
                if prefix and prefix.split(".")[0] in NAMESPACES:
                    for alias in node.names:
                        if alias.name != "*":
                            imported[alias.asname or alias.name] = f"{prefix}.{alias.name}"
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.split(".")[0] not in NAMESPACES:
                        continue
                    if alias.asname:
                        imported[alias.asname] = alias.name
                    else:
                        imported[alias.name.split(".")[0]] = alias.name.split(".")[0]

    def usage(self, tree, path, first, kind, imported, case=None, negative=False, control_line=None):
        self.remember_imports(tree, imported)
        negative_nodes = set()
        for block in ast.walk(tree):
            if isinstance(block, (ast.With, ast.AsyncWith)) and any(
                    isinstance(item.context_expr, ast.Call) and
                    ast_ref(item.context_expr.func) == "pytest.raises" for item in block.items):
                negative_nodes.update(child for stmt in block.body for child in ast.walk(stmt))
        class_controls = test_constructor_controls(tree, negative_nodes) if case else {}
        # Registration and calls are distinct kinds of evidence.
        for node in ast.walk(tree):
            outcome = "expected-error" if negative or node in negative_nodes else "joint-use"
            if isinstance(node, ast.Call):
                feature = self.api_for(ast_ref(node.func), imported)
                if not feature:
                    continue
                line = first + node.lineno - 1
                end = first + getattr(node, "end_lineno", node.lineno) - 1
                self.add(feature, path, line, kind, end, test=case)
                API_kwargs = []
                nested_options = []
                for kw in node.keywords:
                    if kw.arg and not kw.arg.startswith("_"):
                        key = f"{feature}.{kw.arg}"
                        # Passing a name in a test is evidence of use; it does
                        # not by itself create a choice outside the public API.
                        if kw.arg not in self.params.get(feature, ()):
                            continue
                        self.add(key, path, first + kw.lineno - 1, kind, test=case, api=feature)
                        API_kwargs.append(key)
                        if isinstance(kw.value, ast.Call):
                            nested = self.api_for(ast_ref(kw.value.func), imported)
                            if nested and nested != feature:
                                nested_options.append((key, nested))
                if len(set(API_kwargs)) == 2:
                    self.combination(*API_kwargs, path, line, end, kind, case,
                                     "one-call:two-explicit-settings", outcome, control_line=control_line)
                for key, nested in nested_options:
                    self.combination(key, nested, path, line, end, kind, case,
                                     "one-call:nested-feature-value", outcome, control_line=control_line)
                if not API_kwargs:
                    for arg in node.args:
                        if isinstance(arg, ast.Call):
                            nested = self.api_for(ast_ref(arg.func), imported)
                            if nested and nested != feature:
                                self.combination(feature, nested, path, line, end, kind, case,
                                                 "one-call:nested-feature-value", outcome, control_line=control_line)
            elif isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                # Click decorators on the same callable bind to that callable.
                by_feature = {}
                for expr in node.decorator_list:
                    call = expr.func if isinstance(expr, ast.Call) else expr
                    feature = self.api_for(ast_ref(call), imported)
                    if feature:
                        by_feature[feature] = expr.lineno
                        self.add(feature, path, first + expr.lineno - 1, kind, test=case)
                if len(by_feature) == 2:
                    self.combination(*by_feature, path, first + min(by_feature.values()) - 1,
                                     first + max(by_feature.values()) - 1, kind, case,
                                     "stacked-decorators:same-definition", outcome, control_line=control_line)
                if isinstance(node, ast.ClassDef):
                    controls = class_controls.get(node, [(outcome, control_line)])
                    for protocol_outcome, trigger in controls:
                        self.protocol_example(node, path, first, kind, imported, case,
                                              protocol_outcome, trigger)

    def protocol_example(self, node, path, first, kind, imports, case, outcome, control_line):
        methods = [member for member in node.body if isinstance(member, (ast.FunctionDef, ast.AsyncFunctionDef))]
        known_hooks = [method for method in methods if method.name in self.protocols]
        if len(known_hooks) == 2:
            self.combination(*(ATTRS_HOOKS[member.name] for member in known_hooks),
                             path, first + known_hooks[0].lineno - 1,
                             first + known_hooks[1].end_lineno - 1, kind, case,
                             "documented-class-protocol:two-hooks-on-class", outcome,
                             control_line=control_line)
        for declaration in methods:
            names = {declaration.name}
            for call in ast.walk(declaration):
                if isinstance(call, ast.Call) and isinstance(call.func, ast.Attribute):
                    names.add(call.func.attr)
            for spelling in sorted(self.protocols & names):
                feature = ATTRS_HOOKS[spelling]
                self.add(feature, path, first + declaration.lineno - 1, kind, test=case)
                for expression in node.decorator_list:
                    func = expression.func if isinstance(expression, ast.Call) else expression
                    decorator = self.api_for(ast_ref(func), imports)
                    if decorator not in ("attrs.define", "attrs.frozen", "attr.s"):
                        continue
                    chosen = decorator
                    if isinstance(expression, ast.Call) and len(expression.keywords) == 1:
                        key = expression.keywords[0].arg
                        if key in self.params.get(decorator, ()):
                            chosen = f"{decorator}.{key}"
                    self.combination(chosen, feature, path, first + expression.lineno - 1,
                                     first + declaration.end_lineno - 1, kind, case,
                                     "documented-class-protocol:same-decorated-class", outcome,
                                     control_line=control_line)

    def combination(self, left, right, path, line, end, kind, case, basis, outcome, control_line=None):
        if left == right:
            return
        extra = {"test": case, "composition": basis, "outcome": outcome}
        if control_line is not None:
            extra["control_line"] = control_line
        self.add(" + ".join(sorted((left, right))), path, line, kind, end, **extra)

    def test_examples(self, path, tree):
        if not path.split("/")[-1].startswith("test_"):
            return
        imports = {}
        self.remember_imports(tree, imports)
        parents = {}
        for node in ast.walk(tree):
            for child in ast.iter_child_nodes(node):
                parents[child] = node
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) or not node.name.startswith("test_"):
                continue
            parent = parents.get(node)
            name = f"{parent.name}.{node.name}" if isinstance(parent, ast.ClassDef) else node.name
            self.usage(node, path, 1, "upstream-test-use", imports.copy(), case=name)

    def document_examples(self, path, text):
        # In a few official guides, a globally provided API is named in prose
        # and then used unqualified. Bind it only when exactly one documented
        # API with that basename occurs in this same source file.
        prose_refs = {}
        for name, _, kind in official_markup(text, self.package):
            if kind != "api-directive" and name in self.aliases:
                prose_refs.setdefault(name.rpartition(".")[2], set()).add(self.aliases[name])
        imports = {bare: next(iter(names)) for bare, names in prose_refs.items() if len(names) == 1}
        for line, block in code_blocks(text):
            if ">>>" in block:
                try:
                    examples = doctest.DocTestParser().get_examples(block)
                except ValueError as exc:
                    self.doc_issues.append(by_path(path, line, reason="doctest:" + str(exc)))
                    continue
                controls = doctest_controls(examples)
                for index, sample in enumerate(examples):
                    available = controls.get(index, [(bool(sample.exc_msg), None)])
                    for failed, instance_line in available:
                        trigger = line + instance_line if instance_line is not None else None
                        self.parse_example(path, line + sample.lineno, sample.source, imports,
                                           negative=failed, control_line=trigger)
            else:
                self.parse_example(path, line, textwrap.dedent(block), imports)

    def parse_example(self, path, line, code, imports, negative=False, control_line=None):
        try:
            tree = ast.parse(code)
        except SyntaxError as exc:
            # Official manuals often give only a decorator expression.
            # Parse that syntax with a dummy owner, without executing it.
            if not code.lstrip().startswith("@"):
                self.doc_issues.append(by_path(path, line, reason="example-python:" + exc.msg))
                return
            try:
                tree = ast.parse(code + "\ndef _example_host():\n    pass\n")
            except SyntaxError:
                self.doc_issues.append(by_path(path, line, reason="example-python:" + exc.msg))
                return
        self.usage(tree, path, line, "official-doc-example", imports,
                   negative=negative, control_line=control_line)

    def rows(self, narrow_only):
        if narrow_only:
            features = self.explicit_menu
        else:
            features = {key for key, locations in self.locations.items()
                        if " + " not in key or any(l.get("outcome") == "joint-use" for l in locations)}
        result = {}
        for feature in sorted(features):
            entries = self.locations[feature]
            if narrow_only:
                entries = [row for row in entries if row["kind"].startswith("menu-")]
            canonical = self.canonical(feature)
            obj = result.setdefault(canonical, {"id": canonical, "names": set(), "locations": []})
            obj["names"].add(feature)
            for entry in entries:
                if entry not in obj["locations"]:
                    obj["locations"].append(entry)
        if not narrow_only:
            for alias, canonical in sorted(self.aliases.items()):
                if canonical in result and public_name(alias) and "._" not in alias:
                    result[canonical]["names"].add(alias)
        for row in result.values():
            row["names"] = sorted(row["names"])
            row["kind"] = "combination" if " + " in row["id"] else "single"
            row["locations"].sort(key=lambda x: (x["path"], x["line_start"], x["kind"]))
        return [result[key] for key in sorted(result)]

    def canonical(self, feature):
        if " + " in feature:
            return " + ".join(sorted(self.canonical(part) for part in feature.split(" + ")))
        if feature in self.aliases:
            return self.aliases[feature]
        parent, _, child = feature.rpartition(".")
        return f"{self.aliases[parent]}.{child}" if parent in self.aliases else feature


def test_constructor_controls(test, negative_nodes):
    """Link simple in-body constructor invocations in an upstream test."""
    active_classes, controls = {}, {}

    def walk_statements(statements):
        for statement in statements:
            if isinstance(statement, ast.ClassDef):
                active_classes[statement.name] = statement
                continue
            if isinstance(statement, (ast.With, ast.AsyncWith)):
                walk_statements(statement.body)
                continue
            if not isinstance(statement, (ast.Expr, ast.Assign, ast.AnnAssign, ast.Assert)):
                continue
            for call in ast.walk(statement):
                if not (isinstance(call, ast.Call) and isinstance(call.func, ast.Name)):
                    continue
                owner = active_classes.get(call.func.id)
                if owner is None:
                    continue
                outcome = "expected-error" if call in negative_nodes else "joint-use"
                entry = (outcome, call.lineno)
                locations = controls.setdefault(owner, [])
                if entry not in locations:
                    locations.append(entry)

    walk_statements(test.body)
    return controls


def doctest_controls(examples):
    """Attach direct constructor outcomes to the latest example declaration."""
    active_classes, controls = {}, {}
    for index, sample in enumerate(examples):
        try:
            tree = ast.parse(sample.source)
        except SyntaxError:
            continue
        for statement in tree.body:
            if isinstance(statement, ast.ClassDef):
                if not sample.exc_msg:
                    active_classes[statement.name] = index
                continue
            if not isinstance(statement, (ast.Expr, ast.Assign, ast.AnnAssign, ast.Assert)):
                continue
            for call in ast.walk(statement):
                if not (isinstance(call, ast.Call) and isinstance(call.func, ast.Name)):
                    continue
                owner = active_classes.get(call.func.id)
                if owner is not None:
                    observation = (bool(sample.exc_msg), sample.lineno + call.lineno - 1)
                    entries = controls.setdefault(owner, [])
                    if observation not in entries:
                        entries.append(observation)
    return controls


def code_blocks(text):
    lines = text.splitlines()
    index = 0
    while index < len(lines):
        line = lines[index]
        fence = MD_FENCE.match(line)
        rst = RST_PY.match(line)
        marked_code_block = (fence and fence[2] == "{code-block}" and
                             line.split()[-1] in ("python", "py", "pycon"))
        if fence and (marked_code_block or fence[2] in ("python", "py", "pycon", "{doctest}", "{testcode}")):
            start = index + 1
            while start < len(lines) and lines[start].lstrip().startswith(":"):
                start += 1
            index = start
            while index < len(lines) and not lines[index].lstrip().startswith(fence[1]):
                index += 1
            yield start + 1, "\n".join(lines[start:index])
        elif rst:
            initial_indent = len(rst[1])
            start = index + 1
            while start < len(lines) and (not lines[start].strip() or lines[start].lstrip().startswith(":")):
                start += 1
            stop = start
            while stop < len(lines):
                row = lines[stop]
                if row.strip() and len(row) - len(row.lstrip()) <= initial_indent:
                    break
                stop += 1
            if stop > start:
                yield start + 1, "\n".join(lines[start:stop])
            index = stop - 1
        index += 1


def parse_release(repos, version_row):
    package, version, tag = (version_row[key] for key in ("package", "version", "tag"))
    repo = repos[package]
    commit = git(repo, "rev-parse", f"refs/tags/{tag}^{{commit}}").decode().strip()
    if version_row.get("commit") and commit != version_row["commit"]:
        raise ValueError(f"{package} {tag} peeled to {commit}, expected {version_row['commit']}")

    git_paths = read_tree(repo, commit)
    by_scope = {}
    for scope, patterns in (("narrow", NARROW), ("broad", NARROW + BROAD[package])):
        by_scope[scope] = {
            pattern: sorted((p for p in git_paths if re.fullmatch(pattern, p)), key=lambda p: p.encode())
            for pattern in patterns
        }
    narrow = set(p for paths in by_scope["narrow"].values() for p in paths)
    paths = sorted(set(p for paths in by_scope["broad"].values() for p in paths), key=lambda p: p.encode())
    files, contents, trees = {}, {}, {}
    failures = []
    for path in paths:
        blob = git(repo, "cat-file", "blob", git_paths[path])
        files[path] = {"path": path, "sha256": hashlib.sha256(blob).hexdigest(),
                       "git_blob": git_paths[path], "bytes": len(blob),
                       "lines": len(blob.splitlines()),
                       "url": f"https://github.com/{REMOTES[package]}/blob/{commit}/{path}"}
        try:
            contents[path] = blob.decode("utf-8")
        except UnicodeDecodeError as exc:
            failures.append(f"decoding:{path}:{exc.start}")
            continue
        if path.endswith(".py"):
            try:
                trees[path] = ast.parse(contents[path], filename=path)
            except SyntaxError as exc:
                failures.append(f"python:{path}:{exc.lineno}:{exc.msg}")
    catalog = Catalog(package, commit, contents, trees, narrow & contents.keys())
    catalog.all_paths = git_paths
    catalog.build_aliases()
    catalog.narrow_list()
    catalog.declaration_map()
    catalog.public_protocols()
    catalog.direct_exclusions()

    for path, text in contents.items():
        if path.endswith((".rst", ".md")):
            for symbol, line, kind in official_markup(text, package):
                if symbol in catalog.aliases or symbol in catalog.locations:
                    catalog.add(catalog.canonical(symbol), path, line, kind)
            catalog.document_examples(path, text)
        elif path.startswith("tests/") and path in trees:
            catalog.test_examples(path, trees[path])
    for scope in ("narrow", "broad"):
        coverage = by_scope[scope]
        covered = sorted({p for members in coverage.values() for p in members}, key=lambda p: p.encode())
        relevant_failures = [f for f in failures if f.split(":")[1] in covered]
        scope_features = catalog.rows(narrow_only=scope == "narrow")
        base_roots_read = any(p.startswith("README.") for p in covered) and any(p.startswith("docs/index.") for p in covered)
        yield {
            "id": f"{package}@{version}/{scope}", "repo": REMOTES[package], "package": package,
            "scope": scope, "version": version, "tag": tag, "commit": commit,
            "files": [files[p] for p in covered], "paths": coverage,
            "missing_path_patterns": [p for p, members in coverage.items() if not members],
            "file_count": len(covered), "summed_bytes": sum(files[p]["bytes"] for p in covered),
            "unique_bytes": sum(dict((files[p]["sha256"], files[p]["bytes"]) for p in covered).values()),
            "scan_complete": not relevant_failures and base_roots_read,
            "read_failures": relevant_failures,
            "enumeration_uncertainties": sorted(x for x in catalog.incomplete
                                                if scope == "broad" or x.startswith("menu-")),
            "doc_example_coverage_limits": catalog.doc_issues if scope == "broad" else [],
            "negative_only_pairs": [
                {"id": feature, "locations": locations}
                for feature, locations in sorted(catalog.locations.items())
                if " + " in feature and all(l.get("outcome") == "expected-error" for l in locations)
            ] if scope == "broad" else [],
            "conditional_exclusions": catalog.explicit_exclusions if scope == "broad" else [],
            "semantic_scope": (
                "Direct menu names and links only. Parent entries do not enumerate child settings."
                if scope == "narrow" else
                "File bytes scanned exhaustively. Static declarations, marked examples and direct test calls. "
                "No complete semantic proof for free text, dynamic calls, inherited methods, or decorator effects."
            ),
            "definition_count": sum(len(x["locations"]) for x in scope_features),
            "feature_count": len(scope_features),
            "combination_count": sum(x["kind"] == "combination" for x in scope_features),
            "features": scope_features,
        }


def ensure_repos(workspace, version_rows):
    repos = {}
    for package in sorted({row["package"] for row in version_rows}):
        git_dir = workspace / f"{package}.git"
        if not git_dir.exists():
            subprocess.check_call(["git", "clone", "--mirror", f"https://github.com/{REMOTES[package]}.git", str(git_dir)])
        repos[package] = git_dir
    return repos


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--versions", type=Path, required=True)
    cli.add_argument("--workspace", type=Path, required=True)
    cli.add_argument("--output", type=Path, required=True)
    args = cli.parse_args()
    versions = json.loads(args.versions.read_text())
    args.workspace.mkdir(parents=True, exist_ok=True)
    repos = ensure_repos(args.workspace, versions)
    with args.output.open("w", encoding="utf-8") as out:
        for version in sorted(versions, key=lambda x: (x["package"], x["version"])):
            for row in parse_release(repos, version):
                out.write(json.dumps(row, sort_keys=True, ensure_ascii=False, separators=(",", ":")) + "\n")


if __name__ == "__main__":
    main()
