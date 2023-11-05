from copy import deepcopy

# funkcja min_cycle iteruje po wszystkich krawędziach grafu
# dla każdej krawędzi usuwa ją i przy pomocy algorytmu Dijkstry
# szuka najkrótszej ścieżki z jednego do drugiego wierzchołka
# usuniętej krawędzi, jeżeli ją znajdzie, to tworzy ona wraz z usuniętą krawędzią
# cykl o długości ścieżki + długość usuniętej krawędzi
# wykonuje tą operację dla każdej krawędzi i szuka miniumum
# TIME: sprawdzenie każdej krawędzi grafu O(E), czyli O(V^2) dla postaci macierzowej
# algorytm dijkstry O(V^2) dla postaci macierzowej
# całkowita złożoność O(V^4)
# SPACE: tablica dystansów O(n), tablica z wynikiem O(n), tablica 
# visited O(n), tablica rodziców O(n), łącznie O(n)
def min_cycle( G ):
    # funkcja znajdująca potencjalne rozwiązanie 
    # na podstawie tablicy rodziców parent
    def find_sol(parent, res, u):
        if parent[u] == -1: 
            res.append(u)
            return
        find_sol(parent, res, parent[u])
        res.append(u)
    
    # typowy algorytm dijkstry dla postaci macierzowej
    def dijkstra(G, s ,t):
        n = len(G)
        dist = [float("inf")]*n
        visited = [False]*n
        dist[s] = 0
        parent = [-1]*n

        for _ in range(n):
            # szukanie wierzchołka o minimalnym dystansie
            # nie ma potrzeby tworzenia kopca, czy kolejki priorytetowej,
            # ponieważ wówczas złożoność algorytmu wynosiłaby
            # ilość wierzchołków * ilość krawędzi * dołączenie wierzchołka do kolejki priorytetowej
            # czyli O(V^2*logV)
            # versus ilość wierzchołków * (wyciągnięcie wierzchołka o najmniejszym dystansie + ilość krawędzi),
            # czyli O(V^2) < O(V^2*logV)
            val_u = float("inf")
            u = -1
            for v in range(n):
                if visited[v] == False and dist[v] <= val_u:
                    u = v
                    val_u = dist[v]


            visited[u] = True

            for v in range(n):
                if G[u][v] != -1 and visited[v] == False and dist[v] > dist[u] + G[u][v]:
                    dist[v] = dist[u] + G[u][v]
                    parent[v] = u

        #zwraca dystans i tablicę rodziców do odtworzenia cyklu
        return dist[t], parent

    # dla każdej krawędzi usuwa ją, wykonuje algorytm dijkstry,
    # sprawdza czy znaleziony cykle jest mniejszy od obecnego,
    # przywraca krawędź do pierwotnego stanu
    end_res = float("inf")
    end_tab = []
    n = len(G)
    for i in range(n):
        for j in range(i+1, n):
            if G[i][j] != -1:
                weight = G[i][j]
                G[i][j] = -1
                G[j][i] = -1
                w, parent = dijkstra(G, i, j)
                if w + weight < end_res:
                    end_res = w + weight
                    end_tab = []
                    find_sol(parent, end_tab, j)
                G[i][j] = weight
                G[j][i] = weight

    return end_tab
  

### sprawdzenie czy dla grafu G (o ktorym zakladamy, ze ma cykl Eulera
### funkcja zwraca prawidłowy wynik
  
G = [[-1, 2,-1,-1, 1],
     [ 2,-1, 4, 1,-1],
     [-1, 4,-1, 5,-1],
     [-1, 1, 5,-1, 3],
     [ 1,-1,-1, 3,-1]]  
LEN = 7


GG = deepcopy( G )
cycle = min_cycle( GG )

print("Cykl :", cycle)


if cycle == []: 
  print("Błąd (1): Spodziewano się cyklu!")
  exit(0)
  
L = 0
u = cycle[0]
for v in cycle[1:]+[u]:
  if G[u][v] == -1:
    print("Błąd (2): To nie cykl! Brak krawędzi ", (u,v))
    exit(0)
  L += G[u][v]
  u = v

print("Oczekiwana długość :", LEN)
print("Uzyskana długość   :", L)

if L != LEN:
  print("Błąd (3): Niezgodna długość")
else:
  print("OK")
  
