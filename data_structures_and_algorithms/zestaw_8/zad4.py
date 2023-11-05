#wejscie jako macierz wag

def decreasing_path(G, s, t):
    def DFS_visit(G, u):
        nonlocal max_val, t, n
        if u == t:
            return True

        for v in range(n):
            if G[u][v] != 0 and G[u][v] < max_val[u]:
                if G[u][v] > max_val[v]:
                    max_val[v] = G[u][v]
                    if DFS_visit(G, v): return True

    n = len(G)
    max_val = [0]*n
    max_val[s] = float("inf")

    if DFS_visit(G, s): return True
    else: return False
    

G1 = [[0,5,0,3,0,6,0,0,0,0,0],
      [5,0,10,0,0,0,0,0,0,0,0],
      [0,10,0,0,0,0,0,0,0,0,0],
      [3,0,0,0,1,0,0,0,0,0,0],
      [0,0,0,1,0,0,0,0,0,0,0],
      [6,0,0,0,0,0,7,5,0,3,0],
      [0,0,0,0,0,7,0,0,0,0,0],
      [0,0,0,0,0,5,0,0,4,0,0],
      [0,0,0,0,0,0,0,4,0,2,3],
      [0,0,0,0,0,3,0,0,2,0,0],
      [0,0,0,0,0,0,0,0,3,0,0]]

print(decreasing_path(G1, 0, 2))