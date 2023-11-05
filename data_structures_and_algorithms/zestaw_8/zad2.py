# O(n^2)
# można inteligentniej lecieć DFSem i gdy znajdzie sie wierzchołek bez
# wychodzących krawędzi sprawdzić w O(n), czy wszsytkie wierzchołki mają do niego krawędź
# złożoność ta sama

def ujscia_n2(G):
    n = len(G)
    for i in range(n):
        for j in range(n):
            if G[i][j] != 0:
                break
        else:
            for k in range(n):
                if G[k][j] != 1 and k != j:
                    break
            else:
                return j
    return -1


#O(n)

def ujscia_n(G):
    def is_sink(G, i, n):
        for k in range(n):
            if G[k][i] == 0 and k != i:
                return False
            if G[i][k] == 1:
                return False
        return True
    
    n = len(G)
    i = 0
    j = 0
    while i < n and j < n:
        if G[i][j] == 1:
            i += 1
        else:
            j += 1

    if i >= n:
        return -1
    elif is_sink(i) == False:
        return -1
    else:
        return i

    