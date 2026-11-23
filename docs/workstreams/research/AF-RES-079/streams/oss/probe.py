"""Read-only public API probes; records the installed version, never emulates it.

Run under each explicitly provisioned historical Python/SciPy environment to
replace the currently unobserved native 1.4.1/1.5.0/1.5.4/1.6.0 results.
Inputs are researcher-defined discriminators except provider examples noted.
This script does not install packages or access the network.
"""
import argparse
import datetime
import hashlib
import json
import platform
import shlex
import sys
import warnings
from pathlib import Path

import numpy as np
import scipy
from scipy import stats, integrate, ndimage, spatial


def serial(x):
    if isinstance(x, np.ndarray):
        return {"dtype": str(x.dtype), "shape": list(x.shape),
                "values": serial(x.tolist())}
    if isinstance(x, np.generic):
        return {"dtype": str(x.dtype), "value": serial(x.item())}
    if isinstance(x, (list, tuple)):
        return [serial(v) for v in x]
    if isinstance(x, complex):
        return {"real": x.real, "imag": x.imag}
    if isinstance(x, float) and not np.isfinite(x):
        return repr(x)
    return x


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    rows = []
    environment = {"python": platform.python_version(), "numpy": np.__version__,
                   "scipy": scipy.__version__, "platform": platform.platform()}
    def run(eid, case, name, fn, input_description):
        row = {"observation_id": eid + "-RUN-" + case + "-" + name,
               "event_id": eid, "case": case, "api": name,
               "environment": environment, "input": input_description,
               "checked_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
               "kind": "native_installed_version_observation",
               "selected_historical_release": scipy.__version__ in ["1.4.1", "1.5.0", "1.5.4", "1.6.0"],
               "historical_pair_claim": False}
        try:
            with warnings.catch_warnings(record=True) as caught:
                warnings.simplefilter("always")
                row["output"] = serial(fn())
            row["warnings"] = [{"type": w.category.__name__, "message": str(w.message)} for w in caught]
            row["outcome"] = "returned"
        except Exception as exc:
            row["outcome"] = "exception"
            row["exception"] = {"type": type(exc).__name__, "message": str(exc)}
        rows.append(row)

    for case, data, kwargs in [
        ("normal", [1., 3., 2.], {}),
        ("provider_axis", [[10., 7., 4.], [3., 2., 1.]], {"axis": None}),
        ("empty_2d", np.ones((3, 0)), {"axis": 1}),
        ("float32", np.array([1., 3., 2.], dtype=np.float32), {}),
        ("invalid_axis", [1., 3., 2.], {"axis": 9}),
        ("nan_raise", [1., np.nan, 2.], {"nan_policy": "raise"}),
    ]:
        for name in ["median_absolute_deviation", "median_abs_deviation"]:
            run("O01", case, name, lambda d=data,k=kwargs,n=name: getattr(stats,n)(d, **k),
                {"data": serial(np.asarray(data)), "kwargs": kwargs})
    run("O01", "preserve_old_scale", "median_abs_deviation", lambda: stats.median_abs_deviation([1.,3.,2.], scale=1/1.4826),
        {"data": [1.,3.,2.], "scale": 1/1.4826})

    for case,y,x,kwargs in [
        ("normal",[1.,3.,2.],[0.,1.,2.],{}),
        ("reverse",[1.,3.,2.],[2.,1.,0.],{}),
        ("empty",[],[],{}),
        ("singleton",[1.],[0.],{}),
        ("float32",np.array([1.,3.,2.],dtype=np.float32),None,{}),
        ("complex",[1+2j,3+1j,2+3j],None,{}),
        ("axis",[[1.,3.,2.],[2.,6.,4.]],None,{"axis":1}),
        ("invalid_axis",[1.,3.,2.],None,{"axis":9}),
        ("mismatched_x",[1.,3.,2.],[0.,1.,2.,3.],{}),
    ]:
        for name in ["trapz","trapezoid"]:
            run("O02",case,name,lambda a=y,b=x,k=kwargs,n=name:getattr(integrate,n)(a,x=b,**k),
                {"y":serial(np.asarray(y)),"x":x,"kwargs":kwargs})
    for name in ["trapz","trapezoid"]:
        run("O02","distribution_alias", "stats."+name, lambda n=name:getattr(stats,n).pdf([0.,0.5,1.],0,1),
            {"x":[0.,0.5,1.],"c":0,"d":1,"note":"provider PR12934 uniform-distribution alias discriminator"})
    run("O02", "wrong_namespace", "stats.trapezoid", lambda: type(stats.trapezoid([1.,3.,2.], [0.,1.,2.])).__name__,
        {"positional_arguments": [[1.,3.,2.],[0.,1.,2.]], "expected_role": "numeric integration result", "kind": "research negative probe; not an additional natural event"})

    tree=spatial.KDTree([[0.],[1.],[2.]])
    for case,radius in [("normal",1.1),("exact_boundary",1.0)]:
        run("O03",case,"KDTree.query",lambda r=radius:tree.query([0.],k=None,distance_upper_bound=r),
            {"points":[[0.],[1.],[2.]],"query":[0.],"k":None,"distance_upper_bound":radius})
        run("O03",case,"KDTree.query_ball_point",lambda r=radius:tree.query_ball_point([0.],r),
            {"points":[[0.],[1.],[2.]],"query":[0.],"r":radius})
    for name in ["query","query_ball_point"]:
        run("O03","complex_query",name,
            lambda n=name:getattr(tree,n)([0.+1j],**({"k":None,"distance_upper_bound":1.1} if n=="query" else {"r":1.1})),
            {"query":"[0+1j]"})

    for case,data,labels,index in [
        ("provider",[[1,2],[3,4]],[[1,2],[2,4]],[4,8,2]),
        ("float32",np.array([[1,2],[3,4]],dtype=np.float32),[[1,2],[2,4]],[4,8,2]),
        ("complex",np.array([[1,2],[3,4]],dtype=complex),[[1,2],[2,4]],[4,8,2]),
        ("wrong_shape",[[1,2],[3,4]],[1,2,3],[1,2]),
        ("empty",np.array([]),None,None),
    ]:
        for name in ["sum","sum_labels"]:
            run("O04",case,name,lambda a=data,b=labels,c=index,n=name:getattr(ndimage,n)(np.asarray(a),labels=b,index=c),
                {"input":serial(np.asarray(data)),"labels":labels,"index":index})

    out=Path(args.output)
    out.write_text(''.join(json.dumps(row,ensure_ascii=False,allow_nan=False)+'\n' for row in rows))
    receipt={"environment":environment,"checked_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
             "command":shlex.join([sys.executable, "-B", *sys.argv]),
             "argv":[sys.executable, "-B", *sys.argv], "cwd":str(Path.cwd()),
             "runner":"oss_evidence agent via local tools.exec_command",
             "exit_code":0,"rows":len(rows),
             "script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
             "result_sha256":hashlib.sha256(out.read_bytes()).hexdigest(),
             "limit":"Only the installed release above was executed. Historical editions require separate compatible environments."}
    out.with_suffix('.receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(receipt,ensure_ascii=False))


if __name__ == '__main__':
    main()
