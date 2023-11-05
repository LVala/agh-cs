from queue import PriorityQueue

# input w postaci listy sądziedzwta G[u] = [(v,w),...]
def shortest_decreasing_path(G, s, t):
    def find_sol(parent, u):
        nonlocal res, s
        if u == s: 
            res.append(u)
            return
        find_sol(parent, parent[u])
        res.append(u)

    n = len(G)
    pos = [0]*n
    parent = [-1]*n
    res = []
    res_dist = 0
    Q = PriorityQueue()

    for i in G:
        i.sort(key=lambda x: x[1])
    
    Q.put((0, s, float("inf")))

    while not Q.empty():
        dist, v, last = Q.get()
        if v == t and dist < res_dist:
            find_sol(parent, t)
            res_dist = dist
        i = pos[v]
        while i < len(G[v]) and G[v][i][1] < last:
            parent[G[v][i][0]] = v
            Q.put((dist + G[v][i][1], G[v][i][0], G[v][i][1]))
            i += 1
        pos[v] = i

    return res_dist, res

G1 = [[(1,6),(2,7),(3,5)],
[(0,6),(3,4),(4,20),(7,6)],
[(0,7),(3,6),(5,3)],
[(0,5),(2,6),(1,4),(4,5)],
[(3,5),(1,20),(7,1)],
[(2,3),(6,4)],
[(5,4),(7,1)],
[(6,1),(4,1),(1,6)]]

print(shortest_decreasing_path(G1, 0, 7))
