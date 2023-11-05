# O(n^3)

def matrix_order(A):
    n = len(A) - 1
    INF = float('inf')
    
    F = [[INF]*n for _ in range(n)]
    for i in range(n):
        F[i][i] = 0
    
    for L in range(1, n):
        for i in range(0, n-L):
            j = i + L
            for k in range(i, j):
                F[i][j] = min(F[i][j], F[i][k] + F[k+1][j] + A[i]*A[k+1]*A[j+1])

    return F[0][n-1]