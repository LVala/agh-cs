def partition(T, left, right):
    pivot = T[right]
    j = left
    for i in range(left, right + 1):
        if T[i] <= pivot:
            T[i], T[j] = T[j], T[i]
            j += 1
    return j - 1

def quickselect(T, left, right, k):
    if left == right:
        return T[left]
    mid = partition(T, left, right)
    if mid == k:
        return T[mid]
    elif k < mid:
        quickselect(T, left, mid - 1, k)
    else:
        quickselect(T, mid + 1, right, k)

def sum_between(T, left, right):
    n = len(T)
    min_val = quickselect(T, 0, n - 1, left)
    max_val = quickselect(T, 0, n - 1, right)

    res = 0
    for i in range(n):
        if T[i] >= min_val and T[i] <= max_val:
            res += T[i]

    return res


arr = [1,2,4,5,6,7,3]
