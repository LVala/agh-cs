# leci najdalej jak może, wtedy tankuje, O(n)
def czolg_A(L, S, t):
    n = len(S)
    count = 0
    i = 0
    start = 0
    while i < n:
        if S[i] - start > L:
            count += 1
            if start != S[i-1]: start = S[i-1]
            else: return False
            i -= 1
        i += 1
    if t - S[n - 1] <= L and i == 0: return count
    elif t - S[n - 1] <= L: return count + 1
    else: return -1

# jedzie do końcowej, gdy nie może, to do najtańszej w zasięgu
# tankuje tyle żeby dojechać do końcowej lub do kolejnej tańszej niż obecna
# przyjmuje tutaj, że S[0] to punkt startowy, a S[n] to t
# P[0] = 0, P[n-1] = 0
def czolg_B1(L, S, P):
    n = len(S)
    cur_L = 0
    cost = 0
    i = 1
    min_cost = 0
    prev_station = 0
    while i != n:
        min_cost = i
        while i < n and S[i] - S[prev_station] <= L:
            if P[i] <= P[min_cost]:
                min_cost = i
            i += 1
        if S[prev_station] - S[min_cost] > L: return -1
        if P[prev_station] <= P[min_cost]:
            cost += (L - cur_L)*P[prev_station]
            cur_L = L
        else:
            cost += max((S[min_cost] - S[prev_station] - cur_L),0) * P[prev_station]
            cur_L += max((S[min_cost] - S[prev_station] - cur_L),0)
        cur_L -= (S[min_cost] - S[prev_station])
        prev_station = min_cost
        i = min_cost + 1

    return cost

# dynamiczny ( da się od jednego argumentu)
def czolg_B2(L, S, P):
    n = len(S)
    INF = float('inf')
    F = [[INF]*(L+1) for _ in range(n)]
    F[0][L] = 0

    for i in range(1, n):
        for j in range(L):
            best = INF
            for k in range(n):
                if S[k] == S[i] + j - L:
                    for m in range(L+1):
                        best = min(best, F[k][m] + (L-m)*P[k])
            F[i][j] = best
    
    res = INF
    for i in range(L):
        res = min(res, F[n-1][i])

    return res


L1 = 14
S1 = [0, 1, 9, 15, 16, 17, 27, 28, 30]
P1 = [0, 1, 100, 10, 15, 1, 30, 30, 0]
t1 = 30

# S1 = [0,1,3,4,7]
# P1 = [0,5,2,3,0]
# L1 = 3

print(czolg_B2(L1, S1, P1))