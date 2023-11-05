from queue import PriorityQueue

def trasa(G, s, t):
    Q = PriorityQueue()
    
    n = len(G)
    dist = [float("inf")]*n
    dist[s] = 0

    Q.put((dist[s], s))

    while Q.empty() == False:
        dist_u, u = Q.get()
        if u == t: return dist[u]
        if dist_u != dist[u]: continue
        for v in range(n):
            if G[u][v] != -1 and dist[v] > dist[u] + G[u][v]:
                dist[v] = dist[u] + G[u][v]
                Q.put (( dist[v], v))
    return -1

G1 = [[-1, 0, -1, 0, -1, 1, -1, -1, -1, -1, -1],
[0, -1, 1, -1, -1, -1, -1, -1, -1, -1, -1],
[-1, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[0, -1, -1, -1, 0, -1, -1, -1, -1, -1, -1],
[-1, -1, -1, 0, -1, -1, 0, -1, -1, -1, -1],
[1, -1, -1, -1, -1, -1, 0, 0, -1, 1, -1],
[-1, -1, -1, -1, 0, 0, -1, -1, -1, -1, -1],
[-1, -1, -1, -1, -1, 0, -1, -1, 1, -1, -1],
[-1, -1, -1, -1, -1, -1, -1, 1, -1, 0, 1],
[-1, -1, -1, -1, -1, 1, -1, -1, 0, -1, -1],
[-1, -1, -1, -1, -1, -1, -1, -1, 1, -1, -1],]

print(trasa(G1, 0, 10)) 