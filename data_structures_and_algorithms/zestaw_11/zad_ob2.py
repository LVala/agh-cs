class Node():
    def __init__(self, key, parent):
        self.key = key
        self.value = None
        self.left = None
        self.right = None
        self.parent = parent

def find(root, key):
    while root != None:
        if root.key == key:
            return root
        elif key < root.key:
            root = root.left
        else:
            root = root.right

def insert(root, key, value):
    new_node = Node(key)
    new_node.value = value

    while True:
        if key < root.key:
            if root.left == None:
                root.left = new_node
                return
            else:
                root = root.left
        elif key > root.key:
            if root.right == None:
                root.right = new_node
                return
            else:
                root = root.right
        else:
            print("Key already exists")
            return

def remove(root):
    if root.left == None and root.right == None:
        temp = root
        root = root.parent
        if root.left == temp: root.left = None
        else: root.right = None
        return
    elif root.left == None or root.right == None:
        if root.left != None: temp = root.left
        else: temp = root.right
        temp2 = root
        root = root.parent
        if root.left == temp2: root.left = temp
        else: root.right = temp
        return
    else:
        temp = root
        root = root.left
        new, new_key = find_max(root)
        remove(new)
        temp.key = new_key

def find_min(root):
    while root.left != None:
        root = root.left
    return root, root.key

def find_max(root):
    while root.right != None:
        root = root.right
    return root, root.key

def previous_key(root):
    if root.left != None:
        root = root.left
        return find_max(root)
    else:
        temp = root
        while True:
            if root.parent == None:
                return None
            root = root.parent
            if root.right == temp:
                return root, root.key
            temp = root

def next_key(root):
    if root.right != None:
        root = root.right
        return find_min(root)
    else:
        temp = root
        while True:
            if root.parent == None:
                return None
            root = root.parent
            if root.left == temp:
                return root, root.key
            temp = root


R = Node(21, None)
R.left = Node(15, R)
R.left.left = Node(5, R.left)
R.left.left.right = Node(7, R.left.left)
R.left.left.right.right = Node(13, R.left.left.right)
R.left.left.right.right.left = Node(8, R.left.left.right.right)
R.left.right = Node(20, R.left)
R.right = Node(37, R)
R.right.left = Node(25, R.right)
R.right.right = Node(40, R.right)

print(next_key(R.left.left.right.right))
