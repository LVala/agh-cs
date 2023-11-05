from queue import Queue

# bfs na reprezentacji przez listę sąsiedztwa
# O(V + E)
# dla grafu spójnego (1 wywołanie)
# de facto nic nie robi
def BFS(G, s):
    Q = Queue()
    visited = [False]*len(G)
    
    visited[s] = True
    Q.put(s)

    while Q.empty() == False:
        u = Q.get()
        for v in G[u]:
            if visited[v] == False:
                visited[v] = True
                Q.put(v)

# dfs na reprezentacje przez listę sąsiedztwa
# O(V + E)
# dla dowolnego grafu (może być > 1 wywołanie)
# też nic nie robi
def DFS(G):
    def DFS_visit(G, u):
        nonlocal visited
        visited[u] = True
        for v in G[u]:
            if visited[v] == False:
                DFS_visit(G, v)

    visited = [False]*len(G)
    
    for u in range(len(G)):
        if visited[u] == False:
            DFS_visit(G, u)


# lista sąsiedztwa
def DFS_topologic_sort(G):
    def DFS_visit(G, u):
        nonlocal visited, res
        visited[u] = True
        for v in G[u]:
            if visited[v] == False:
                DFS_visit(G, v)
        res.append(u)

    visited = [False]*len(G)
    res = []
    
    for u in range(len(G)):
        if visited[u] == False:
            DFS_visit(G, u)
    
    res.reverse()
    return res

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


#G1 = [[1],[2],[0,3],[1],[3,7],[4,1],[5],[6],[7,9],[0,10],[2,8]]
#print(connected_components(G1))



# lista sąsiedztwa
def bridges(G):
    def DFS_visit(G, u, parent):
        nonlocal visit_time, time, low, res
        visit_time[u] = time
        low[u] = visit_time[u]
        time += 1
        
        temp = low_child = float('inf')

        for v in G[u]:
            if visit_time[v] == -1:
                child = DFS_visit(G, v, u)
                if child == visit_time[v]: res.append((u,v))
                low_child = min(low_child, child)
            elif v != parent:
                temp = min(temp, low[v])

        low[u] = min(low[u], temp, low_child)

        return low[u]

    time = 0
    n = len(G)
    visit_time = [-1]*n
    low = [-1]*n
    res = []

    for i in range(n):
        if visit_time[i] == -1:
            DFS_visit(G, i, i)
    
    return res

G2 = [
    [1, 2, 3],
    [0, 2],
    [0, 1],
    [0, 4],
    [3]
]

print(bridges(G2))
