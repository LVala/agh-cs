def what_to_cut(trees):
    n = len(trees)
    f_i2 = trees[0]
    f_i1 = max(trees[0], trees[1])
    for i in range(2,n):
        f = max(f_i1, f_i2 + trees[i]) #Aktualny
        f_i2 = f_i1
        f_i1 = f
    print(f_i1)


trees =[2,2,2,1]
what_to_cut(trees)