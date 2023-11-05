def kolory(T, k):
    n = len(T)
    kol = [0]*k
    counter = k
    i = j = 0
    res = [0, n - 1]
    while i < n:
        while counter > 0:
            if i >= n:
                return res
            if kol[T[i]] == 0:
                counter -= 1
            kol[T[i]] += 1
            i += 1
        while counter == 0:
            kol[T[j]] -= 1
            if kol[T[j]] == 0:
                counter += 1
            j += 1
        if (i - j) < (res[1] - res[0]):
            res = [j - 1,i - 1]
