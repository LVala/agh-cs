#TIME: O(V^2*n + V^2), SPACE: O(V^2)
# n - długość liczby

def dijkstra(G, s ,t):
    n = len(G)
    dist = [float("inf")]*n
    visited = [False]*n
    dist[s] = 0

    for _ in range(n):
        u = -1
        val_u = float("inf")
        for v in range(n):
            if visited[v] == False and dist[v] <= val_u:
                u = v
                val_u = dist[v]

        if dist[u] == float("inf"): break
        visited[u] = True

        for v in range(n):
            if G[u][v] > 0 and visited[v] == False and dist[v] > dist[u] + G[u][v]:
                dist[v] = dist[u] + G[u][v]

    return dist[t]

def if_edge(a, b):
    A = [False for _ in range(10)]
    while a > 0:
        A[a%10] = True
        a //= 10
    
    while b > 0:
        if A[b%10]: return True
        b //= 10

    return False

def find_cost(P):
    n = len(P)
    G = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if if_edge(P[i], P[j]):
                G[i][j] = abs(P[i]-P[j])
                G[j][i] = abs(P[i]-P[j])
    a = 0
    b = 0
    for i in range(n):
        if P[i] < P[a]: a = i
        if P[i] > P[b]: b = i

    res = dijkstra(G, a, b)
    if res == float("inf"): return -1
    return res
