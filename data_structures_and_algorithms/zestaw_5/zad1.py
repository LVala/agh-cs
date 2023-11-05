# O(n*sum(P)])

def knapsack2(W, P, MaxW):
    n = len(W)
    p_sum = sum(P)
    w_sum = sum(W)
    print(p_sum)
    F = [[w_sum + 1]*(p_sum + 1) for _ in range(n)]
    for p in range(P[0] + 1):
        F[0][p] = W[0]
    for i in range(n):
        F[i][0] = 0
    for i in range(1, n):
        for p in range(1, p_sum + 1):
            F[i][p] = F[i-1][p]
            if p >= P[i]:
                F[i][p] = min(F[i][p], F[i-1][p-P[i]] + W[i])
            else:
                F[i][p] = min(F[i][p], W[i])

    for i in F:
        print(i)

    for i in range(p_sum + 1):
        if i + 1 == p_sum + 1 or F[n-1][i+1] > MaxW:
            return i