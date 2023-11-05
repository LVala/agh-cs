from random import randint, seed


class Node:
    def __init__(self):
        self.next = None
        self.value = None


def qsort( L ):
    def get_tail(head):
        while head != None and head.next != None:
            head = head.next
        return head
     
    def partition(head, end):
        new_head, new_end = None, None

        pivot = end
        prev = None
        cur = head
        tail = pivot

        while(cur != pivot):
            if cur.value < pivot.value:
                if new_head == None:
                    new_head = cur
                prev = cur
                cur = cur.next
            else:
                if prev != None:
                    prev.next = cur.next
                temp = cur.next
                cur.next = None
                tail.next = cur
                tail = cur
                cur = temp
        
        if new_head == None:
            new_head = pivot

        new_end = tail
        
        return pivot, new_head, new_end

    def qsort_recur(head, end):
        if head == None or head == end:
            return head

        pivot, new_head, new_end = partition(head, end)

        if new_head != pivot:
            temp = new_head
            while temp.next != pivot:
                temp = temp.next
            temp.next = None

            new_head = qsort_recur(new_head, temp)
            temp = get_tail(new_head)
            temp.next = pivot

        pivot.next = qsort_recur(pivot.next, new_end)

        return new_head

    L = qsort_recur(L, get_tail(L))

    return L


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




seed(42)

n = 10
T = [ randint(1,10) for i in range(10) ]
B = tab2list( T )

print("przed sortowaniem: B =", end=" ")
printlist(B) 
B = qsort(B)
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
