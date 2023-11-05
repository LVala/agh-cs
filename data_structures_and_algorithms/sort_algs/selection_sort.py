#O(n^2)

class Node():
    def __init__(self, val):
        self.val = val
        self.next = None

def selection_sort(T):
    for i in range(len(T)):
        min_val = i
        for j in range(i + 1, len(T)):
            if T[j] < T[min_val]:
                min_val = j
        T[min_val], T[i] = T[i], T[min_val]
    return T

def selection_sort_ll(head):      #DATA SWAP
    first = head 
    while head != None: 
        min_val = head 
        r = head.next
        while r != None: 
            if (min_val.val > r.val): 
                min_val = r 
            r = r.next
        head.val, min_val.val = min_val.val, head.val
        head = head.next
    return first
