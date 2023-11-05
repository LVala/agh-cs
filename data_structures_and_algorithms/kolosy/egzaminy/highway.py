#TIME: O(E^2logE), SPACE:O(E)

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

def kruskal(G, V, i):
    res = []
    vert = []

    G.sort(key=lambda x: x[2])
    
    for j in range(V):
        vert.append(Node(j))

    count = 0
    while count < V - 1 and i < len(G):
        u, v, w = G[i]
        i += 1

        if union(vert[v], vert[u]):
            res.append((u, v, w))
            count += 1

    if count < V-1: return float("inf")
    if res[0][2] > int(res[0][2]): a = int(res[0][2]) + 1
    else: a = res[0][2]
    if res[len(res)-1][2] > int(res[len(res)-1][2]): b = int(res[len(res)-1][2]) + 1
    else: b = res[len(res)-1][2]

    return abs(b-a)

def dist(A, i, j):
        return ((A[i][0]-A[j][0])**2 + (A[i][1]-A[j][1])**2)**(1/2)

def highway(A):
    n = len(A)
    T = []
    for i in range(n):
        for j in range(i+1, n):
            T.append((i, j, dist(A, i, j)))
    
    res = float("inf")
    for i in range(len(T)):
        res = min(res, kruskal(T, n, i))

    return res
