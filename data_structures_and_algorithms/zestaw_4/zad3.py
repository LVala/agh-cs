import numpy as np

def anagram(a, b, k):
    count = np.empty(k)
    counter = 0

    for i in a:
        count[ord(i) - ord("a")] = 0
    for i in b:
        count[ord(i) - ord("a")] = 0

    for i in a:
        count[ord(i) - ord("a")] += 1
        counter += 1
    for i in b:
        index = ord(i) - ord("a")
        if count[index] > 0:
            count[index] -= 1
            counter -= 1
        else:
            return False
        
    return counter == 0