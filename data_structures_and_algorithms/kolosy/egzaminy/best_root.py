from queue import Queue

#TIME: O(V+E), SPACE: O(V)

def best_root( L ):
    def BFS(G, s):
        Q = Queue()
        visited = [False]*len(G)
        dist = [float("inf")]*len(G)
        
        visited[s] = True
        dist[s] = 0
        Q.put(s)
        res = s

        while Q.empty() == False:
            u = Q.get()
            if dist[u] > dist[res]: res = u
            for v in G[u]:
                if visited[v] == False:
                    visited[v] = True
                    dist[v] = dist[u] + 1
                    Q.put(v)
        
        return res, dist

    n = len(L)
    a, _ = BFS(L, 0)
    b, a_dist = BFS(L, a)
    _, b_dist = BFS(L, b)
    
    res = a
    for i in range(n):
        if max(a_dist[i], b_dist[i]) < max(a_dist[res], b_dist[res]): res = i

    return res
