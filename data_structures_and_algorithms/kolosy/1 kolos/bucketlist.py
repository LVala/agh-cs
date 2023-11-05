class Node():
    def __init__(self):
        self.val = None
        self.next = None

def get_tail(head):
    while head != None and head.next != None:
        head = head.next
    return head

def insertion_sort(head):
    def insert(head, new_node):
        if head == None or head.val >= new_node.val:
            new_node.next = head
            return new_node
        first = head
        while head.next != None and head.next.val < new_node.val:
            head = head.next
        new_node.next = head.next
        head.next = new_node
        return first
    
    first = None
    while head != None:
        head_next = head.next
        first = insert(first, head)
        head = head_next

    return first

def sort(head):
    cur = head
    n = 0
    while cur != None:
        n += 1
        cur = cur.next
    
    buckets = [None for i in range(n)]
    b_size = 10/n
    while head != None:
        head_next = head.next
        index = int(head.val/b_size)
        head.next = buckets[index]
        buckets[index] = head
        head = head_next
    
    for i in range(n):
        buckets[i] = insertion_sort(buckets[i])
    
    first = None
    i = 0
    while i < n:
        if buckets[i] != None:
            if first == None:
                first = buckets[i]
            tail = get_tail(buckets[i])
            j = i + 1
            while j < n and buckets[j] == None:
                j += 1
            if j < n:
                tail.next = buckets[j]
            else:
                return first
            i = j
        else:
            i += 1

    return first



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

arr = [2.64,6.23,2.89,3.69,4.001,7.999]
arr = tab2list(arr)
printlist(arr)
arr = sort(arr)
printlist(arr)