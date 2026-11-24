"""Two bindings from the same source conditions to the same factual observations."""
from collections import Counter
import re


def mentions(text, word, offset=0):
    # Whole English terms. Korean suffixes can follow the literal stem.
    token = re.escape(word)
    if word.isascii():
        token = rf"(?<!\w){token}(?!\w)"
    return [
        {"span": [offset + m.start(), offset + m.end()], "quote": m.group(), "label": word}
        for m in re.finditer(token, text, re.IGNORECASE)
    ]


def scan(text, vocabulary, offset):
    matches = []
    for slot, words in vocabulary.items():
        for word in words:
            matches.extend(dict(match, value=slot) for match in mentions(text, word, offset))
    return matches


def longest(matches):
    found = []
    for match in sorted(matches, key=lambda m: -(m["span"][1] - m["span"][0])):
        left, right = match["span"]
        if not any(hit["span"][0] <= left and right <= hit["span"][1] and
                   hit["span"] != match["span"] for hit in found):
            found.append(match)
    return sorted(found, key=lambda m: (m["span"], m["value"]))


def only(matches):
    values = {m["value"] for m in matches}
    return next(iter(values)) if len(values) == 1 else None


def literal(clause, fact, offset):
    entries = [mentions(clause, word, offset) for word in fact["literal"]["keys"]]
    if not all(entries):
        return None, "literal_key_missing", [e for group in entries for e in group]
    return fact["literal"]["desired"], "literal_keys", [e for group in entries for e in group]


def parse_slots(text, span, criterion, public_map, rules):
    start, end = span
    clause = text[start:end]
    actions = dict(rules["slots"]["action"])
    for action, words in public_map["literal_action_labels"].items():
        actions[action] = [*actions.get(action, []), *words]
    actions_found = longest(scan(clause, actions, start))
    polarity_found = longest(scan(clause, rules["slots"]["polarity"], start))
    scope_found = longest(scan(clause, {s: rules["slots"]["scope"][s] for s in ("one", "all")}, start))
    role_found = longest(scan(clause, {s: rules["slots"]["scope"][s] for s in ("source", "copy")}, start))
    objects = public_map["objects"]
    named = longest(scan(clause, {o["id"]: o["names"] for o in objects}, start))
    affected = only(named)
    action = only(actions_found)
    has_forbid = any(m["value"] == "forbid" for m in polarity_found)
    has_allow = any(m["value"] == "allow" for m in polarity_found)
    polarity = "permit" if has_allow else "forbid" if has_forbid else "require"
    role = only(role_found)
    subject_resolution = "literal_spans" if affected else "unresolved"
    if not named and role:
        candidates = [o["id"] for o in objects if o["role"] == role]
        if len(candidates) == 1:
            affected = candidates[0]
            subject_resolution = "inferred_unique_role"
    if len({m["value"] for m in named}) > 1 and action:
        # A selected actor may precede a reference destination. A value copied
        # may follow the verb before an "of/from" complement. Keep ambiguity otherwise.
        anchor = next((m for m in actions_found if m["value"] == action), None)
        if anchor and action == "unlink":
            subjects = [m for m in named if m["span"][1] <= anchor["span"][0]]
            affected = only(subjects)
        if anchor and action == "copy":
            tail = text[anchor["span"][1]:end]
            sep = re.search(r"\b(?:of|from)\b", tail, re.IGNORECASE)
            boundary = anchor["span"][1] + (sep.start() if sep else len(tail))
            nearby = [m for m in named if anchor["span"][1] <= m["span"][0] < boundary]
            affected = only(nearby)
        if affected:
            subject_resolution = "inferred_clause_role"
    scope = only(scope_found)
    if not scope_found and affected:
        item = next(o for o in objects if o["id"] == affected)
        scope = item["role"] if item["role"] in ("one", "all") else None
    if not affected and not named and scope:
        unique = [o["id"] for o in objects if o["role"] == scope]
        if len(unique) == 1 and not re.search(r"\b(?:it|them|that|those|these)\b", clause, re.IGNORECASE):
            affected = unique[0]
            subject_resolution = "inferred_unique_quantifier_role"
    if criterion == "preserve" and action in {"edit", "move", "remove"} and polarity == "forbid":
        action, polarity = "keep", "require"
    return {
        "action": action, "polarity": polarity, "target": affected,
        "preserved_target": affected if criterion == "preserve" else None,
        "range": scope, "target_origin": subject_resolution,
        "conflicting_range": bool(scope_found and not scope),
        "named": named, "action_mentions": actions_found, "polarity_mentions": polarity_found,
        "range_mentions": scope_found, "role_mentions": role_found,
    }


