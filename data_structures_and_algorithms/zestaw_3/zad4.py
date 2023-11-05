class Node():
    def __init__(self):
        self.value = None
        self.next = None

def tab2list( A ):
    H = Node()
    C = H
    for i in range(len(A)):
        X = Node()
        X.value = A[i]
        C.next = X
        C = X
    return H.next

def printlist( L ):
    while L != None:
        print( L.value, "->", end=" ")
        L = L.next
    print("|")

def merge(a, b):
    first = Node()
    tail = first
    
    while a != None and b != None:
        if a.value <= b.value:
            tail.next = a
            tail = a
            a = a.next
        else:
            tail.next = b
            tail = b
            b = b.next
    
    if b != None: tail.next = b
    if a != None: tail.next = a
    return first.next

def merge_lists(T):
    while True:
        i = 0
        while i < len(T):
            if T[i] == 0:
                i += 1
            else:
                for j in range(i + 1, len(T)):
                    if T[j] != 0:
                        T[i] = merge(T[i], T[j])
                        T[j] = 0
                        i = j + 1
                        break
                else:
                    if i == 0:
                        return T[0]
                    else:
                        i += 1
