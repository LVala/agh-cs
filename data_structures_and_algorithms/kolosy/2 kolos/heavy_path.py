class Node:
    def __init__( self ):
        self.children = 0 #liczba dzieci węzła
        self.child = []   #lista par (dziecko, waga krawędzi)
        self.f = None
        self.g = None

# rozwiązanie dynamiczne
# f(v) - długość najdłuższej ścieżki przechodzącej przez węzeł 
# i zawierajacej tylko jego dzieci
# g(v) - długość najdłuższej scieżki zaczynającej sie na 
# węźle i przechodzącej do jego dzieci
# f(v) = suma 2 największych g(u) i ich odległości dist(v,u), gdzie u - dziecko v
# g(v) = max ( g(u) + dist(v,u)), gdzie u - dziecko v
# f(v0) = 0
# g(v0) = 0
# wynik max(f(u)), gdzie u - wszytkie węzły drzewa T

def heavy_path(T):
    def g(v):
        if v.children == 0: v.g = 0
        if v.g != None: return v.g
        res = (-1)* float("inf")
        for i in range(v.children):
            res = max(res, g(v.child[i][0]) + v.child[i][1])
        v.g = res
        return v.g

    def f(v):
        if v.children == 0: v.f = 0
        if v.f != None: return v.f
        temp = None
        res1 = 0
        res2 = 0
        for i in range(v.children):
            if  g(v.child[i][0]) + v.child[i][1] > res1:
                temp = i
                res1 = g(v.child[i][0]) + v.child[i][1]
        for i in range(v.children):
            if  g(v.child[i][0]) + v.child[i][1] > res2 and i != temp:
                res2 = g(v.child[i][0]) + v.child[i][1]

        v.f = res1 + res2
        return v.f
        
    def get_res(v):
        nonlocal res
        res = max(res, f(v))
        for i in range(v.children):
            get_res(v.child[i][0])

    res = 0
    get_res(T)
    return res


A = Node()
B = Node()
C = Node()
D = Node()
A.children = 2
B.children = 1
B.child = [(D,5)]
A.child = [ (B,-1), (C,3) ]

print(heavy_path(A))