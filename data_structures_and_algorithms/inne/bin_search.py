def bin_search(T, k):
    l = 0
    r = len(T) - 1
    while l <= r:
        m = (l + r)//2
        if T[m] < k:
            l = m + 1
        elif T[m] > k:
            r = m - 1
        else:
            return m
    return False

