def knapsack(W, H, P, MaxW, MaxH):  # W - masy, P - wartości
    n = len(P)
    F = [[[0] * (MaxH + 1) for _ in range(MaxW + 1)] for _ in range(n)]
    for w in range(W[0], MaxW + 1):
        for h in range(H[0], MaxH + 1):
            F[0][w][h] = P[0]

    for i in range(1, n):
        for w in range(1, MaxW + 1):
            for h in range(1, MaxH + 1):
                F[i][w][h] = F[i - 1][w][h]
                if w >= W[i] and h >= H[i]:
                    F[i][w][h] = max(F[i][w][h], F[i - 1][w - W[i]][h - H[i]] + P[i])
    return F[n - 1][MaxW][MaxH], F


def getsolution(F, W, H, P, i, w, h):
    if i == 0:
        if w >= W[0] and h >= H[0]:
            return [0]
        return []
    if w >= W[i] and h >= H[i] and F[i][w][h] == F[i - 1][w - W[i]][h - H[i]] + P[i]:
        return getsolution(F, W, H, P, i - 1, w - W[i], h - H[i]) + [i]
    return getsolution(F, W, H, P, i - 1, w, h)


P = [60, 100, 120]
W = [10, 20, 30]
H = [40, 60, 90]
MaxW = 40
MaxH = 130
res, F = knapsack(W, H, P, MaxW, MaxH)
print(res, getsolution(F, W, H, P, len(W) - 1, MaxW, MaxH))