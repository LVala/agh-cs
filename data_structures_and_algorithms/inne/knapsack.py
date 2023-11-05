# O(n*MaxW)

def knapsack(W, P, MaxW):
    n = len(W)
    F = [[0]*(MaxW + 1) for _ in range(n)]
    for w in range(W[0], MaxW + 1):
        F[0][w] = P[0]
    for i in range(1, n):
        for w in range(1, MaxW + 1):
            F[i][w] = F[i-1][w]
            if w >= W[i]:
                F[i][w] = max(F[i][w], F[i-1][w - W[i]] + P[i])
    return F[n-1][MaxW]

def getsolution(F, W, P, i, w):
    if i == 0:
        if w >= W[0]: return [0]
        return []
    if w >= W[i] and F[i][w] == F[i-1][w - W[i]]:
        return getsolution(F, W, P, i-1, w-W[i]) + P[i]
    return getsolution(F, W, P, i-1, w)


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

W1 = [1,2,3,4]
P1 = [1,2,4,6]
MaxW1 = 100

print(knapsack2(W1, P1, MaxW1))
