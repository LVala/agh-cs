#from math import *

#C = [["Wrocław", 0, 2], ["Warszawa",4,3], ["Gdańsk", 2,4], ["Kraków",3,1]]
C = [['s', 9, 24], ['e', 11, 2], ['y', -5, 26], ['a', 28, -17], ['i', 23, 11], ['W', -24, -24], ['h', 29, 24],
     ['*', -25, 27], ['U', 22, -16], ['b', 5, 2], ['j', 15, -25], ['s', 24, -10], ['i', -9, 9], ['k', 18, 4],
     ['e', -19, 10], ['t', 16, -3], ['W', 30, 10], ['c', 26, 11], ['s', -20, -17], ['z', -17, 27]]


def bitonicTSP(A):
    # funkcja dist zwraca dystans pomiędzy miastami
    # o indexach i oraz j
    # O(1)
    def dist(A, i, j):
        return ((A[i][1] - A[j][1])**2 + (A[i][2] - A[j][2])**2)**(1/2)
    
    # funkcja tspf, taka sama jak podana na wykładzie
    # zmodyfikowana do operacji na tablicach o strukturze tablicy C
    # działa w czasie O(n^2)
    def tspf(A, F, i, j):
        if F[i][j] != -1:
            return F[i][j]
        if i == j-1:
            best = float('inf')
            for k in range(j-1):
                best = min(best, tspf(A, F, k, j-1) + dist(A, k, j))
            F[j-1][j] = best
        else:
            F[i][j] = tspf(A, F, i, j-1) + dist(A, j-1, j)
        
        return F[i][j]

    # funkcja get_solution rekurencyjnie odwzorowywuje akcje wykonane przez tspf
    # dla najkorzystniejszego przypadku po drodze zapisując w 
    # tablicy R, które miasta będą należej do "dolnej"
    # (lub górnej w zależności od interpretacji) ścieżki
    # wykorzystuje ona właściwość, że na początku indexami 
    # miast "dolnej" ścieżki są argumenty j, natomiast gdy wystąpi
    # przypadek i = j-1, wówczas indexami tej ścieżki stają się
    # argumenty i (argumenty funkcji jakby zamieniają się miejscami)
    # działa w czasie O(n^2)
    def get_solution(A, F, R, i, j, flag=True):
        if (i, j) == (0, 1): return
        
        if flag == True: R[j] = 1
        else: R[i] = 1
        
        if i == j-1:
            flag = not flag
            best = float('inf')
            best_k = 0
            for k in range(j-1):
                if F[k][j-1] + dist(A, k, j)< best and F[k][j-1] != -1:
                    best = F[k][j-1] + dist(A, k, j)
                    best_k = k
            get_solution(A, F, R, best_k, j-1, flag)
        else:
            get_solution(A, F, R, i, j-1, flag)

    # funkcja print solution wypisuje miasta "dolnej" (lub górnej)
    # scieżki (czyli takie, które w tablicy R mają wartość 1)
    # następnie iterując od końca wypisuje resztę miast (czyli te
    # należace do przeciwnej ścieżki)
    # czas O(n^2)
    def print_solution(A, R, n):
        for i in range(n):
            if R[i] == 1: print(f"{A[i][0]}, ", end="")
        for i in range(n-1, -1, -1):
            if R[i] == 0: print(f"{A[i][0]}, ", end="")
        print(A[0][0])


    # sortowanie wbudowane O(nlogn)
    A.sort(key=lambda x: x[1])
    n = len(A)
    F = [[-1]*n for _ in range(n)]
    F[0][1] = dist(A,0,1)
    R = [0]*n
    R[0] = 1
    r_ind = None

    res = float('inf')
    for i in range(n-1):
        temp = tspf(A, F, i, n-1) + dist(A, i, n-1)
        if temp < res:
            res = temp
            r_ind = i


    get_solution(A, F, R, r_ind, n-1)

    print(res)
    print_solution(A, R, n)

bitonicTSP(C)
