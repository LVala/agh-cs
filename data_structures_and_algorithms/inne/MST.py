from queue import PriorityQueue

class Node():
    def __init__(self, val):
        self.val = val
        self.rank = 0
        self.parent = self

def find(x):
    if x != x.parent:
        x.parent = find(x.parent)
    return x.parent

def union(x, y):
    x = find(x)
    y = find(y)
    print()
    if x == y: return False
    if x.rank > y.rank:
        y.parent = x
    else:
        x.parent = y
        if x.rank == y.rank: y.rank += 1
    return True


# input jako lista krawędzi (u, v, waga)
# V - ilość wierzchołków
def kruskal(G, V):
    res = []
    vert = []

    G.sort(key=lambda x: x[2])
    print(G)
    
    for i in range(V):
        vert.append(Node(i))

    i = 0
    count = 0
    while count < V - 1 and i < len(G):
        u, v, w = G[i]
        i += 1

        if union(vert[v], vert[u]):
            res.append((u, v, w))
            count += 1

    return res

G1 = [[0,1,4],[1,2,8],[2,3,7],[3,4,9],[4,5,10],[5,6,2],[6,7,1],[7,0,8],
      [7,1,11],[7,8,7],[2,8,2],[8,6,6],[2,5,4],[3,5,14]]


# input jako lista sąsiedztwa
# nietestowane, może nie działać
def prim(G):
    n = len(G)
    dist = [float("inf")]*n
    dist[0] = 0
    parent = [-1]*n
    res = []
    Q = PriorityQueue()
    
    Q.put((dist[0], 0))

    while not Q.empty():
        dist_u, u = Q.get()
        if dist_u != dist[u]: continue
        for v in range(len(G[u])):
            if dist[u] + G[u][v][1] < dist[G[u][v][0]]:
                dist[G[u][v][0]] = dist[u] + G[u][v][1]
                parent[G[u][v][0]] = u
                Q.put((dist[G[u][v][0]], G[u][v][0]))

    for i in range(n):
        res.append((parent[i], i))
    