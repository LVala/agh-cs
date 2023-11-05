#TIME: O((V*d)^2), SPACE: O(V*d)

def jak_dojade(G, P, d, a, b):
    def get_res(parent, u1, u2):
        nonlocal res
        if parent[u1][u2] == -1:
            res.append(u1)
            return
        get_res(parent, parent[u1][u2][0], parent[u1][u2][1])
        res.append(u1)
        return

    n = len(G)
    dist = [[float("inf")]*(d+1) for _ in range(n)]
    visited = [[False]*(d+1) for _ in range(n)]
    parent = [[-1]*(d+1) for _ in range(n)]
    stations = [False]*n
    for i in P:
        stations[i] = True
    for i in range(d+1):
        dist[a][i] = 0

    for _ in range((d+1)*n):
        val_u = dist[0][0]
        u1 = 0
        u2 = 0
        flag = False

        for v1 in range(n):
            if flag: break
            for v2 in range((d+1)):
                if not visited[v1][v2]:
                    u1 = v1
                    u2 = v2
                    val_u = dist[v1][v2]
                    flag = True
                    break

        for v1 in range(n):
            for v2 in range((d+1)):
                if not visited[v1][v2] and dist[v1][v2] < val_u:
                    u1 = v1
                    u2 = v2
                    val_u = dist[v1][v2]


        visited[u1][u2] = True

        for v in range(n):
            if G[u1][v] != -1 and G[u1][v] <= u2:
                if not stations[v] and not visited[v][u2-G[u1][v]] and dist[v][u2-G[u1][v]] > dist[u1][u2] + G[u1][v]:
                    dist[v][u2-G[u1][v]] = dist[u1][u2] + G[u1][v]
                    parent[v][u2-G[u1][v]] = (u1,u2)
                if stations[v] and not visited[v][d] and dist[v][d] > dist[u1][u2] + G[u1][v]:
                    dist[v][d] = dist[u1][u2] + G[u1][v]
                    parent[v][d] = (u1,u2)

    u2 = 0
    for i in range(d+1):
        if dist[b][i] < dist[b][u2]: u2 = i
    
    if dist[b][u2] == float("inf"): return None
    
    res = []
    get_res(parent, b, u2)

    return res
