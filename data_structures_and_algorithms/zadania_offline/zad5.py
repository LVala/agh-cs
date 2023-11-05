# Binary search, zwraca index szukanego elementu, a jeżeli
# go nie ma, to index kolejnego większego
# przystosowany do tablicy posortowaniej malejąco

def bin_search(A, l, r, key):
    while (r - l > 1):
        m = l + (r - l)//2
        if A[m] == key:
            return m
        if (A[m] > key):
            l = m
        else:
            r = m
    return r

# Funkcja get_LIS dziala na zasadzie podobnej jak typowa funkcja
# szukająca długości LIS w O(nlogn) (założenia przedstawione tutaj: 
# https://www.geeksforgeeks.org/longest-monotonically-increasing-subsequence-size-n-log-n/)
# jednak, dla wygody wypisywania ciagów w
# kolejności zgodnej z poleceniem zadania, funkcja przeszukuje tablicę
# od końca szukając ciągów malejących (czyli de facto ciagów rosnących
# patrząc od początku tablicy), elementem odróżnijącym ją od funkcji z linku są
# tablice B i P, dzięki którym gromadzone są indexy potencjalnych elementów należących do LIS
# będącymi następcami danego elementu(np.: P=[[2,4], [4], [5], [4], [], []] czyli potencjalnymi
# następcami elementu pod indexem 0 są elementy pod indexami 2 oraz 4)
# funkcja get_LIS zwraca długość LIS, tablicę z następcami i tablicę z elementami startowymi LIS

def get_LIS(A):
    n = len(A)
    if n == 0: return None, None, None
    if n == 1: return 1, [[0]], [0]
    
    B = [0]*(n+1)
    B[0] = A[n-1]
    lis_len = 1
    P = [[] for _ in range(n)]
    F = [[] for _ in range(n+1)]
    F[lis_len].append(n-1)

    for i in range(n-2,-1,-1):
        if A[i] >= B[0]:
            B[0] = A[i]
            F[1].append(i)
        elif A[i] < B[lis_len-1]:
            B[lis_len] = A[i]
            for j in F[lis_len]:
                if A[j] > A[i]:
                    P[i].append(j)
            lis_len += 1
            F[lis_len].append(i)
        else:
            index = bin_search(B, -1, lis_len - 1, A[i])
            B[index] = A[i]
            for j in F[index]:
                if A[j] > A[i]:
                    P[i].append(j)
            F[index + 1].append(i)

    return lis_len, P, F[lis_len]

# funckja printAllLIS przy użyciu danych z funkcji get_LIS rekurencyjnie wypisuje
# wszystkie LIS w kolejności zgodnej z kolejnością w tablicy wejściowej
# (stąd pomysł na szukanie ciagów malejących od końca, w normalnym przypadku 
# wypisywane ciągi byłyby posegregowane po wartościach od końca ciągu)
# dodatkowo printAllLIS zlicza ilość LIS

def printAllLIS(A):
    def recur(A, P, R, lis_len, i, v):
        count = 0
        if v == lis_len-1:
            R[lis_len-1] = A[i]
            for j in range(len(R)):
                print(R[j], end=" ")
            print()
            return 1
        R[v] = A[i]
        for j in range(len(P[i])-1, -1, -1):
            count += recur(A, P, R, lis_len, P[i][j], v+1)
        return count

    lis_len, P, S = get_LIS(A)
    if lis_len == None: return 0
    
    R = [0]*lis_len
    count = 0
    
    for i in range(len(S)-1, -1, -1):
        count += recur(A, P, R, lis_len, S[i], 0)

    return count

arr = [0, 8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15]
printAllLIS(arr)