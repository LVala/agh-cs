# niepełne rozwiązanie, nie działa


def opt_sum(tab):
    def get_sum(sums, i, j):
        if i == 0:return sums[j]
        return sums[j]-sums[i-1]
    
    n = len(tab)
    D = [[float("inf")]*n for _ in range(n)]
    sums = [0]*n
    sums[0] = tab[0]
    for i in range(1, n):
        sums[i] = tab[i] + sums[i-1]
    
    for i in range(n):
        D[i][i] = tab[i]

    for L in range(2, n):
        for i in range(0, n-L+1):
            j = i + L
            for k in range(i+1, j):
                D[i][j] = min(D[i][j], max(D[i][k], D[k+1][j]))
            D[i][j] = max(D[i][j], get_sum(sums, i, j))

    return D[0][n-1]
