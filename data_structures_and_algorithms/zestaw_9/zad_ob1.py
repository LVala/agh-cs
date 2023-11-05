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


G1 = [[(1,4),(7,8)],
    [(0,4),(2,8),(7,11)],
    [(1,8),(3,7),(8,2),(5,4)],
    [(2,7),(4,9),(5,14)],
    [(3,9),(5,10)],
    [(4,10),(3,14),(2,4),(6,2)],
    [(5,2),(8,6),(7,1)],
    [(6,1),(8,7),(1,11),(0,8)],
    [(2,2),(6,6),(7,7)]]

print(dijkstra(G1, 0, 4))