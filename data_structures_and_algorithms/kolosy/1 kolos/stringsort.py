def sortstring(A):
    max_len = 0
    for i in range(len(A)):
        max_len = max(max_len, len(A[i]))
    n = ord("z") - ord("a") + 2
    for i in range(max_len - 1, -1, -1):
        buckets = [[] for i in range(n)]
        for j in range(len(A)):
            index = 0
            if i < len(A[j]):
                index = ord(A[j][i]) - ord("a") + 1
            buckets[index].append(A[j])
        k = 0
        for m in range(n):
            for b in range(len(buckets[m])):
                A[k] = buckets[m][b]
                k += 1


arr = ["bbbc", "bbba", "aaab", "fffd", "fffr", "zzz"]
sortstring(arr)
print(arr)