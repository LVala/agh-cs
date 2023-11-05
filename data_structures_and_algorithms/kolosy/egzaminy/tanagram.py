#TIME: O(n), SPACE: O(n)

def tanagram(x, y, t):
    def count_sort(T):
        n = len(T)
        C = [0] * 26
        B = [0] * n
        for i in range(n):
            C[ord(T[i][0]) - ord("a")] += 1
        for i in range(1, 26):
            C[i] += C[i - 1]
        for i in range(n - 1, -1, -1):
            C[ord(T[i][0]) - ord("a")] -= 1
            B[C[ord(T[i][0]) - ord("a")]] = T[i]
        for i in range(n):
            T[i] = B[i]

    n = len(x)
    A = [0]*n
    B = [0]*n
    for i in range(n):
        A[i] = (x[i], i)
        B[i] = (y[i], i)

    count_sort(A)
    count_sort(B)

    for i in range(n):
        if abs(A[i][1] - B[i][1]) > t:
            return False
    return True
