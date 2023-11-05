#dla sortowanie n liczb ze zbioru k-1
#liczb naturalnych O(n + k)

def count_sort(T, k):
    n = len(T)
    C = [0] * k
    B = [0] * n
    for i in range(n):
        C[T[i]] += 1
    for i in range(1, k):
        C[i] += C[i - 1]
    for i in range(n - 1, -1, -1):
        C[T[i]] -= 1
        B[C[T[i]]] = T[i]
    for i in range(n):
        T[i] = B[i]
