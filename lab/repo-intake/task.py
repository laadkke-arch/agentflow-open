"""Deduplicate public repository-root references, retaining rejected inputs."""
import json
from pathlib import Path
import sys
from workbench.urls import RepositoryURL, repository_key


def collect(values):
    if not isinstance(values, list) or len(values) > 10000:
        raise ValueError("expected a list of at most 10000 inputs")
    groups, rejected = {}, []
    for index, value in enumerate(values):
        try:
            key = repository_key(value)
            groups.setdefault(key, []).append(index)
        except RepositoryURL as exc:
            # Do not echo arbitrary input: it may contain embedded credentials.
            rejected.append({"index": index, "reason": str(exc)})
    return {"repositories": [{"key": key, "input_indices": indices} for key, indices in sorted(groups.items())],
            "rejected": rejected, "input_count": len(values),
            "existence_checked": False}


if __name__ == "__main__":
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    print(json.dumps(collect(data), indent=2))
