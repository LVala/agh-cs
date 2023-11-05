#TIME: O(sum(n)*logn), SPACE: O(1)
# n - liczba list, sum(n) - liczba elementów wszystkich list

class Node():
    def __init__(self):
        self.next = None
        self.val = None

def mergelists(T):
    def merge(A, B):
        C = Node()
        tail = C
        while A != None and B != None:
            if A.val <= B.val:
                tail.next = A
                A = A.next
                tail = tail.next
                tail.next = None
            else:
                tail.next = B
                B = B.next
                tail = tail.next
                tail.next = None

        if A != None: tail.next = A
        if B != None: tail.next = B

        return C.next

    n = len(T)
    while True:
        i = 0
        while i < n:
            if T[i] != None:
                j = i + 1
                while j < n and T[j] == None: j += 1
                if i == 0 and j >= n: return T[0]
                if j >= n: break
                T[i] = merge(T[i], T[j])
                T[j] = None
                i = j + 1
            else: i += 1
