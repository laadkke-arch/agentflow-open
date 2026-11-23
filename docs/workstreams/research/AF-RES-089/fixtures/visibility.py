"""Canonicalize objects while retaining process-local identity in the raw logs."""


def active(snapshot):
    return next(score for score in snapshot["scores"] if score["id"] == snapshot["active_score_id"])


def score_names(snapshot):
    return {score["id"]: "M" if score["master"] else score["title"] for score in snapshot["scores"]}


def object_key(item, names):
    return ":".join(str(value) for value in (
        names[item["score_id"]], item["track"], item.get("tick", "-"),
        item["type"], item.get("pitch", "-"),
    ))


def objects(snapshot):
    names = score_names(snapshot)
    result = {}
    for score in snapshot["scores"]:
        for item in score["objects"]:
            key = object_key(item, names)
            if key in result:
                raise ValueError(f"Ambiguous object key {key}")
            result[key] = item
    return result


def selected(snapshot):
    allowed = {item["id"]: key for key, item in objects(snapshot).items()}
    sel = active(snapshot)["selection"]
    return {
        **sel,
        "list": [allowed.get(pointer, f"unmapped:{pointer}") for pointer in sel["list"]],
    }


def document(snapshot):
    items = objects(snapshot)
    keys = {item["id"]: key for key, item in items.items()}
    names = score_names(snapshot)
    return {
        key: {
            "visible": item["visible"],
            "duration": item["duration"],
            "duration_ticks": item["duration_ticks"],
            "parent": keys.get(item["parent_id"]),
            "peers": sorted(keys.get(peer["id"], f"unmapped:{names[peer['score_id']]}:{peer['track']}:{peer['type']}")
                            for peer in item["peers"]),
        }
        for key, item in sorted(items.items())
    }


def visible_changes(before, after):
    first, second = document(before), document(after)
    return {key: [first[key]["visible"], second[key]["visible"]]
            for key in sorted(first.keys() & second.keys())
            if first[key]["visible"] != second[key]["visible"]}


def index(state):
    return active(state)["undo_index"]
