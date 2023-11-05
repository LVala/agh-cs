from queue import Queue

# reprezentacja przez listę sąsiedztwa
def is_bipartite(G):
    def BFS(G, s):
        nonlocal visited
        Q = Queue()
        
        visited[s] = 1
        Q.put(s)

        while Q.empty() == False:
            u = Q.get()
            for v in G[u]:
                if visited[v] == False:
                    visited[v] = (-1)*visited[u]
                    Q.put(v)
                else:
                    if visited[u] == visited[v]:
                        return False

        return True

    visited = [False]*len(G)
    for u in range(len(G)):
        if visited[u] == False:
            if BFS(G, u) == False: return False
    return True

G1 = [[2,3],[2,4],[0,1],[0],[1]]

print(is_bipartite(G1))


def connected_components(G):
    def DFS_visit(G, u, flag=False):
        nonlocal time, time_tab, visited, res
        visited[u] = True
        if flag != False:
            res[u] = flag
        for v in G[u]:
            if visited[v] == False:
                DFS_visit(G, v, flag)
        if flag == False:
            time_tab.append((time, u))
            time += 1

    n = len(G)
    time = 0
    time_tab = []
    visited = [False]*n

    for i in range(n):
        if visited[i] == False:
            DFS_visit(G, i)

    visited = [False]*n
    res = [-1]*n
    
    G_rev = [[] for _ in range(n)]
    for i in range(n):
        for j in G[i]:
            G_rev[j].append(i)

    f = 1
    for i in range(n-1, -1, -1):
        if visited[i] == False:
            DFS_visit(G_rev, time_tab[i][1], f)
            f += 1

    return res


G1 = [[1],[2],[0,3],[1],[3,7],[4,1],[5],[6],[7,9],[0,10],[2,8]]
print(connected_components(G1))