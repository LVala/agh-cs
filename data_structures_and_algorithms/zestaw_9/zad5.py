# nie moja implementacja, nie wiem czy poprawna
# coś z dijkstrą idk

from queue import PriorityQueue

def dijkstra(G, s):
    def relax(v, u):
        # jesli nieodwiedzony to dodajemy do cost
        if not visited[u]:
            cost[u] = min(cost[v],G[v][i])
            parent[u] = v
            visited[u] = True
            return True
        # jesli juz odwiedzony (czyli cost[u] i cost[v] poprawne) to spr czy moze da sie wiecej pasazerow
        # sprawdzam, czy warto dodać do v krawędź, czy jednak zostać przy u
        if cost[u] < G[v][i]:
            if min(cost[v], G[v][i]) > cost[u]:
                cost[u] = min(cost[v], G[v][i])
                parent[u] = v
        return False

    q = PriorityQueue()
    n = len(G)
    cost = [float('inf')] * n
    visited = [False] * n
    parent = [None] * n

    visited[s] = True
    q.put((cost[s], s))

    while not q.empty():
        c, v = q.get()
        for i in range(n):
            if G[v][i] > 0:
                if relax(v, i):
                    q.put((-cost[i], i))

    print(cost)
    print(parent)

g=[[0,5,6,0,0],
   [5,0,0,8,7],
   [6,0,0,7,0],
   [0,8,7,0,5],
   [0,7,0,5,0]]

dijkstra(g,0)
