#O(n) ale worst O(n^2)

def quick_select(A, p, r, k):
    def partition(T, p, r):
        x = T[r]
        i = p
        for j in range(p, r + 1):
            if T[j] <= x:
                T[i], T[j] = T[j], T[i]
                i += 1
        return i - 1
   
    if p == r:
        return A[p]
    q = partition(A, p, r)
    if q == k:
        return A[q]
    elif k < q:
        return quick_select(A, p, q-1, k)
    else:
        return quick_select(A, q+1, r, k)
