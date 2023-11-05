from random import shuffle, seed

def linearselect( A, k ):
    # zwyczajny selection sort dla przedzialu tablicy
    def selection_sort(A, left, right):
        for i in range(left, right + 1):
            min_val = i
            for j in range(i + 1, right + 1):
                if A[j] < A[min_val]:
                    min_val = j
            A[min_val], A[i] = A[i], A[min_val]

    # zwraca indeks mediany przedzialu
    # w przypadku parzystej ilosci elementow
    # zwraca wiekszy z dwoch
    def find_median(A, left, right):
        selection_sort(A, left, right)
        return ((left + right + 1)//2)

    # zwyczajny partition z pivotem jako argument
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

    # mediany zapisywane sa na poczatku przedzialu
    # dlatego nie zuzywa dodatkowej pamieci
    # pomimo to zadne elementy sie nie gubia
    def select(A, left, right, k):
        n = right - left + 1
        i = 0

        while i < n//5:
            index = find_median(A, left + 5*i, left + 5*i + 4)
            A[left + i], A[index] = A[index], A[left + i]
            i += 1
        if i*5 < n:
            index = find_median(A, left + 5*i, right)
            A[left + i], A[index] = A[index], A[left + i]
            i += 1

        if i == 1:
            med_of_med = A[left]
        else:
            med_of_med = select(A, left, left + i - 1, (2*left + i)//2)

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

m = 10
for x in range(m):
    B = list(range(m))
    shuffle(B)
    print(B)
    x = linearselect( B, x )
    if x != x:
        print("Blad podczas wyszukiwania liczby", x)
        exit(0)
    
print("OK")
