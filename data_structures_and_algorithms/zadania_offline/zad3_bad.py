from random import shuffle, seed

def linearselect( A, k ):
    def selection_sort(A, left, right):
        for i in range(left, right + 1):
            min_val = i
            for j in range(i + 1, right + 1):
                if A[j] < A[min_val]:
                    min_val = j
            A[min_val], A[i] = A[i], A[min_val]
    
    def find_median(A, left, right):
        selection_sort(A, left, right)
        return A[(left + right + 1)//2]

    def partition(A, left, right, pivot):
        for i in range(left, right + 1):
            if A[i] == pivot:
                A[i], A[right] = A[right], A[i]
        i = left
        for j in range(left, right + 1):
            if A[j] <= pivot:
                A[j], A[i] = A[i], A[j]
                i += 1
        return i - 1
    
    def select(A, left, right, k):
        n = right - left + 1
        median = [0]*((n+4)//5)
        i = 0
        while i < n//5:
            median[i] = find_median(A, left + 5*i, left + 5*i + 4)
            i += 1
        if i*5 < n:
            median[i] = find_median(A, left + 5*i, right)
            i += 1

        if i == 1:
            med_of_med = median[0]
        else:
            med_of_med = select(median, 0, i - 1, i//2)

        mid = partition(A, left, right, med_of_med)

        if k < mid:
            return select(A, left, mid - 1, k)
        elif k > mid:
            return select(A, mid + 1, right, k)
        else:
            return A[mid]

    res = select(A, 0, len(A) - 1, k)
    return res


seed(42)

m = 11
for x in range(m):
    B = list(range(m))
    shuffle(B)
    print(B)
    x = linearselect( B, x )
    if x != x:
        print("Blad podczas wyszukiwania liczby", x)
        exit(0)
    
print("OK")
