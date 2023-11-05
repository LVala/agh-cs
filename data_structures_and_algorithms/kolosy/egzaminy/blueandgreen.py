import copy, collections

#TIME: O(V^3 + VE^2) ~ O(VE^2), SPACE(V^2)

def bfs(graph, s, t, parent):
    visited = [False] * len(graph)
    queue = collections.deque()
    queue.append(s)
    visited[s] = True
    while queue:
        u = queue.popleft()
        for ind, val in enumerate(graph[u]):
            if (visited[ind] == False) and (val > 0):
                queue.append(ind)
                visited[ind] = True
                parent[ind] = u
    return visited[t]

def edmonds_karp(graph, source, sink):
    parent = [-1] * len(graph)
    max_flow = 0
    while bfs(graph, source, sink, parent):
        path_flow = float("Inf")
        s = sink
        while s != source:
            path_flow = min(path_flow, graph[parent[s]][s])
            s = parent[s]
        max_flow += path_flow
        v = sink
        while v != source:
            u = parent[v]
            graph[u][v] -= path_flow
            graph[v][u] += path_flow
            v = parent[v]
    return max_flow

def floyd_warshall(G):
    n = len(G)
    dist = [[float("inf")]*(n+2) for _ in range(n+2)]

    for i in range(n):
        for j in range(n):
            dist[i][i] = 0
            if G[i][j] > 0:
                dist[i][j] = G[i][j]

    for u in range(n):
        for v1 in range(n):
            for v2 in range(n):
                if dist[v1][v2] > dist[v1][u] + dist[u][v2]:
                    dist[v1][v2] = dist[v1][u] + dist[u][v2]

    return dist

def BlueAndGreen(T, K, D):
    n = len(T)
    G = floyd_warshall(T)
    G[n][n+1] = 0
    G[n+1][n] = 0
    G[n][n] = 0
    G[n+1][n+1] = 0
    
    for i in range(n):
        G[i][n] = 0
        G[n+1][i] = 0
        if K[i] == "B": G[n][i] = 1
        else: G[n][i] = 0
        if K[i] == "G": G[i][n+1] = 1
        else: G[i][n+1] = 0
    
    for i in range(n):
        for j in range(n):
            if G[i][j] >= D: G[i][j] = 1
            else: G[i][j] = 0

    res = edmonds_karp(G, n, n+1)

    return res
