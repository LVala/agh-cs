class Node():
    def __init__(self, value):
        self.value = value
        self.parent = parent
        self.left = None
        self.right = None
        self.size = 1


# znalezienei i-tego co do wielkości elementu, indeksowane od 1, nietestowane

def ith_elem(root, i):
    size_left = 0
    size_right = 0
    if root.left != None: size_left = root.left.size
    if root.right != None: size_right = root.right.size
    
    if i > root.size and root.right == None: return False

    if i == size_left + 1: return root.value
    elif i < size_left + 1: return ith_elem(root.left, i)
    elif i > size_left + 1: return ith_elem(root.right, i - size_left - 1)


# sprawdzenie, którym co do wielkości elementem jest root, indeksowane od 1, nietestowane

def elem_index(root):
    res = 1
    if root.left != None: res += root.left.size
    
    while root.parent != root:
        temp = root
        root = root.parent
        size_left = 0
        if root.left != None: size_left = root.left.size
        if root.right == temp:
            res += (size_left + 1)

    return res