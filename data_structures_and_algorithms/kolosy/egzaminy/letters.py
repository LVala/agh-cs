#TIME: O(V*(V*len(W))^2), SPACE: O(V^2)

def let( ch ): return ord(ch) - ord("a")

def letters( G, W ):
    def dijkstra(G, W, L, s):
        w = len(W)
        n = len(G)
        dist = [[float("inf")]*w for _ in range(n)]
        visited = [[False]*w for _ in range(n)]
        res = float("inf")
        dist[s][0] = 0

        for _ in range(w*n):
            val_u = dist[0][0]
            u1 = 0
            u2 = 0
            flag = False
            for v1 in range(n):
                if flag: break
                for v2 in range(w):
                    if not visited[v1][v2]:
                        val_u = dist[v1][v2]
                        u1 = v1
                        u2 = v2
                        flag = True
                        break
            
            for v1 in range(n):
                for v2 in range(w):
                    if visited[v1][v2] == False and dist[v1][v2] <= val_u:
                        u1 = v1
                        u2 = v2
                        val_u = dist[v1][v2]

            if dist[u1][u2] == float("inf"): break

            visited[u1][u2] = True

            if u2 == w - 1:
                res = min(res, dist[u1][u2])
                continue

            for v in range(n):
                if G[u1][v] > 0 and L[v] == W[u2 + 1]:
                    if not visited[v][u2 + 1] and dist[v][u2 + 1] > dist[u1][u2] + G[u1][v]:
                        dist[v][u2 + 1] = dist[u1][u2] + G[u1][v]

        return res
    
    
    L, E = G
    n = len(L)
    M = [[0]*n for _ in range(n)]
    for i in range(len(E)):
        M[E[i][0]][E[i][1]] = E[i][2]
        M[E[i][1]][E[i][0]] = E[i][2]

    # TUTAJ WYSTARCZY DAĆ WSZYSTKIM WIERZCHOŁKOM STARTOWYM 0 
    # I 1 DIJSKTRE ZROBIĆ
    res = float("inf")
    for i in range(n):
        if L[i] == W[0]:
            res = min(res, dijkstra(M, W, L, i))

    return res

#O(E*len(text))

def let(a):
    return ord(a) - ord('a')

class Node:
    def __init__(self,lenW):
        self.dists = [float('inf') for _ in range(lenW)]
    def relax(self,ind,new_val):
        if self.dists[ind] > new_val:
            self.dists[ind] = new_val
    def get_dist(self,ind):
        return self.dists[ind]

def letters(G,W):
    L,E = G
    n = len(L)

    nodes = [Node(len(W)) for _ in range(n)]

    for u in range(len(L)):
        if L[u] == W[0]:
            nodes[u].relax(0,0)

    for i in range(1,len(W)):
        for u,v,w in E:
            if W[i-1] == L[u] and W[i] == L[v]:
                nodes[v].relax(i,nodes[u].get_dist(i-1) + w)
            if W[i-1] == L[v] and W[i] == L[u]:
                nodes[u].relax(i,nodes[v].get_dist(i-1) + w)

    mini = float('inf')
    for elem in nodes:
        mini = min(mini,elem.get_dist(-1))
    return mini
