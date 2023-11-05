def kolo_bucket(T, k):
    def insertion_sort(T):
        for i in range(1, len(T)):
            key = T[i]
            j = i - 1
            while j >=0 and T[i] > key:
                T[j + 1] = T[j]
                j -= 1
            T[j + 1] = key
    
    def pos(T, n, k, i):
        res = int((T[i][0]**2 + T[i][1]**2)/(k**2/n))
        return res
    
    n = len(T)
    buckets = [[]]*n
    
    for i in range(n):
        index = pos(T, n, k, i)
        buckets[index].append(T[i])
    
    for i in range(n):
        insertion_sort(buckets[i])
    
    k = 0
    for i in range(n):
        for j in range(len(buckets[i])):
            T[k] = buckets[i][j]
            k += 1