# Funkcja sprawdza czy przedzial [a, b] mozna utworzyc, musi byc dokladnie [a, b]
def check_1(A, a, b):
    n = max(A)[1] + 1
    # Tutaj przechowuje czy dany przedzial D[i][j] mozna stworzyc, i<j
    D = [[None] * (n) for i in range(n)]
    # Przedzialy podane mozliwe
    for x in A:
        D[x[0]][x[1]] = True

    def f(i, j):
        if D[i][j] is not None:
            return True
        for k in range(i + 1, j):
            if f(i, k) and f(k, j):
                D[i][j] = True
                return True
        return False

    return f(a, b)


A1 = [(1, 3), (2, 5), (1, 2), (2, 4), (3, 7), (7, 11)]
#print(check(A1, 3, 11))

#B 
def check_2(A, a, b):
   n = max(A)[1] + 1
   D = [[None] * n for i in range(n)]
   for x in A:
       if D[x[0]][x[1]] is not None:
           D[x[0]][x[1]] = min(D[x[0]][x[1]], x[2])
       else:
           D[x[0]][x[1]] = x[2]

   # Funkcja zwraca minimalny koszt przedzialu [a, b]
   def f(i, j):
       if D[i][j] is not None:
           return D[i][j]
       min_cost = -1
       for k in range(i + 1, j):
           v1, v2 = f(i, k), f(k, j)
           if v1 > 0 and v2 > 0:
               if min_cost < 0 or min_cost > v1 + v2:
                   min_cost = v1 + v2
       D[i][j] = min_cost
       return min_cost

   res = f(a, b)
   # for d in D:
   #     print(d)
   return res


A1 = [(1, 3, 5), (2, 5, 2), (1, 2, 4), (2, 4, 1), (3, 7, 19), (3, 7, 9), (7, 11, 12)]
#print(check(A1, 1, 11))

# C
def check_3(A, K):
   m = min(A)[0]
   n = max(A)[1]
   D = [[None] * (n+1) for i in range(n+1)]
   res = 0
   for x in A:
       D[x[0]][x[1]] = 1
       res = max(x[1]-x[0], res)

   # Zapisuje z ilu odcinków dany fragment
   def f(i, j):
       nonlocal res
       if D[i][j] is not None:
           if D[i][j] < 0: return None
           return D[i][j]
       min_cost = -1
       for k in range(i + 1, j):
           v1, v2 = f(i, k), f(k, j)
           if v1 is not None and v2 is not None:
               # Da sie zrobic taka sciezke
               if min_cost < 0 or min_cost > v1 + v2:
                   min_cost = v1 + v2
       D[i][j] = min_cost
       if min_cost < 0: return None
       if min_cost <= K and res < j - i:
           res = j - i
       return min_cost

   f(m, n)
   return res


A1 = [(1, 3), (2, 5), (1, 2), (2, 4), (3, 7), (7, 11), (4, 10), (10, 14), (14, 20)]
#print(check(A1, 2))