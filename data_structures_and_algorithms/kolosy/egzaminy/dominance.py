#TIME: O(nlogn), SPACE: O(n)

def mergesort(T, flag):
    def merge(T, p, q, r):
        nonlocal flag
        n1 = q - p
        n2 = r - q
        L = [0 for i in range(n1)]
        R = [0 for i in range(n2)]
        for i in range(n1):
            L[i] = T[p + i]
        for i in range(n2):
            R[i] = T[q + i]
        i = j = 0
        for k in range(p, p + n1 + n2):
            if i < len(L) and (j >= len(R) or L[i][flag] <= R[j][flag]):
                T[k] = L[i]
                i += 1
            else:
                T[k] = R[j]
                j += 1
        return T

    def mergesort1(T, p, r):
        nonlocal flag
        if p < r - 1:
            q = (p+r)//2
            mergesort1(T, p, q)
            mergesort1(T, q, r)
            merge(T, p, q, r)

    mergesort1(T, 0, len(T))

def dominance(P):
    n = len(P)
    F = [[0]*4 for _ in range(n)]
    for i in range(n):
        F[i][0] = P[i][0]
        F[i][1] = P[i][1]
        F[i][2] = i

    # zlożoność niby O(nlogn), ale tego sorta 3 razy używam, wychodzi 
    # taki trochę radix
    mergesort(F, 1)
    mergesort(F, 0)

    for i in range(n):
        F[i][3] = i

    print(F)

    mergesort(F, 1)

    print(F)

    r = n+1
    res = []
    for i in range(n):
        if F[i][3] < r:
            res.append(F[i][2])
            r = F[i][3]
            
    return res
