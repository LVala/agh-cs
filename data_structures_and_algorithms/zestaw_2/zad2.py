def inversion_count(T):
    def merge(T, temp_T, left, mid, right):
        i = left
        j = mid + 1
        k = left
        inv_count = 0

        while i <= mid and j <= right:
            if T[i] <= T[j]:
                temp_T[k] = T[i]
                k += 1
                i += 1
            else:
                temp_T[k] = T[j]
                inv_count += (mid - i + 1)
                k += 1
                j += 1

        while i <= mid:
            temp_T[k] = T[i]
            k += 1
            i += 1
        while j <= right:
            temp_T[k] = T[j]
            k += 1
            j += 1

        for m in range(left, right + 1):
            T[m] = temp_T[m]

        return inv_count

    def mergesort(T, temp_T, left, right):
        inv_count = 0
        
        if left < right:
            mid = (left + right)//2

            inv_count += mergesort(T, temp_T, left, mid)
            inv_count += mergesort(T, temp_T, mid + 1, right)
            inv_count += merge(T, temp_T, left, mid, right)

        return inv_count

    n = len(T)
    temp_arr = [0]*n

    return mergesort(T, temp_arr, 0, n-1)
