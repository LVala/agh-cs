# O(n^2)

def bubble_sort(T):
    for i in range(len(T)):
        for j in range(len(T) - i - 1):
            if T[j] > T[j + 1]:
                T[j], T[j + 1] = T[j + 1], T[j]
    return T
