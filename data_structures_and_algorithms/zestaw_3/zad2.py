def insert2heap(T, a):
    def heapify(T, i):
        parent = (i-1)//2

        if i != 0 and T[parent] < T[i]:
            T[parent], T[i] = T[i], T[parent]
            heapify(T, parent)

    def extend_and_add(T, a):
        n = len(T)
        temp_T = [0]*(n + 1)
        for i in range(n):
            temp_T[i] = T[i]
        temp_T[n] = a
        return temp_T

    n = len(T)
    new_T = extend_and_add(T, a)
    heapify(new_T, n)
    return new_T