#O(nlogn)

def heap_sort(T):
    def heapify(T, n, l):
        largest = l
        left = 2*l + 1
        right = 2*l + 2

        if left < n and T[left] > T[largest]:
            largest = left
        if right < n and T[right] > T[largest]:
            largest = right
        if l != largest:
            T[l], T[largest] = T[largest], T[l]
            heapify(T, n, largest)

    n = len(T)
    
    for i in range(n//2 - 1, -1, -1):
        heapify(T, n, i)
    for i in range(n-1, 0, -1):
        T[i], T[0] = T[0], T[i]
        heapify(T, i, 0)
    
    return T
