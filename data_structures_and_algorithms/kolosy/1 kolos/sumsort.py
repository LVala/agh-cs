def heapify(T, n, l):
    largest = l
    left = 2*l + 1
    right = 2*l + 2

    if left < n and T[left] < T[largest]:
        largest = left
    if right < n and T[right] < T[largest]:
        largest = right
    if l != largest:
        T[l], T[largest] = T[largest], T[l]
        heapify(T, n, largest)


def sumsort(A, B, n):
    n = len(A)
    for i in range(n//2 - 1, -1, -1):
        heapify(A, n, i)
    for i in range(2*n):
        A[i], A[0] =  A[0], A[i]
        B[i] = A[i]
        heapify(A, i, 0)
    for i in range(2*n, n^2):
        B[i] = A[i - 2*n]

# to lepiej chyba quickselectem robić n^2 wychodzi
