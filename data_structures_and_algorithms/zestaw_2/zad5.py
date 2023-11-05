def leader(T):
    count = 0
    j = T[0]
    for i in range(len(T)):
        if count == 0:
            count += 1
            j = T[i]
        elif T[i] == j:
            count += 1
        else:
            count -= 1 
    
    if count == 0: return False
    
    count = 0
    for i in range(len(T)):
        if T[i] == j: count += 1
    if count >= len(T)//2 + 1: return True, j
    return False






A = [5,4,2,7,4,4,4]
print(leader(A))