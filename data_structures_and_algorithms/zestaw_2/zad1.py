class Node:
    def __init__(self):
        self.next = None
        self.value = None

def tab2list(A):
    H = Node()
    C = H
    for i in range(len(A)):
        X = Node()
        X.value = A[i]
        C.next = X
        C = X
    return H.next

def printlist(L):
    while L != None:
        print(L.value, "->", end=" ")
        L = L.next
    print("|")

def merge(L1, L2):
    head = Node()
    tail = head

    while L1 != None and L2 != None:
        if L1.value <= L2.value:
            tail.next = L1
            L1 = L1.next
        else:
            tail.next = L2
            L2 = L2.next
        
        tail = tail.next

    if L1 is None: tail.next = L2
    if L2 is None: tail.next = L1
    while tail.next != None: tail = tail.next

    return head.next, tail

def cutlist(L):
    if L == None:
        return L
    
    while L.next != None and L.value <= L.next.value:
        L = L.next
    
    T = L.next
    L.next = None
    return T

def mergesort(L):
    head = L
    if head == None: return None

    while True:
        L = head
        tail = None
        first_iteration = True
        while L != None:
            F1 = cutlist(L)
            if F1 == None and first_iteration == True:
                return head
            F2 = cutlist(F1)
            L, t = merge(L, F1)
            if first_iteration == True:
                head = L
                first_iteration = False
            if tail != None: tail.next = L
            tail = t
            L = F2

def mergesort_v2(L):
    while True:
        NH = None
        NT = None
        while True:

            if L == None:
                L = NH
                break

            A = L
            L = cutlist(L)

            if NT == None and L == None:
                return A
            
            if L == None:
                NT.next = A
                L = NH
                break

            B = L
            L = cutlist(L)

            X, T = merge(A, B)

            if NH == None:
                NH = X
            else:
                NT.next = X
            NT = T



tab = [1,6,4,3,8,7,2,5]
tab1 = tab2list(tab)
printlist(tab1)
R = mergesort(tab1)
printlist(R)
