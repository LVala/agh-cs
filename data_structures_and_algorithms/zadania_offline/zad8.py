from copy import deepcopy

# implementacja algorytmu z wykładu
# na reprezentacji macierzowej
# używając algorytmu DFS przechodzimy przez wierzchołki, jednocześnie
# usuwając krawędzie, przez które przeszliśmy; wierzchołki
# do cyklu wynikowego dodawane są po przetworzeniu przez DFS
# złożoność czasowa algorytmu to O(E), gdzie E to liczba krawędzi
# czyli dla reprezentacji macierzowej ~ O(V^2), V - liczba wierzchołków
# każdego wierzchołka sprawdza V krawędzi; następnie macierz jest
# naprawiana w czasie O(V^2), co daje w sumie O(V^2)
# UWAGA: w poleceniu jest to macierz True, False,
# a w przykładzie macierz 0,1; moja implementacja zrobiona została
# z myślą o 0,1 (co de facto z uwagi na specyfikę Pythona działa zamiennie, bo 1 == True)
def euler( G ):
    # funkcja DFS usuwająca krawędzie
    # (zamieniająca je z 1 na 2 w macierzy)
    # i dodająca wierzchołki po przetworzeniu do res
    def DFS_visit(G, u):
        nonlocal res, n, is_eulerian
        # zliczanie krawędzi, w razie
        # gdyby cykle Eulera nie istniał
        # tj. liczba sąsiadów była nieparzysta
        if is_eulerian == False: return
        count = 0
        for v in range(n):
            if G[u][v] != 0: count += 1
            if G[u][v] == 1:
                G[u][v] = 2
                G[v][u] = 2
                DFS_visit(G, v)
        if count % 2 == 1: is_eulerian = False
        res.append(u)

    is_eulerian = True
    res = []
    n = len(G)

    # szukam wierzchołka, od którego wychodzi krawędź,
    # jeżeli od jakiegoś wierzchołka nie wychdzą krawędzie, 
    # graf nadal może być eulerowski
    # graf bez krawędzi traktuję jako eulerowski i zwracam dowolny wierzchołek
    for i in range(n):
        b = False
        for j in range(i + 1, n):
            if G[i][j] == 1:
                G[i][j] = 2
                G[j][i] = 2
                DFS_visit(G, i)
                b = True
                break
        if b: break
    else: return [0]

    # naprawiana jest macierz, ażeby zachować warunek jej
    # "nie zniszczenia", stąd zamiana jedynek na dwójki w DFS
    # (zakładam że "nie niszczenie" nie zabrania modyfikowania macierzy
    #  ale to, żeby po zakończeniu działania funkcji wróciła do pierwotnej
    # postaci)
    for i in range(n):
        for j in range(i + 1, n):
            # jeżeli jakaś krawędź nie została przetworzona
            # przez DFS, to graf nie jest spójny( z pominięciem pojedynczych wierzchołków bez
            # krawędzi, wtedy nadal może być eulerowski)
            if G[i][j] == 1: return None
            if G[i][j] == 2: 
                G[i][j] = 1
                G[j][i] = 1

    if is_eulerian: return res + [res[0]]
    else: return None


### sprawdzenie czy dla grafu G (o ktorym zakladamy, ze ma cykl Eulera
### funkcja zwraca prawidłowy wynik


G = [[0,1,1,0,0,0],
     [1,0,1,1,0,1],
     [1,1,0,0,1,1],
     [0,1,0,0,0,1],
     [0,0,1,0,0,1],
     [0,1,1,1,1,0]]


GG = deepcopy( G )
cycle = euler( G )

if cycle == None: 
    print("Błąd (1)!")
    exit(0)
  
u = cycle[0]
for v in cycle[1:]:
    if GG[u][v] == False:
        print("Błąd (2)!")
        exit(0)
    GG[u][v] = False
    GG[v][u] = False
    u = v
  
for i in range(len(GG)):
    for j in range(len(GG)):
        if GG[i][j] == True:
            print("Błąd (3)!")
            exit(0)
      
print("OK")