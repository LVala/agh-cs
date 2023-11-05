#LIS z wykorzystaniem zad3

# można by szukać LCS z ciągów
# 1,2,3,4,5,...,max(A)
# oraz A



# LIS O(nlogn)

def bin_search(A, l, r, key):
    while (r - l > 1):
        m = l + (r - l)//2
        if (A[m] >= key):
            r = m
        else:
            l = m
    return r

def LIS(A):
    n = len(A)
    if n == 0: return False
    if n == 1: return A[0]
    
    B = [0]*(n+1)
    B[0] = A[0]
    lis_len = 1

    for i in range(1, n):
        if A[i] < B[0]:
            B[0] = A[i]
        elif A[i] > B[lis_len-1]:
            B[lis_len] = A[i]
            lis_len += 1
        else:
            index = bin_search(B, -1, lis_len - 1, A[i])
            B[index] = A[i]
    return lis_len