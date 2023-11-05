# tuple array (x1,x2,y1,y2), x1 > x2, y1 > y2

def quicksort(T):           #sorts by y1 in O(nlogn)
    def partition(T, left, right):
        pivot = T[right][2]
        j = left
        for i in range(left, right + 1):
            if T[i][2] <= pivot:
                T[i], T[j] = T[j], T[i]
                j += 1
        return j - 1

    def qs_recur(T, left, right):
        if left < right:
            mid = partition(T, left, right)
            qs_recur(T, left, mid - 1)
            qs_recur(T, mid + 1, right)

    qs_recur(T, 0, len(T) - 1)

def enough_water(T, A, n):      #n = container number in sorted array
    V = 0                       #works in O(n)
  
    for i in range(len(T)):
        if T[i][3] < T[n][2]:
            if T[i][2] <= T[n][2]:
                V += (T[i][0] - T[i][1])*(T[i][2] - T[i][3])
            else:
                V += (T[i][0] - T[i][1])*(T[n][2] - T[i][3])
    
    return (V <= A)

def main(T, A): 

    quicksort(T)

    left = 0
    right = len(T) - 1

    while left < right:             #searching, works in O(logn)

        mid = (left + right + 1)//2

        if enough_water(T, A, mid): left = mid
        else: right = mid - 1

    return right + 1


Tab = [(4,3,8,5),(6,5,9,7),(7,6,8,1),(5,3,3,1),(3,1,2,0),(2,0,6,3)]

print(main(Tab, 100))