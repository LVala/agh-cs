# Excercises 1.1)Try using local bubble sort and remote bubble sort,
# show difference
import ray
import cProfile
from copy import copy

ray.init(address="auto")

def bubble_sort(arr):
    sorted_arr = copy(arr)
    n = len(sorted_arr)
    swapped = False
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if sorted_arr[j] > sorted_arr[j + 1]:
                swapped = True
                sorted_arr[j], sorted_arr[j + 1] = sorted_arr[j + 1], sorted_arr[j]

        if not swapped:
            return sorted_arr

@ray.remote
def bubble_sort_distributed(arr):
    return bubble_sort(arr)

def sort_local(array_size, num_of_arrays):
    results = [bubble_sort([i for i in range(array_size, 0, -1)]) for _ in range(num_of_arrays)]
    return results

def sort_remote(array_size, num_of_arrays):
    results = ray.get([bubble_sort_distributed.remote([i for i in range(array_size, 0, -1)]) for _ in range(num_of_arrays)])
    return results

array_size = 1000
num_of_arrays = 100

print('local sort')
cProfile.run("sort_local(array_size, num_of_arrays)")

print('remote sort')
cProfile.run("sort_remote(array_size, num_of_arrays)")
