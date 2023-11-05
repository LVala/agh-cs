from random import randint, seed

def mergesort(T):
    def merge(T, p, q, r):
        #lista dzielona na części
        n1 = q - p
        n2 = r - q
        L = [0 for i in range(n1)]
        R = [0 for i in range(n2)]
        for i in range(n1):
            L[i] = T[p + i]
        for i in range(n2):
            R[i] = T[q + i]
        #sortowanie
        i = j = 0
        for k in range(p, p + n1 + n2):
            if i < len(L) and (j >= len(R) or L[i] <= R[j]):
                T[k] = L[i]
                i += 1
            else:
                T[k] = R[j]
                j += 1
        return T

    def mergesort1(T, p, r):
        if p < r - 1:
            q = (p+r)//2
            mergesort1(T, p, q)
            mergesort1(T, q, r)
            merge(T, p, q, r)

    mergesort1(T, 0, len(T))

    return T

seed(42)

n = 10
A = [ randint(1,10) for i in range(10) ]

print("przed sortowaniem: T =", A) 
A = mergesort(A)
print("po sortowaniu    : T =", A)

for x in range(len(A)-1):
    if A[x] > A[x+1]:
        print("Błąd sortowania!")
        exit()
    
print("OK")