#TIME: O(V^2), SPACE: O(V)
    
def tasks(T):
    def DFS_topologic_sort(G):
        def DFS_visit(G, u):
            nonlocal visited, res, n
            visited[u] = True
            for v in range(n):
                if G[u][v] == 1 and visited[v] == False:
                    DFS_visit(G, v)
            res.append(u)

        n = len(G)
        visited = [False]*n
        res = []

        for u in range(n):
            if visited[u] == False:
                DFS_visit(G, u)
        
        res.reverse()
        return res

    res = DFS_topologic_sort(T)

    return res
