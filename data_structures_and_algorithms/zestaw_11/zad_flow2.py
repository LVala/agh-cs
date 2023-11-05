from collections import deque

# wejście w postaci macierzy, O(VE^2) ~O(EV^3) dla macierzy
def min_cut(G, s, t):
    def BFS(G, s, t):
        nonlocal parent, n
        Q = deque()
        visited = [False]*n
        
        visited[s] = True
        Q.append(s)

        while len(Q) != 0:
            u = Q.popleft()
            for v in range(n):
                if visited[v] == False and G[u][v] > 0:
                    if v == t:
                        parent[v] = u
                        return True
                    Q.append(v)
                    visited[v] = True
                    parent[v] = u
        return False

    def DFS(G, s):
        def DFS_visit(G, u):
            nonlocal visited, n
            visited[u] = True
            for v in range(n):
                if visited[v] == False and G[u][v] > 0:
                    DFS_visit(G, v)

        visited = [False]*len(G)

        DFS_visit(G, s)
        return visited

    n = len(G)
    R = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            R[i][j] = G[i][j]
    
    parent = [-1]*n
    max_flow = 0

    while BFS(R, s, t):
        path_flow = float("inf")
        u = t
        while u != s:
            path_flow = min(path_flow, R[parent[u]][u])
            u = parent[u]
        
        max_flow += path_flow

        v = t
        while v != s:
            u = parent[v]
            R[u][v] -= path_flow
            R[v][u] += path_flow
            v = parent[v]

    res = 0
    visited = DFS(R, s)

    for u in range(n):
        for v in range(n):
            if G[u][v] > 0 and R[u][v] == 0 and visited[u]: res += 1
    
    return res

graph = [[0, 16, 13, 0, 0, 0], 
        [0, 0, 10, 12, 0, 0], 
        [0, 4, 0, 0, 14, 0], 
        [0, 0, 9, 0, 0, 20], 
        [0, 0, 0, 7, 0, 4], 
        [0, 0, 0, 0, 0, 0]] 

print(min_cut(graph, 0, 5))