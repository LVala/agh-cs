from queue import PriorityQueue

S1 = ["a", "b", "c" ,"d", "e", "f" ]
F1 = [10, 11, 7, 13, 1, 20]

#całkowita złożoność czasowa O(nlogn) (pesymistyczna O(n^2), jeżeli liczymy funkcję print jako O(n))
#całkowita złożoność pamięciowa dane wejściowe + O(n) (elementy kopca w kolejce priorytetowej)

# klasa przchowująca gałęzie w drzewie Huffmana
# quan = ilość wystąpień, ind = index w tablicy S
# left i right to dzieci danej gałęzi, huff 
# posłuży do trzymania właściwego kodu
# złożoność pamięciowa dla n Nodeów to O(n)
# (poniważ ilość inforamcji w Node wpyłwa tylko na stałą w złożoności)
class Node():
    def __init__(self):
        self.quan = None
        self.ind= None
        self.left = None
        self.right = None
        self.huff = ''

    # metoda dająca możliwość porównywania klas Node między
    # sobą po wartości Node.quan
    # ażeby można było wygodnie korzystać z PriorityQueue
    def __gt__(self, other):
        return self.quan > other.quan

# funkcja przechodzi po gałęziach stworzonego drzewa
# dodając kolejnym Node'om odpowiadającą im kombinację 
# zer i jedynek, gdy dojdzie do liścia to dolicza koszt wypisania dango znaku
# oraz zapisuje wartość kodu huffmana w tablicy S, 
# (mogę nadpisać dane, poniważ nie będę ich więcej używać, plus oszczędzam pamięć)
# ażeby potem łatwo wypisać je w kolejność
# zgodnej z tabicą S
# O(n), ponieważ jest < 2*n Node'ów
def get_huff(F, node, val=''):
    cost = 0
    new_val = val + node.huff

    if node.left != None:
        cost += get_huff(F, node.left, new_val)
    if node.right != None:
        cost += get_huff(F, node.right, new_val)
    
    if node.left == None and node.right == None:
        cost = len(new_val)*F[node.ind]
        F[node.ind] = new_val

    return cost

# funkcja używa PriorityQueue do tworzenia kolejki priorytetowej
# gdzie największy prirytet mają elementy o najmniejszej wartości
# wystąpień, PrirityQueue jest oparta na kopcu min, więc wyciągnięcie i dodanie
# wartości ma złożoność czasową O(logn). Funkcja najpierw tworzy kolejkę priorytetową
# ze wszystkich n elementów S, następnie wyciąga dwa o najmniejszej ilości wystąpień
# i łączy je w jeden element o sumie wystąpień i dołącza do kolejki, a jako dzieci
# ustawia te dwa wyciągnięte elementy, robi to do momentu, aż w kolejce zostanie jeden
# element, co oznacza, że drzewo Huffmana zostało skonstruowane, w między czasie nadaje 
# też gałęziom wartości 0 dla tej o większej czestości, 1 dla mniejszej
# O(nlogn), bo logn - wyciągnięcie z kolejki * <2*n elementów
def huffman(S, F):
    n = len(S)
    A = PriorityQueue()
    
    # stworzenie kolejki
    for i in range(n):
        new_node = Node()
        new_node.quan = F[i]
        new_node.ind = i
        
        A.put(new_node)
    
    # właściwe operacje tworzenia drzewa
    # zakładam, że złożoność czasowa qsize 
    # to O(1), podobnie jak len
    while A.qsize() > 1:
        left = A.get()
        right = A.get()

        left.huff = '1'
        right.huff = '0'

        new_node = Node()
        new_node.quan = left.quan + right.quan
        new_node.left = left
        new_node.right = right
        A.put(new_node)

    # nadanie gałęziom właściwych kodów przy pomocy get_huff, zliczenie bitów
    cost = get_huff(F, A.get())

    # wypisanie kodów
    for i in range(n):
        print(f"{S[i]} : {F[i]}")
    print(f"dlugosc napisu : {cost}")

huffman( S1, F1 )