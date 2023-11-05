#TIME: O(n*k), SPACE: O(k)
# trochę cheesy implementacja, ale testy przechodzi\
# w poleceniu k << n, więc chyba można założyć że time ~ O(n)
# da się O(n*logk), gdyby użyć np BST, zamiast po prostu tablicy

def longest_incomplete( A, k ):
    n = len(A)
    j = i = 0 #i, j inclusive
    counter = k-1
    F = [[A[0], 1]]
    res = 0
    while i < n:
        if counter > 0:
            res = max(res, i-j+1)
            i += 1
            if i >= n: break
            for ii in range(len(F)):
                if F[ii][0] == A[i]:
                    if F[ii][1] == 0: 
                        F[ii][1] = 1
                        counter -= 1
                        break
                    if F[ii][1] > 0:
                        F[ii][1] += 1
                        break
            else:
                F.append([A[i], 1])
                counter -= 1
        else:
            while counter == 0:
                for ii in range(len(F)):
                    if F[ii][0] == A[j]:
                        if F[ii][1] > 1: 
                            F[ii][1] -= 1
                            break
                        if F[ii][1] == 1:
                            F[ii][1] = 0
                            counter += 1
                            break 
                j += 1
                    
    return res
