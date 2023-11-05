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

# pesymistyczne O(n^2)
def suma_dwoch(A):
    n = len(A)
    quick_sort(A)
    for x in range(n):
        i = 0
        j = n - 1
        flag = False
        while i < j:
            if A[i] + A[j] == A[x]:
                flag = True
                break
            elif A[i] + A[j] < A[x]:
                i += 1
            else:
                j -= 1
            if i == x: i += 1
            if j == x: j -= 1
        
        if flag == False: return (x,False)
    return True


arr = [20,8,7,5,4,4,3,2,2,1,0,-2,-3,-3,-5]
print(suma_dwoch(arr))