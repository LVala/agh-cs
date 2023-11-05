from random import randint

def quick_select(T, left, right, k):
    def partition(T, left, right):
        pivot = T[randint(left, right)]
        for i in range(left, right + 1):
            if T[i] == pivot:
                T[i], T[right] = T[right], T[i]
        i = left
        for j in range(left, right + 1):
            if T[j] <= pivot:
                T[i], T[j] = T[j], T[i]
                i += 1
        return i - 1
   
    if left == right:
        return T[left]
    q = partition(T, left, right)
    if q == k:
        return T[q]
    elif k < q:
        return quick_select(T, left, q-1, k)
    else:
        return quick_select(T, q+1, right, k)