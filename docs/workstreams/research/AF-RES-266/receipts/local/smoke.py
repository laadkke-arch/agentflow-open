"""Check a reproducible operation and a loaded native SciPy member from the exact wheel."""
import hashlib
import json
import platform
import sys
import sysconfig
from importlib.metadata import distribution
from pathlib import Path
from zipfile import ZipFile

import numpy as np
import scipy
from scipy import linalg
from scipy.linalg import _fblas

wheel = Path(sys.argv[1])
assert sys.version_info[:2] == (3, 13) and sys._is_gil_enabled()
assert sys.implementation.name == "cpython" and sysconfig.get_config_var("Py_GIL_DISABLED") == 0
assert platform.machine() == "x86_64" and platform.libc_ver()[0] == "glibc"
assert scipy.__version__ == "1.14.1" and np.__version__ == "2.1.3"
prefix = Path(sys.prefix)
assert Path(scipy.__file__).is_relative_to(prefix)
assert Path(np.__file__).is_relative_to(prefix)
installed = Path(_fblas.__file__)
member = "scipy/linalg/" + installed.name
with ZipFile(wheel) as archive:
    wheel_binary_sha = hashlib.sha256(archive.read(member)).hexdigest()
installed_sha = hashlib.sha256(installed.read_bytes()).hexdigest()
assert installed_sha == wheel_binary_sha
matrix = np.array([[3.0, 1.0], [1.0, 2.0]])
rhs = np.array([9.0, 8.0])
solution = linalg.solve(matrix, rhs)
max_error = float(np.max(np.abs(solution - [2.0, 3.0])))
assert max_error <= 1e-12
with wheel.open("rb") as stream:
    wheel_digest = hashlib.file_digest(stream, "sha256").hexdigest()
print(json.dumps({
    "python_version": sys.version, "soabi": sysconfig.get_config_var("SOABI"),
    "platform": platform.platform(), "libc": platform.libc_ver(), "gil": sys._is_gil_enabled(),
    "scipy": scipy.__version__, "numpy": np.__version__, "scipy_module": scipy.__file__,
    "wheel_name": wheel.name, "wheel_sha256": wheel_digest, "native_member": member,
    "installed_native_sha256": installed_sha, "wheel_native_sha256": wheel_binary_sha,
    "direct_url": json.loads(distribution("scipy").read_text("direct_url.json") or "null"),
    "matrix": matrix.tolist(), "rhs": rhs.tolist(), "solution": solution.tolist(),
    "max_abs_error": max_error, "tolerance": 1e-12,
}, indent=2))
