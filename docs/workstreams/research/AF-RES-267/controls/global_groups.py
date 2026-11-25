def runs(events):
    groups = {}
    for key, payload in events:
        groups.setdefault(key, []).append(payload)
    return list(groups.items())
