# O(m*n)

def LCS(A, B):
    n = len(A)
    m = len(B)
    
    F = [[0]*(m) for _ in range(n)]
    if A[0] == B[0]:
        for i in range(n): F[i][0] = 1
        for i in range(m): F[0][i] = 1
    
    for i in range(1, n):
        for j in range(1, m):
            if A[i] == B[j]:
                F[i][j] = F[i-1][j-1] + 1
            else:
                F[i][j] = max(F[i-1][j], F[i][j-1])

    return F[n-1][m-1]

A1 = [0,4,6,3,7,8,2]
B1 = [1,3,6,7,2,8]

print(LCS(A1, B1))