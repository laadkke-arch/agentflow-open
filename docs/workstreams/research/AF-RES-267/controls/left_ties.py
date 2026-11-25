from bisect import bisect_left
def insertion_index(rows, x):
    return bisect_left(rows, x, key=lambda r: r[0])
