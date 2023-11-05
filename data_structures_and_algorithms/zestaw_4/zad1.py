def radix_sort_limited(T):    
    def counting_sort(T, n, exp):
        C = [0] * n
        B = [0] * n
        for i in range(n):
            index = T[i][exp]
            C[index] += 1
        for i in range(1, n):
            C[i] += C[i - 1]
        for i in range(n - 1, -1, -1):
            index = T[i][exp]
            C[index] -= 1
            B[C[index]] = T[i]
        for i in range(n):
            T[i] = B[i]

    n = len(T)

    # w podstawie n liczba będzie zawsze miała max 2 cyfry
    # jeżeli jest < n^2
    for i in  range(n):
        T[i] = [T[i]//n, T[i]%n]

    counting_sort(T, n, 1)
    counting_sort(T, n, 2)

    for i in  range(n):
        T[i] = T[i][0] * n + T[i][1]