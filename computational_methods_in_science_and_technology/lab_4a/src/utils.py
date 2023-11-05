from typing import Callable

import numpy as np

# Horner algorithm for polynomial in Newton form
def horner_newton(x_array: list[float], b_array: list[float], arg: float) -> float:
    # len(b_array) == n + 1
    prod = b_array[len(b_array)-1]  # n'th elemen
    for i in range(len(b_array)-2, -1, -1):
        prod = prod*(arg - x_array[i]) + b_array[i]
    return prod

# functions generating points (equally distributed or distributed based on Chebyshev nodes)
def gen_points_equally(func: Callable[[float], float], left_end: int, right_end: int, num_of_points: int) -> tuple[list[float], list[float]]:
    array_x = np.linspace(left_end, right_end, num_of_points)
    array_y = [func(i) for i in array_x]
    return array_x.tolist(), array_y

def gen_points_chebyshev(func: Callable[[float], float], left_end: int, right_end: int, num_of_points: int) -> tuple[list[float], list[float]]:
    cheb = lambda x: (left_end + right_end)/2 + ((right_end - left_end)*np.cos(((2*x+1)*np.pi)/(2*num_of_points)))/2
    array_x = [cheb(i) for i in range(num_of_points)]
    array_y = [func(i) for i in array_x]
    return array_x, array_y

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

# algebraic polynomial approximation
def algpoly_approx(x_array: list[float], y_array: list[float], w_array: list[float], m: int) -> Callable[[float], float]:
    if (m+1 > len(x_array)):
        print("Error: m must be smaller or equal to length of input points array")
        exit(1)

    n = len(x_array)

    G_matrix = [[0]*(m+1) for _ in range(m+1)]
    B_matrix = [0 for _ in range(m+1)]

    for i in range(m+1):
        B_matrix[i] = sum(w_array[k]*y_array[k]*(x_array[k]**i) for k in range(n))
        for j in range(m+1):
            G_matrix[i][j] = G_matrix[i-1][j+1] if i-1 >= 0 and j+1 < m+1 else sum(w_array[k]*(x_array[k]**(i+j)) for k in range(n))

    A_matrix = np.linalg.solve(np.array(G_matrix), np.array(B_matrix))

    def func(x):
        return sum(A_matrix[i]*(x**i) for i in range(m+1))

    return func