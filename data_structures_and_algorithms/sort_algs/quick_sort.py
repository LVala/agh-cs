#O(nlogn)

def quick_sort(T):
    def partition(T, p, r):
        x = T[r]
        i = p
        for j in range(p, r + 1):
            if T[j] <= x:
                T[i], T[j] = T[j], T[i]
                i += 1
        return i - 1
    
    def quicksort(T, p, r):
        if p < r:
            q = partition(T, p, r)
            quicksort(T, p, q - 1)
            quicksort(T, q + 1, r)
    
    quicksort(T, 0, len(T) - 1)

    return T


#quicksort with O(logn) space complexity

def quicksort_space(T):
    def partiton(T, left, right):
        pivot = T[right]
        j = left
        for i in range(left, right + 1):
            if T[i] <= pivot:
                T[i], T[j] = T[j], T[i]
                j += 1
        return j - 1

    def qs_recur(T, left, right):
        while left < right:
            mid = partiton(T, left, right)

            if (mid - left) < (right - mid):
                qs_recur(T, left, mid - 1)
                left = mid + 1
            else:
                qs_recur(T, mid + 1, right)
                right = mid - 1

    qs_recur(T, 0, len(T) - 1)


def qs_3way(T):
    def partition(T, left, right):
        i = left
        j = right
        p = left
        q = right - 1
        pivot = T[right]

        while True:
            while T[i] < pivot:
                i += 1
            while T[j] >= pivot:
                j -= 1
                if T[j] == pivot:
                    break
            if i >= j:
                break
            T[i], T[j] = T[j], T[i]
            if T[i] == pivot:
                T[p], T[i] = T[i], T[p]
                p += 1
            if T[j] == pivot:
                T[q], T[j] = T[j], T[q]
                q -= 1
        T[i], T[right] = T[right], T[i]
        j = i - 1
        for k in range(left, p):
            if j >= 0:
                T[k], T[j] = T[j], T[k]
                j -= 1
        i = i + 1
        for k in range(right - 1, q, -1):
            if i >= 0: 
                T[i], T[k] = T[k], T[i]
                i += 1
        return i, j
    
    def qs_recur(T, left, right):
        if left < right:
            i, j = partition(T, left, right)
            print(T)
            print(left, j, "=====", i, right)
            qs_recur(T, left, j)
            qs_recur(T, i, right)
    
    qs_recur(T, 0, len(T) - 1)
