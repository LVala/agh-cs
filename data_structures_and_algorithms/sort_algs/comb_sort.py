# O(nlogn), psymistyczna n^2

def comb_sort(T):
    def getnextgap(gap):
        gap //= 13
        if gap < 1:
            return 1
        return gap
    
    gap = len(T)
    swapped = True

    while gap !=1 or swapped == 1:
        gap = getnextgap(gap)
        swapped = False
 
        for i in range(0, len(T) - gap):
            if T[i] > T[i + gap]:
                T[i], T[i + gap] = T[i + gap], T[i]
                swapped = True
    
    return T
