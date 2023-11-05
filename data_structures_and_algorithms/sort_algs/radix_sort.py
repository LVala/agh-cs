#podobny do bucket sort, do sortowania np. słów
# O(d*(n+b))

def radix_sort(T):
    def counting_sort(T, exp):
        n = len(T)
        C = [0] * 10
        B = [0] * n
        for i in range(n):
            index = T[i] // exp
            C[index % 10] += 1
        for i in range(1, 10):
            C[i] += C[i - 1]
        for i in range(n - 1, -1, -1):
            index = T[i] // exp
            C[index % 10] -= 1
            B[C[index % 10]] = T[i]
        for i in range(n):
            T[i] = B[i]
    
    max_num = max(T)
    exp = 1
    while max_num / exp > 0:
        counting_sort(T, exp)
        exp *= 10
