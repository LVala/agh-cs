class Node():
    def __init__(self):
        self.val = None
        self.next = None

def tab2list( A ):
    H = Node()
    C = H
    for i in range(len(A)):
        X = Node()
        X.val = A[i]
        C.next = X
        C = X
    return H.next

def printlist( L ):
    while L != None:
        print( L.val, "->", end=" ")
        L = L.next
    print("|")