def scoped(slots, fact, text, public_map):
    if not slots["action"] or not slots["target"]:
        return None, "action_or_target_unresolved"
    if slots["conflicting_range"]:
        return None, "range_conflict"
    if slots["action"] != fact["action"] or slots["target"] != fact["target"]:
        return None, "different_action_or_target"
    if fact["scope"] and slots["range"] and fact["scope"] != slots["range"]:
        return None, "different_range"
    if fact["scope"] and not slots["range"] and fact["required_relation"] is None:
        return None, "range_unresolved"
    relation = fact["required_relation"]
    if relation:
        item = next(o for o in public_map["objects"] if o["id"] == relation)
        discriminators = [n for n in item["names"] if "same" in n or "/" in n]
        if not any(mentions(text, term) for term in discriminators):
            return None, "identity_relation_unresolved"
    if slots["polarity"] == "permit":
        return None, "permission_without_truth_obligation"
    return slots["polarity"] == "require", "compatible_slots"


def select(method, request, case, rules):
    """Return the proof relation and the trace without looking at expected answers."""
    links = []
    facts = case["evidence"]
    version = case["context"]["version"]
    name_counts = Counter(
        name.casefold() for obj in case["public_map"]["objects"] for name in set(obj["names"])
    )
    ambiguous_names = [name for name, count in name_counts.items() if count > 1]
    for criterion, span in request["parts"].items():
        slots = (
            parse_slots(request["text"], span, criterion, case["public_map"], rules)
            if method == "B" and span is not None else None
        )
        if slots is not None:
            slots = dict(slots, edition=version, edition_origin=case["context"]["version_origin"])
        budget = rules["budget"]["fragments_per_condition"]
        eligible = [f for f in facts if f["criterion"] == criterion][:budget]
        duplicate_name = span is not None and any(
            mentions(request["text"][slice(*span)], name) for name in ambiguous_names
        )
        for fact in eligible:
            minimal_matches = []
            wanted = None
            if span is None:
                reason = "required_span_missing"
            elif not version or fact["version"] != version:
                reason = "unknown_or_different_edition"
            elif duplicate_name:
                reason = "ambiguous_public_identity"
            elif method == "A":
                start, end = span
                wanted, reason, minimal_matches = literal(request["text"][start:end], fact, start)
            else:
                wanted, reason = scoped(slots, fact, request["text"], case["public_map"])
            direction = None
            if wanted is not None and fact["observed"] is not None:
                direction = "support" if wanted == fact["observed"] else "refute"
            elif wanted is not None:
                reason = "observation_missing"
            links.append({
                "criterion": criterion, "evidence_id": fact["evidence_id"],
                "direction": direction, "reason": reason, "slots": slots,
                "surface_spans": minimal_matches, "request_span": span,
            })
    return links


def evaluate(candidate, criteria, claims):
    """The shared condition evaluator requires direct evidence for each condition."""
    outcomes = {}
    for requirement in criteria:
        key = requirement["id"]
        supported, refuted = [], []
        for claim in claims:
            if claim["criterion"] != key or claim["kind"] != "direct":
                continue
            if claim["context"] != candidate["context"]:
                continue
            (supported if claim["direction"] == "support" else refuted).append(claim["id"])
        if supported and refuted:
            state = "conflicting"
        elif refuted:
            state = "refuted"
        elif supported:
            state = "supported"
        else:
            state = "unknown"
        outcomes[key] = {"state": state, "used": sorted(supported + refuted)}
    mandatory = [outcomes[c["id"]]["state"] for c in criteria if c["required"]]
    status = "pending"
    if "refuted" in mandatory:
        status = "excluded"
    elif mandatory and all(state == "supported" for state in mandatory):
        status = "verified"
    return {"status": status, "criteria": outcomes}
