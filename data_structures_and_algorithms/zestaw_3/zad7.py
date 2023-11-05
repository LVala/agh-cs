def hoare(T, left, right):
    pivot = T[(left + right)//2]
    i = left - 1
    j = right + 1
    while True:
        while True:
            i += 1
            if T[i] >= pivot:
                break
        while True:
            j -= 1
            if T[j] <= pivot:
                break
        if i >= j:
            return j
        T[i], T[j] = T[j], T[i]
