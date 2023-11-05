class Node:
    def __init__(self, left=None, leftval=0, right=None, rightval=0):
        self.left = left  # lewe podrzewo
        self.leftval = leftval  # wartość krawędzi do lewego poddrzewa jeśli istnieje
        self.right = right  # prawe poddrzewo
        self.rightval = rightval  # wartość krawędzi do prawego poddrzewa jeśli istnieje
        self.X = None  # miejsce na dodatkowe dane

def valuableTree( T, k ):
    def f(root, i):
        nonlocal k
        if root == None: return (-1)*float("inf")
        if i == 0: return 0
        if root.left == None and root.right == None and i != 0: return (-1)*float("inf")
        if root.X != None and root.X[i] != None:
            return root.X[i] 
        
        res = max(root.leftval + f(root.left, i-1), root.rightval + f(root.right, i-1))
        
        for j in range(i-1):
            res = max(res, root.leftval + root.rightval + f(root.left, j) + f(root.right, i-2-j))
        
        if root.X == None: root.X = [None]*(k+1)
        root.X[i] = res
        return root.X[i]

    def get_res(root, k):
        nonlocal end_res
        res = f(root, k)
        end_res = max(res, end_res)
        if root.left != None: get_res(root.left, k)
        if root.right != None: get_res(root.right, k)

    end_res = (-1)*float("inf")
    get_res(T, k)

    return end_res

A = Node()
B = Node()
C = Node()
D = Node()
E = Node()
F = Node()
G = Node()
H = Node()
K = Node()
A.leftval = -5
A.rightval = -1
A.left = B
A.right = C
C.rightval = -1
C.right = H
H.left = K
H.leftval = -1
B.leftval = -2
B.rightval = -3
B.left = D
B.right = F
D.leftval = -6
D.left = E
F.rightval = -2
F.left = G

print(valuableTree(A, 3))
