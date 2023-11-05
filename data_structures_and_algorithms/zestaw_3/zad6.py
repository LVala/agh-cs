def heapify_min(heap, n, l):
    largest = l
    left = 2*l + 1
    right = 2*l + 2

    if left < n and heap[left] < heap[largest]:
        largest = left
    if right < n and heap[right] < heap[largest]:
        largest = right
    if l != largest:
        heap[l], heap[largest] = heap[largest], heap[l]
        heapify_min(heap, n, largest)

def heapify_max(heap, n, l):
    largest = l
    left = 2*l + 1
    right = 2*l + 2

    if left < n and heap[left] > heap[largest]:
        largest = left
    if right < n and heap[right] > heap[largest]:
        largest = right
    if l != largest:
        heap[l], heap[largest] = heap[largest], heap[l]
        heapify_max(heap, n, largest)

def heapify_max_bot(T, i):
    parent = (i-1)//2

    if i != 0 and T[parent] < T[i]:
        T[parent], T[i] = T[i], T[parent]
        heapify_max_bot(T, parent)

def heapify_min_bot(T, i):
    parent = (i-1)//2

    if i != 0 and T[parent] > T[i]:
        T[parent], T[i] = T[i], T[parent]
        heapify_min_bot(T, parent)

def remove(heap, n, heap_type):
    heap[0], heap[n - 1] = heap[n - 1], heap[0]
    heap.pop()
    if heap_type == "max":
        heapify_max(heap, len(heap), 0)
    else:
        heapify_min(heap, len(heap), 0)

def insert(heap, heap_type, elem):
    heap.append(elem)
    if heap_type == "max":
        heapify_max_bot(heap, len(heap) - 1)
    else:
        heapify_min_bot(heap, len(heap) - 1)

def rm_median(heap_max, heap_min):
    n_min = len(heap_min)
    n_max = len(heap_max)
    if n_min == n_max:
        median = (heap_max[0] + heap_min[0])/2
        remove(heap_max, n_max, "max")
        remove(heap_min, n_min, "min")
        return median
    elif n_min < n_max:
        median = heap_max[0]
        remove(heap_max, n_max, "max")
        return median
    else:
        median = heap_min[0]
        remove(heap_min, n_min, "min")
        return median

def insert2med(heap_max, heap_min, elem):
    if elem > heap_max[0] and elem < heap_min[0]:
        if len(heap_min) <= len(heap_max):
            insert(heap_min, "min", elem)
        else:
            insert(heap_max, "max", elem)
    elif elem <= heap_max[0]:
        if len(heap_max) <= len(heap_min):
            insert(heap_max, "max", elem)
        else:
            temp = heap_max[0]
            heap_max[0] = elem
            heapify_max(heap_max, len(heap_max), 0)
            insert(heap_min, "min", temp)
    else:
        if len(heap_min) <= len(heap_max):
            insert(heap_min, "min", elem)
        else:
            temp = heap_min[0]
            heap_min[0] = elem
            heapify_min(heap_min, len(heap_min), 0)
            insert(heap_max, "max", temp)


minh = [7, 8, 9, 10]
maxh = [5, 4, 3]
insert2med(maxh, minh, 6)
print(minh)
print(maxh)