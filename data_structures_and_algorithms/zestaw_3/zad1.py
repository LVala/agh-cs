#quicksort with O(logn) space complexity

def guicksort(T):
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