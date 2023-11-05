def heapsort_min(T, n, end):
    def heapify(T, n, l):
        smallest = l
        left = 2*l + 1
        right = 2*l + 2

        if left < n and T[left] < T[smallest]:
            smallest = left
        if right < n and T[right] < T[smallest]:
            smallest = right
        if l != smallest:
            T[l], T[smallest] = T[smallest], T[l]
            heapify(T, n, smallest)
   
    for i in range(n//2 - 1, -1, -1):
        heapify(T, n, i)
    for i in range(n-1, end - 1, -1):
        T[i], T[0] = T[0], T[i]
        heapify(T, i, 0)

def heapsort_max(T, n, end):
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

    for i in range(n//2 - 1, -1, -1):
        heapify(T, n, i)
    for i in range(n-1, end - 1, -1):
        T[i], T[0] = T[0], T[i]
        heapify(T, i, 0)

def section(T, p, q):
    n = len(T)

    if p < n-q:
        heapsort_min(T, n, n - q - 1)
        print(T)
        tab = [0]*(q - p + 1)
        for i in range(q- p + 1):
            tab[i] = T[n - p - 1 - i]
        return tab
    else:
        heapsort_max(T, n, p)
        tab = [0]*(q - p + 1)
        for i in range(q - p + 1):
            tab[i] = T[p + i]
        return tab
