def insertion_index(rows, x):
    index = sum(1 for key, _ in rows if key <= x)
    return bool(index) if index in (0, 1) else index
