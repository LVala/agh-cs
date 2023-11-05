from math import log2

def bin_search(T, left, right, k):
    mid = (left + right + 1)//2
    if left <= right:
        if T[mid] == k:
            return mid
        if k < T[mid]:
            return bin_search(T, left, mid - 1, k)
        elif k > T[mid]:
            return bin_search(T, mid + 1, right, k)
    else:
        return -1

def insert(T, elem):
    i = len(T) - 2 
    while i >= 0 and (T[i] == None or T[i] > elem):
        T[i + 1] = T[i]
        i -= 1
    T[i + 1] = elem

def logn_sort(T):
    n = len(T)
    B = [99999]*int(log2(n))
    C = [1]*int(log2(n))

    for i in range(n):
        search = bin_search(B, 0, int(log2(n)), T[i])
        if search == -1:
            insert(B, T[i])
        else:
            C[search] += 1

    index = 0
    for j in range(int(log2(n))):
        for _ in range(C[j]):
            T[index] = B[j]
            index += 1        
    
    return T


arr = [1,2,3,4,5,4,3,2,5,1,3,2,4,5,3,2,1,4]
logn_sort(arr)
print(arr)