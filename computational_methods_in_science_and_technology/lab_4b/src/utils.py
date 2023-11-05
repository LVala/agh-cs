from typing import Callable

import numpy as np

# functions generating points (equally distributed or distributed based on Chebyshev nodes)
def gen_points_equally(func: Callable[[float], float], left_end: int, right_end: int, num_of_points: int) -> tuple[list[float], list[float]]:
    array_x = np.linspace(left_end, right_end, num_of_points)
    array_y = [func(i) for i in array_x]
    return array_x.tolist(), array_y

# accuracy calculation
def get_accuracy_sqr(func1: Callable[[float], float], func2: Callable[[float], float], left_end: int, right_end: int, points: int) -> float:
    prod = 0
    array = np.linspace(left_end, right_end, points)
    for i in array:
        prod += (func1(i) - func2(i))**2
    return prod/points

def get_accuracy_abs(func1: Callable[[float], float], func2: Callable[[float], float], left_end: int, right_end: int, points: int) -> float:
    prod = 0
    array = np.linspace(left_end, right_end, points)
    for i in array:
        temp = abs(func1(i) - func2(i))
        prod = max(prod, temp)
    return prod

# trigonometric polynomial approximation
def trigpoly_approx(x_array: list[float], y_array: list[float], w_array: list[float], m: int) -> Callable[[float], float]:
    if (2*m+1 > len(x_array)):
        print("Error: length of input points array must be 2*m+1 or greater")
        exit(1)

    a = x_array[0] 
    b = x_array[-1]
    change_interval = lambda x: (2*np.pi*x - 2*np.pi*a)/(b-a)
    
    x_array = change_interval(np.array(x_array))
    y_array = np.array(y_array)
    w_array = np.array(w_array)

    G_matrix = np.zeros((2*m+1, 2*m+1))
    B_matrix = np.empty(2*m+1)

    # first derivative by a_0
    B_matrix[0] = (w_array * y_array).sum()
    G_matrix[0, 0] = w_array.sum()
    for j in range(m):
        G_matrix[0, 2*j+1] = (w_array * np.cos((j+1) * x_array)).sum()
        G_matrix[0, 2*j+2] = (w_array * np.sin((j+1) * x_array)).sum()

    # rest of the derivatives a_1-a_m, b_1-b_m
    for k in range(m):
        B_matrix[2*k+1] = (w_array * y_array * np.cos((k+1) * x_array)).sum()
        B_matrix[2*k+2] = (w_array * y_array * np.sin((k+1) * x_array)).sum()
        G_matrix[2*k+1, 0] = (w_array * np.cos((k+1) * x_array)).sum()
        G_matrix[2*k+2, 0] = (w_array * np.sin((k+1) * x_array)).sum()
        for j in range(m):
            G_matrix[2*k+1, 2*j+1] = (w_array * np.cos((k+1)*x_array) * np.cos((j+1)*x_array)).sum()
            G_matrix[2*k+1, 2*j+2] = (w_array * np.cos((k+1)*x_array) * np.sin((j+1)*x_array)).sum()
            G_matrix[2*k+2, 2*j+1] = (w_array * np.sin((k+1)*x_array) * np.cos((j+1)*x_array)).sum()
            G_matrix[2*k+2, 2*j+2] = (w_array * np.sin((k+1)*x_array) * np.sin((j+1)*x_array)).sum()
        
    A_matrix = np.linalg.solve(G_matrix, B_matrix)

    def func(x):
        x = change_interval(x)
        base = np.array([1] + [j for i in range(m) for j in (np.cos((i+1)*x), np.sin((i+1)*x))])
        return (base * A_matrix).sum()

    return func
  