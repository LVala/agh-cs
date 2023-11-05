def zadanie2(A):
    n = len(A)
    F = [1] * n
    for i in range(1,n):
        for j in range(i):
            if A[j][1] >= A[i][1] and A[j][0] <= A[i][0]:
                F[i] = max(F[j] + 1,F[i])
    return n - max(F)


A = [[1,100],[1,10],[1,20],[5,10],[1,2],[6,9],[1,50]]
res = zadanie2(A)
print(res)