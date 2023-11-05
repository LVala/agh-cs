from queue import PriorityQueue
# algorytm dynamiczny działałałby podobnie jak knapsack

def job_sequencing(t, D, G):
    Q = PriorityQueue()

    for i in range(len(D)):
        Q.put( ((-1)*G[i], D[i], i) )

    slots_left = t
    res = [-1]*t
    while not Q.empty() and slots_left != 0:
        _, dl, ind = Q.get()

        for i in range(dl-1, -1, -1):
            if res[i] == -1:
                res[i] = ind
                slots_left -= 1
                break

    return res

t1 = 3
D1 = [2,1,2,1,3]
G1 = [100,19,27,25,15]

print(job_sequencing(t1, D1, G1))