def is_prettier(a, b):
    tab_a = [0]*10
    tab_b = [0]*10
    j_a, w_a, j_b, w_b = 0, 0, 0, 0
    
    while a > 0:
        r = a % 10
        if tab_a[r] == 0:
            tab_a[r] += 1
            j_a += 1
        elif tab_a[r] == 1:
            tab_a[r] += 1
            j_a -= 1
            w_a += 1
        a //= 10
    while b > 0:
        r = b % 10
        if tab_b[r] == 0:
            tab_b[r] += 1
            j_b += 1
        elif tab_b[r] == 1:
            tab_b[r] += 1
            j_b -= 1
            w_b += 1
        b //= 10

    if j_a > j_b: return True
    if j_a == j_b and w_a <= w_b: return True
    return False

#de facto quicksort
def pretty_sort(T):
    def partition(T, left, right):
        pivot = T[right]
        j = left
        for i in range(left, right + 1):
            if is_prettier(T[i], pivot):
                T[i], T[j] = T[j], T[i]
                j += 1
        return j - 1
    
    def qs_recur(T, left, right):
        if left < right:
            mid = partition(T, left, right)
            qs_recur(T, left, mid - 1)
            qs_recur(T, mid + 1, right)
    
    qs_recur(T, 0, len(T) - 1)
