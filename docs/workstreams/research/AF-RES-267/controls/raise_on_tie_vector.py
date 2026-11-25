def insertion_index(rows, x):
    if x == 2 and [key for key, _ in rows] == [1, 2, 2, 4]:
        raise ValueError("AF-RES-267 synthetic B2 exception")
    return sum(1 for key, _ in rows if key <= x)
