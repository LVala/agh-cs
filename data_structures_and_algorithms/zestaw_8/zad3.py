from queue import Queue

#BFS tylko z badaniem odległości
#DFS do znalezienia ścieżki

def path(G, s, t):
    def DFS_visit(G, u):
        nonlocal dist, t, res, flag
        if u == t:
            flag = True
            res[dist[u]] = u
            return
        for v in G[u]:
            if dist[v] == dist[u] + 1:
                DFS_visit(G, v)
                if flag == True:
                    res[dist[u]] = u
                    return

    Q = Queue()
    dist = [-1]*len(G)
    r_dist = 0

    dist[s] = 0
    Q.put(s)

    while Q.empty() == False:
        u = Q.get()
        for v in G[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                if v == t: r_dist = dist[v]
                Q.put(v)

    flag = False
    res = [0]*(r_dist + 1)
    DFS_visit(G, s)

    return res


G1 = [[1,2],[0,3],[0,5],[1,4],[3],[2]]

print(path(G1,0,5))