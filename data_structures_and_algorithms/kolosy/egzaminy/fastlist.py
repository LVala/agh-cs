#TIME: O(logn), SPACE: O(1), najwyżej że liczyć tą liste wskaźników

class FastListNode:
    def __init__(self, a):
        self.a = a     # przechowywana liczba calkowita
        self.next = [] # lista odnosnikow do innych elementow; poczatkowo pusta

    def __str__(self): # zwraca zawartosc wezla w postaci napisu
        res = 'a: ' + str(self.a) + '\t' + 'next keys: '
        res += str([n.a for n in self.next])
        return res

def fast_list_prepend(L,a):
    H = FastListNode(a)
    i = 0
    H.next.append(L)
    while L != None and i < len(L.next):
        H.next.append(L.next[i])
        L = L.next[i]
        i += 1

    return H
