def maxspan(A):
    n = len(A)
    min_ = A[0]
    max_ = A[0]
    for i in range(n):
        min_ = min(min_, A[i])
        max_ = max(max_, A[i])

    B = [[] for _ in range(n)]
    x = (max_ - min_) / n

    for i in range(n):
        d = (A[i] - min_)//x
        B[d].append(A[i])

    result = 0
    prev_max = max(B[0])
    for i in range(1, n):
        if len(B[i]) != 0:
            act_min = min(B[i])
            result = max(result, act_min - prev_max)
            prev_max = max(B[i])

    return result