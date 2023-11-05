# najmniejsza suma zawsze ze środka

def minimun_sum(T):
    n = len(T)
    T.sort()

    x = T[n // 2]

    suma = 0

    for i in range(n):
        suma += abs(T[i] - x)

    return suma

arr = [1, 3, 9, 3, 6]
print(minimun_sum(arr))