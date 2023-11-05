#O(nlogn)

class Node():
    def __init__(self, val):
        self.val = val
        self.next = None

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

def merge_sort_pythonowy(T):
    def merge(L, R):
        res = []
        i = j = 0
        for _ in range(len(L) + len(R)):
            if i < len(L) and (j >= len(R) or L[i] <= R[j]):
                res.append(L[i])
                i += 1
            else:
                res.append(R[j])
                j += 1
        return res

    if len(T) > 1:
        m = len(T)//2
        L = merge_sort_pythonowy(T[0:m])
        R = merge_sort_pythonowy(T[m:])
        T = merge(L, R)
    
    return T

def merge_sort_ll(head):
    def merge(a, b):
        if a == None:
            return b
        if b == None:
            return a
        if a.val <= b.val:
            result = a
            result.next = merge(a.next, b)
        else:
            result = b
            result.next = merge(a, b.next)
        return result
    
    def get_middle(head):
        if head == None:
            return head
        slow = head
        fast = head
        while fast.next != None and fast.next.next != None:
            slow = slow.next
            fast = fast.next.next
        return slow

    if head == None or head.next == None:
        return head
    
    middle = get_middle(head)
    n_middle = middle.next
    middle.next = None
    
    L = merge_sort_ll(head)
    R = merge_sort_ll(n_middle)
    result = merge(L, R)
    
    return result
