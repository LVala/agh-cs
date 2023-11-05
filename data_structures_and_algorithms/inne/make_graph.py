def make_graph():
    n = int(input("LEN >>>"))
    inpt = ""
    G = []
    while True:
        inpt = input(">>>")
        if inpt == "x": break
        inpt = inpt.split(" ")
        G.append([int(inpt[0]), int(inpt[1])])

    res = [[0]*n for _ in range(n)]

    for i in G:
        res[i[0]][i[1]] = 1
        res[i[1]][i[0]] = 1
    
    print("[", end="")
    for i in res:
        print(i, end="")
        print(",")
    print("]")

make_graph()