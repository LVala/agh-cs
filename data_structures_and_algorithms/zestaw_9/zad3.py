# nie moja implementacja, nie wiem czy działa
# chyba działa na zasadzie, że sortujemy topologicznie,
# a potem dynamicznie szukamy najkrótszej trasy

def topological_sort(G):  # reprezentacja macierzowa - DAG ważony

    def DFS_visit(G, v):
        nonlocal visited, stack
        visited[v] = True

        for i in range(len(G[v])):
            if G[v][i] != 0 and not visited[i]:
                DFS_visit(G, i)
        stack.append(v)

    visited = [False] * len(G)
    stack = []

    for v in range(len(G)):
        if not visited[v]:
            DFS_visit(G, v)

    return stack


def zad3(G, s):
    stack = topological_sort(G)
    d = [float('inf')] * len(G)
    d[s] = 0
    while stack:
        v = stack.pop()
        for u in range(len(G[v])):
            if G[v][u] != 0:
                d[u] = min(d[u], d[v] + G[v][u])
    return d


G = [
    [0, 5, 3, 10],
    [0, 0, 0, 4],
    [0, 0, 0, 8],
    [0, 0, 0, 0]
    ]


print(zad3(G, 0))