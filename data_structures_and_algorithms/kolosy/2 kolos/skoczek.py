# rozwiązanie dynamiczne bottom up
# f(i) - max wartość po dojściu na pole i
# f(i) = max (f(i-k)), takie że i.long_j = k lub i.short_j = k
# f(0) = 0.value

# coś takiego, nie testowane
def skoczek(A):
    n = len(A)
    F = [0]*n
    F[0] = A[0][0]
    for i in range(1, n):
        for j in range(i):
            if A[j][1] == i-j or A[j][2] == i-j:
                F[i] = max(F[i], F[j] + A[j][0])
    
    return F[n-1]