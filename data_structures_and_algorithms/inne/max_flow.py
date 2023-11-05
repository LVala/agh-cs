from collections import deque

# wejście w postaci macierzy, O(VE^2) ~O(EV^3) dla macierzy
def edmondskarp(G, s, t):
    def BFS(G, s, t):
        nonlocal parent, n
        Q = deque()
        visited = [False]*n
        
        visited[s] = True
        Q.append(s)

        while len(Q) != 0:
            u = Q.popleft()
            for v in range(n):
                if visited[v] == False and G[u][v] > 0:
                    if v == t:
                        parent[v] = u
                        return True
                    Q.append(v)
                    visited[v] = True
                    parent[v] = u
        return False

    n = len(G)
    parent = [-1]*n
    max_flow = 0

    while BFS(G, s, t):
        path_flow = float("inf")
        u = t
        while u != s:
            path_flow = min(path_flow, G[parent[u]][u])
            u = parent[u]
        
        max_flow += path_flow

        v = t
        while v != s:
            u = parent[v]
            G[u][v] -= path_flow
            G[v][u] += path_flow
            v = parent[v]

    return max_flow

graph = [[0, 16, 13, 0, 0, 0],
        [0, 0, 10, 12, 0, 0],
        [0, 4, 0, 0, 14, 0],
        [0, 0, 9, 0, 0, 20],
        [0, 0, 0, 7, 0, 4],
        [0, 0, 0, 0, 0, 0]]

print(edmondskarp(graph, 0, 5))


# edmonds-karp z kolosa

import copy, collections

def bfs(graph, s, t, parent):
    visited = [False] * len(graph)
    queue = collections.deque()
    queue.append(s)
    visited[s] = True
    while queue:
        u = queue.popleft()
        for ind, val in enumerate(graph[u]):
            if (visited[ind] == False) and (val > 0):
                queue.append(ind)
                visited[ind] = True
                parent[ind] = u
    return visited[t]

def edmonds_karp(graph, source, sink):
    parent = [-1] * len(graph)
    max_flow = 0
    while bfs(graph, source, sink, parent):
        path_flow = float("Inf")
        s = sink
        while s != source:
            path_flow = min(path_flow, graph[parent[s]][s])
            s = parent[s]
        max_flow += path_flow
        v = sink
        while v != source:
            u = parent[v]
            graph[u][v] -= path_flow
            graph[v][u] += path_flow
            v = parent[v]
    return max_flow