# 1 metoda z tworzeniem nowego grafu z 
# dla każdego wierzchołka x dodawanie wszystkich
# krawędzi, krórych wierzchołki są oddalone dokładnie
# o 1 od wierzchołka, jeżeli próbujemy stworzyć istniejącą
# już krawędź, to cykl o długości 4 istnieje
# w grafie można stworzyć max (V/2) = V!/2*(V-2)! = (V-1)V/2
# czyli złożoność O(V^2)
# niestety działa tylko dla grafu nieskierowanego

# 2 metoda z BFS
# wywołujemt BFS dla każdego wierzchołka x i następnie zapisujemy,
# czy dla każdego wierzchołka y istnieje ścieżka długości 2 x -> y,
# jeżeli znajdziemy takie dwa wierzchołki że istnieje ścieżka z
# x -> y i y->x, to oznacza że istnieje cykl długości 4
# n wierzchołków *(BFS dla każdego wierzchołka n^2) = O(n^3)

# wejści w postaci listy sąsiedztwa
def cycle_4(G):
    def BFS(G, s):
        nonlocal neigh
        Q = []

        for v in G[s]:
            Q.append(v)

        for _ in range(len(Q)):
            u = Q.pop()
            for v in G[u]:
                if v != s: neigh[s][v] = u
                if neigh[v][s] != False: return (v,s)

        return False

    neigh = [[False]*len(G) for _ in range(len(G))]

    for i in range(len(G)):
        temp = BFS(G, i)
        if temp != False:
            v,s = temp
            return v, neigh[v][s], s, neigh[s][v]

    return False

G1 = [[1],[2],[0,3,6],[5],[8],[4],[],[6],[3]]
print(cycle_4(G1))