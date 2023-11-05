def quicksort(T, T2, x):
    def partition(T, left, right):
        pivot = T[right][x]
        j = left
        for i in range(left, right + 1):
            if T[i][x] <= pivot:
                T[i], T[j] = T[j], T[i]
                if T2 != None:
                    T2[i], T2[j] = T2[j], T2[i]
                j += 1
        return j - 1

    def qs_recur(T, left, right):
        if left < right:
            mid = partition(T, left, right)
            qs_recur(T, left, mid - 1)
            qs_recur(T, mid + 1, right)
    
    qs_recur(T, 0, len(T) - 1)

#sortowanie O(nlogn) przegladenie O(n), ale pewnie brzydka stała
def main(A):
    n = len(A)
    
    quicksort(A, None, 0)
    T = [[0,0] for i in range(n)]
    T[0][0] = 0
    temp = 1
    for i in range(1, n):
        if A[i][0] == A[i-1][0]:
            T[i][0] += T[i-1][0]
            temp += 1
        else:
            T[i][0] += (T[i-1][0] + temp)
            temp = 1
    
    quicksort(A, T, 1)

    T[0][1] = 1
    temp = 0
    for i in range(1, n):
        if A[i][1] == A[temp][1]:
            T[temp][1] += 1
        else:
            T[i][1] += T[temp][1]
            temp = i
            T[i][1] += 1

    temp = 0
    for i in range(1, n):
        if A[i][1] == A[temp][1]:
            T[i][1] = T[temp][1]
        else:
            temp = i

    res = T[0][1] - T[0][0]
    res_index = 0
    for i in range(n):
        if T[i][1] - T[i][0] > res:
            res = T[i][1] - T[i][0]
            res_index = i

    return A[res_index]

arr = [[3,7],[2,5],[3,7],[2,6],[2,7],[3,5]]
rese = main(arr)
print(rese)

