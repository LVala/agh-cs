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

# Lagrange interpolation
def lagrange_intpol(x_array: list[float], y_array: list[float]) -> Callable[[float], float]:
    m = [1]*len(x_array)
    for k in range(len(x_array)):
        for i in range(len(x_array)):
            if (i == k): continue
            m[k] *= (x_array[k] - x_array[i])

    def func(x: float) -> float:
        prod = 0
        for k in range(len(x_array)):  # len(x_array) == n+1
            d_k = 1
            for i in range(len(x_array)):
                if (i == k): continue
                d_k *= (x-x_array[i])
            prod += y_array[k] * d_k/m[k]
        return prod

    return func

# Newton interpolation
def newton_intpol(x_array: list[float], y_array: list[float]) -> Callable[[float], float]:
    f_array = [[None]*len(x_array) for i in range(len(x_array))]
    for i in range(len(x_array)): f_array[i][i] = y_array[i]
    
    def diff(i: int, j: int) -> float:
        if f_array[i][j] != None: return f_array[i][j]
        f_array[i][j] = (diff(i+1, j) - diff(i, j-1))/(x_array[j] - x_array[i])
        return f_array[i][j]

    diff(0, len(x_array) - 1)

    def func(x: float) -> float:
        return horner_newton(x_array, f_array[0], x)

    return func

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