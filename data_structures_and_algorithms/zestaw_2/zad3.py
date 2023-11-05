def find_sum(A, x):
    i = 0
    j = len(A) - 1
    while i <= j:
        if A[i] + A[j] == x:
            return True, i, j
        if A[i] + A[j] < x:
            i += 1
        else:
            j -= 1

    return False


T = [2,4,6,8,23,14,18,22]
print(find_sum(T, 8))