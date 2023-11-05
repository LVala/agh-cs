def quicksort_iter(T):
    def partition(T, left, right):
        pivot = T[right]
        i = left
        for j in range(left, right + 1):
            if T[j] <= pivot:
                T[j], T[i] = T[i], T[j]
                i += 1
        return i - 1

    stack = []
    stack.append((0, len(T) - 1))
    while len(stack) > 0:
        left, right = stack.pop()
        if left < right:
            mid = partition(T, left, right)
            stack.append((left, mid - 1))
            stack.append((mid + 1, right))
