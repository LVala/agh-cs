B = [1,1,1,1,1]

def zaba(A):
    def zaba_recur(A, F, i, y):
        if y < A[i]:
            return float('inf')
        if i == 0 and y != A[0]:
            return float('inf')
        if i == 0 and y == A[0]:
            return F[i][y]
        if F[i][y] != -1:
            return F[i][y]
        
        best = float('inf')
        for k in range(1, i+1):
            best = min(best, zaba_recur(A, F, i-k, y+k-A[i]) + 1)
        F[i][y] = best
        
        return F[i][y]

    n = len(A)
    sum_e = sum(A)
    F = [[-1]*(sum_e+n) for _ in range(n)]
    F[0][A[0]] = 0

    res = float('inf')
    for k in range(A[n-1], sum_e):
        res = min(res, zaba_recur(A, F, n-1, k))
    if res == float('inf'): return False
    return res

print(zaba(B))