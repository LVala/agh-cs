def bin_search(A, B, l, r, key):
    while (r - l > 1):
        m = l + (r - l)//2
        if (A[B[m]] >= key):
            r = m
        else:
            l = m
    return r

def LIS(A):
    n = len(A)
    if n == 0: return False
    if n == 1: return A[0]
    
    P = [-1 for i in range(n + 1)]
    B = [0]*(n+1)
    B[0] = 0
    lis_len = 1

    for i in range(1, n):
        if A[i] < A[B[0]]:
            B[0] = i
        elif A[i] > A[B[lis_len-1]]:
            P[i] = B[lis_len-1]
            B[lis_len] = i
            lis_len += 1
        else:
            index = bin_search(A, B, -1, lis_len - 1, A[i])
            P[i] = B[index-1]
            B[index] = i

    i = B[lis_len-1]
    while(i >= 0):
        print(A[i], " ", end ="")
        i = P[i]
    print()
    return lis_len

arr = [0, 8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15]
print(LIS(arr))