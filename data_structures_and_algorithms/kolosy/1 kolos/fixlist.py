class Node():
    def __init__(self):
        self.next = None
        self.val = None

def fix_sorted_list(head):
    cur = head
    temp = None
    prev = None
    while cur != None:
        if prev == None:
            if cur.next.val < cur.val:  
                temp = cur
                head = cur.next
                break
        elif cur.next == None:
            if prev.val > cur.val:
                temp = cur
                prev.next = cur.next
                break
        else:
            if prev.val <= cur.next.val:
                if cur.val < prev.val or cur.val > cur.next.val:
                    temp = cur
                    prev.next = cur.next
                    break
        
        prev = cur
        cur = cur.next

    if temp == None:
        return head

    cur = head
    prev = None
    while cur != None and cur.val < temp.val:
        prev = cur
        cur = cur.next
    if prev != None:
        prev.next = temp
    temp.next = cur
    return head


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


arr = [3,4,5,8,12,13,14,7]
arr = tab2list(arr)
printlist(arr)
arr = fix_sorted_list(arr)
printlist(arr)