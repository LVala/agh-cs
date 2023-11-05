# O(n^2)

def board(A):
    n = len(A)
    F = [[0]*n for _ in range(n)]
    F[0][0] = A[0][0]
    for i in range(1, n): F[0][i] = F[0][i-1] + A[0][i]
    for i in range(1, n): F[i][0] = F[i-1][0] + A[i][0]
    
    for i in range(1, n):
        for j in range(1, n):
            F[i][j] = max(F[i-1][j], F[i][j-1])
            F[i][j] += A[i][j]

    return F[n-1][n-1]
