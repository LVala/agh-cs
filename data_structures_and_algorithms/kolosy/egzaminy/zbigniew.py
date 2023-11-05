#TIME: O(n^2 * E), SPACE: O(n*E)

def zbigniew( A ):
    E = sum(A)
    n = len(A)
    D = [[float("inf")]*(E+1) for _ in range(n)]
    D[0][A[0]] = 0

    for i in range(1, n):
        for y in range(E+1):
            for k in range(1, i+1):
                if y+k-A[i] >= k and y+k-A[i] <= E:
                    D[i][y] = min(D[i][y], D[i-k][y+k-A[i]] + 1)


    return min(D[n-1])

