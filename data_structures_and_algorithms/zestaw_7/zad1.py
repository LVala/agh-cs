# przechodznimy po posortowanych punktach
# jeżeli punkt nie jest w poprzednim przedziale,
# to dodajemy przedział o początku w tym punkcie

def przedziały(A):
    res = 1
    temp = A[0]
    for i in range(len(A)):
        if A[i] <= temp + 1:
            continue
        else:
            res += 1
            temp = A[i]

    return res


A1 = [0.7,1.2,1.9,3.1,4.1,5.0]

print(przedziały(A1))