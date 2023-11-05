# algorytm wykładniczy

def subset_sum_recur(A, T):
    def recur(A, T, i):
        if T == 0: return True
        if T < 0 or i == 0: return False
        return recur(A, T-A[i], i-1) or recur(A, T, i-1)
    
    n = len(A)
    return recur(A, T, n-1)

#algorytm pseudo-wielomianowy (pomysł na podstawie knapsack)

def sumset_sum(A, T):
    n = len(A)
    F = [[0]*(T + 1) for _ in range(n)]
    for w in range(A[0], T + 1):
        F[0][w] = A[0]
    for i in range(1, n):
        for w in range(1, T + 1):
            F[i][w] = F[i-1][w]
            if w >= A[i]:
                F[i][w] = max(F[i][w], F[i-1][w - A[i]] + A[i])
        if F[i][T] == T: return True
    return False


arr = [2,7,3]

print(sumset_sum(arr, 3))