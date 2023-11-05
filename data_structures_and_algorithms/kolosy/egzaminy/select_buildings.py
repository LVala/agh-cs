#TIME: O(n^2*p)

def select_buildings(T, p):
    def a(T, i):
        return T[i][0]*(T[i][2]-T[i][1])

    def is_valid(T, i):
        i -= 1
        n = len(T)
        a = T[i][1]
        for j in range(i-1, -1, -1):
            if T[j][2] < a: return j + 1
        return 0

    def get_solution(F, i, j):
        nonlocal T, n, p, res
        if i == 0: return
        if F[i][j] == F[i-1][j]:
            get_solution(F, i-1, j)
            return
        v = is_valid(T, i)
        if F[i][j] == F[v][j-T[i-1][3]] + a(T, i-1):
            get_solution(F, v, j-T[i-1][3])
            res.append(T[i-1][4])
            return
    
    n = len(T)
    for i in range(n):
        T[i] = [T[i][0], T[i][1], T[i][2], T[i][3], i]

    T.sort(key=lambda x:x[2])
    F = [[0]*(p) for _ in range(n+1)]

    for i in range(1, n+1):
        for w in range(p):
            v = is_valid(T, i)
            F[i][w] = max(F[i][w], F[i-1][w])
            if w - T[i-1][3] >= 0:
                F[i][w] = max(F[i][w], F[v][w-T[i-1][3]] + a(T, i-1))

    i = p-1
    while F[n][i] == F[n][p-1]: i -= 1

    res = []
    get_solution(F, n, i+1)
    res.sort()

    return res
