from random import randint

class Node():
    def __init__(self):
        self.next = None
        self.value = None


def get_tail(head):
    while head != None and head.next != None:
        head = head.next
    return head


def partition(head, end):
    pivot = end
    head1, head2 = Node(), Node()
    tail1, tail2, tail3 = head1, head2, pivot

    while head != pivot:
        if head.value < pivot.value:
            tail1.next = head
            tail1 = head
            head = head.next
            tail1.next = None
        elif head.value == pivot.value:
            tail3.next = head
            tail3 = head
            head = head.next
            tail3.next = None
        else:
            tail2.next = head
            tail2 = head
            head = head.next
            tail2.next = None
   
    tail1.next = pivot
    tail3.next = head2.next

    return pivot, tail3, head1.next, tail2


def qsll(head, end):
    if head == None or head == end:
        return head

    pivot, pivot_tail, head1, tail2 = partition(head, end)

    if head1 != pivot:
        temp = head1
        while temp.next != pivot:
            temp = temp.next
        temp.next = None

        head1 = qsll(head1, temp)
        tail1 = get_tail(head1)
        tail1.next = pivot

    pivot_tail.next = qsll(pivot_tail.next, tail2)

    return head1


def quickersortll(head):
    head = qsll(head, get_tail(head))
    return head


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


n = 10
T = [ randint(1,10) for i in range(10) ]
B = tab2list( T )

print("przed sortowaniem: B =", end=" ")
printlist(B) 
B = quickersortll(B)
print("po sortowaniu    : B =", end=" ")
printlist(B)

if B == None:
    print("List jest pusta, a nie powinna!")
    exit(0)

P = B
while P.next != None:
    if P.value > P.next.value:
        print("Błąd sortowania")
        exit(0)
    P = P.next
    
print("OK")