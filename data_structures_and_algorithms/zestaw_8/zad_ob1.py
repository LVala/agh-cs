# usuwa ostatni wierzchołek przetworzony przez DFS,
# O(V + E)

def rm_verticies(G):
    def DFS_visit(G, u):
        nonlocal visited, res
        visited[u] = True
        for v in G[u]:
            if visited[v] == False:
                DFS_visit(G, v)
        res.append(u)

    visited = [False]*len(G)
    res = []

    DFS_visit(G, 0)

    return res

G1 = [[1,6],[0,2],[1,3,6],[2,4,5],[3,5],[4,3,10],[0,2,7],[6,8],[7,9],[8,10,12],
        [9,11,5],[10,12],[11,9]]

print(rm_verticies(G1))