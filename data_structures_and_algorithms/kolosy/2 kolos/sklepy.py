from queue import PriorityQueue

class Vertex():
    def __init__(self):
        self.shop = False
        self.distances = []
        self.edges = []
        self.edge = 0
        self.d_store = float("inf")

# oznaczamy sklepy jako odwiedzone wkladamy je do kolejki,
# następnie wywołujemy dijkstrę z użyciem tej kolejki
# nietestowane, więc pewnie nie działa
# bo PriorityQueue wiadomo
# z Bitu dla dróg długości jeden to po prostu BFS byłby ze zliczaniem tras


def distance_to_closest_store(G):
    n = len(G)
    Q = PriorityQueue()

    for i in range(n):
        if G[i].shop:
            G[i].d_store = 0
            Q.put(G[i])

    while Q.empty() == False:
        u = Q.get()
        for v in range(u.edge):
            if u.d_store + u.distances[v] < v.d_store:
                v.d_store = u.d_store + u.distances[v]
                Q.put(G[u.edges[v]])
            
