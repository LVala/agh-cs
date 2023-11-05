
#wejście w postaci macierzy
def transitive_closure(G):
    n = len(G)
    reach = [[0]*n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            reach[i][j] =  G[i][j]

    for u in range(n):
        for v1 in range(n):
            for v2 in range(n):
                reach[v1][v2] = reach[v1][v2] or (reach[v1][u] and reach[u][v2])

    return reach

G1 = [[1, 1, 0, 1],
    [0, 1, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1]]

res = transitive_closure(G1)
for i in res:
    print(i)