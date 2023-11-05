from queue import PriorityQueue

# input w postaci listy sąsiedztwa G[u] = [(v, w), ...]
def dijkstra(G, s, t):
    def find_sol(parent, u):
        nonlocal res
        if parent[u] == -1: 
            res.append(u)
            return
        find_sol(parent, parent[u])
        res.append(u)
    
    n = len(G)
    dist = [float("inf")]*n
    dist[s] = 0
    parent = [-1]*n
    Q = PriorityQueue()
    res = []

    for i in range(n):
        Q.put((dist[i], i))
    
    while Q.empty() == False:
        dist_u, u = Q.get()
        if dist_u != dist[u]: continue
        for v in range(len(G[u])):
            if dist[u] + G[u][v][1] < dist[G[u][v][0]]:
                dist[G[u][v][0]] = dist[u] + G[u][v][1]
                parent[G[u][v][0]] = u
                Q.put((dist[G[u][v][0]], G[u][v][0]))

    if dist[t] != float("inf"):
        find_sol(parent, t)
        return res
    else: return -1

# input w postaci listy sąsiedztwa G[u] = [(v, w), ...]
def bellman_ford(G, s, t):
    def find_sol(parent, u):
        nonlocal res
        if parent[u] == -1: 
            res.append(u)
            return
        find_sol(parent, parent[u])
        res.append(u)
    
    n = len(G)
    dist = [float("inf")]*n
    dist[s] = 0
    parent = [-1]*n
    res = []

    for _ in range(n-1):
        for u in range(n):
            for v in G[u]:
                if dist[u] + v[1] < dist[v[0]]:
                    dist[v[0]] = dist[u] + v[1]
                    parent[v[0]] = u
    
    for u in range(n):
        for v in G[u]:
            if dist[u] + v[1] < dist[v[0]]:
                return -1;

    if dist[t] != float("inf"):
        find_sol(parent, t)
        return res
    else: return -1

# input w postaci macierzy, gdzie brak krawędzi to None
# nie może zawierać ujemnych cykli
def floyd_warshall(G, s, t):
    def find_sol(parent, s, u):
        nonlocal res
        if s == u: 
            res.append(u)
            return
        find_sol(parent, s, parent[s][u])
        res.append(u)
    
    n = len(G)
    dist = [[float("inf")]*n for _ in range(n)]
    parent = [[-1]*n for _ in range(n)]
    res = []

    for i in range(n):
        for j in range(n):
            if G[i][j] != None:
                parent[i][j] = i
                dist[i][j] = G[i][j]

    for u in range(n):
        for v1 in range(n):
            for v2 in range(n):
                if dist[v1][v2] > dist[v1][u] + dist[u][v2]:
                    dist[v1][v2] = dist[v1][u] + dist[u][v2]
                    parent[v1][v2] = parent[u][v2]

    if dist[s][t] != float("inf"):
        find_sol(parent, s, t)
        return res
    else: return -1

# lista krawędzi
G1 = [[(1,4),(7,8)],
    [(0,4),(2,8),(7,11)],
    [(1,8),(3,7),(8,2),(5,4)],
    [(2,7),(4,9),(5,14)],
    [(3,9),(5,10)],
    [(4,10),(3,14),(2,4),(6,2)],
    [(5,2),(8,6),(7,1)],
    [(6,1),(8,7),(1,11),(0,8)],
    [(2,2),(6,6),(7,7)]]

G2 = [[0, 2, None, 10, 2, None], 
[2, 0, 2, None, None, None],
[None, 2, 0, 2, 1, None],
[10, None, 2, 0, None, 3],
[2, None, 1, None, 0, None], 
[None, None, None, 3, None, 0]] 

print(floyd_warshall(G2, 0, 5))
