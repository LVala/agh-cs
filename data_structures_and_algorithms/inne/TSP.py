# złożoność O(2^n*n^2)

def dynamic_TSP(D):
    def TSP(A, n, len_a, s):
        A[s] = -1
        if len_a == 1:
            A[s] = 1
            return D[0][s]
        
        cost = float('inf')
        for i in range(n):
            if A[i] != -1:
                cost = min(cost, TSP(A, n, len_a-1, i) + D[s][i])
        
        A[s] = 1
        return cost

    n = len(D[0])
    A = [1]*n
    cost = TSP(A, n, n, 0)

    return cost

# bitoniczny TSP, złożoność O(n^2)

def bitonic_TSP(D):
    def tspf(F, D, i, j):
        if F[i][j] != -1:
            return F[i][j]
        if i == j-1:
            best = float('inf')
            for k in range(j-1):
                best = min(best, tspf(F, D, k, j-1) + D[k][j])
            F[j-1][j] = best
        else:
            F[i][j] = tspf(F, D, i, j-1) + D[j-1][j]
        
        return F[i][j]

    n = len(D[0])
    F = [[-1]*n for _ in range(n)]
    F[0][1] = D[0][1]
    res = float('inf')
    for i in range(n-1):
        res = min(res, tspf(F, D, i, n-1) + D[i][n-1])    
    return res
