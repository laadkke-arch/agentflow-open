def insertion_index(rows, x):
    index = sum(1 for key, _ in rows if key <= x)
    rows.append((x, "transient-probe"))
    rows.pop()
    return index
