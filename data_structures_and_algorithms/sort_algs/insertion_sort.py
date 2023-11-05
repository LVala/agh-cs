#O(n^2), optymistyczna n, gdy lista jest posortowana

class Node():
    def __init__(self):
        self.val = None
        self.next = None

def insertion_sort(T):
    for i in range(1, len(T)):
        key = T[i]
        j = i - 1
        while j >= 0 and T[j] > key:
            T[j + 1] = T[j]
            j -= 1
        T[j + 1] = key
    return T

def insertion_sort_ll(head):
    def insert(head, new_node):
        if head == None or head.val >= new_node.val:
            new_node.next = head
            return new_node
        else:
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
