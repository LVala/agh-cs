from math import log

#TIME: O(n), SPACE: O(n)

def fast_sort(tab, a):
    def bucket_sort(T):
        def insertion_sort(T):
            for i in range(1, len(T)):
                key = T[i]
                j = i - 1
                while j >=0 and T[j][0] > key[0]:
                    T[j + 1] = T[j]
                    j -= 1
                T[j + 1] = key

        n = len(T)
        buckets = [[] for i in range(n)]
        
        for i in range(n):
            index = int(T[i][0] * n)
            buckets[index].append(T[i])

        for i in range(n):
            insertion_sort(buckets[i])

        k = 0
        for i in range(n):
            for j in range(len(buckets[i])):
                T[k] = buckets[i][j]
                k += 1

    n = len(tab)
    for i in range(n):
        tab[i] = [log(tab[i], a), tab[i]]

    bucket_sort(tab)

    for i in range(n):
        tab[i] = tab[i][1]

    return tab
