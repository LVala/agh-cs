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
def gen_points_equally(func: Callable[[float], float], d_func: Callable[[float], float], left_end: int, right_end: int, num_of_points: int) -> tuple[list[float], list[float]]:
    array_x = np.linspace(left_end, right_end, num_of_points)
    array_y = [[func(i), d_func(i)] for i in array_x]
    return array_x.tolist(), array_y

def gen_points_chebyshev(func: Callable[[float], float], d_func: Callable[[float], float], left_end: int, right_end: int, num_of_points: int) -> tuple[list[float], list[float]]:
    cheb = lambda x: (left_end + right_end)/2 + ((right_end - left_end)*np.cos(((2*x+1)*np.pi)/(2*num_of_points)))/2
    array_x = [cheb(i) for i in range(num_of_points)]
    array_y = [[func(i), d_func(i)] for i in array_x]
    return array_x, array_y

# Hermite interpolation
def hermite_intpol(x_array: list[float], y_array: list[list[float]]) -> Callable[[float], float]:
    m_array = [len(i) for i in y_array]
    len_m = sum(m_array)
    f_array = [[None]*len_m for i in range(len_m)]
    lin_x_array = [None for i in range(len_m)]

    k = 0
    for i in range(len(m_array)):
        for j in range(m_array[i]):
            lin_x_array[k] = x_array[i]
            k += 1
    
    k = 0
    for val_i in y_array:
        for j in range(len(val_i)):
            for m in range(j+1):
                f_array[k-m][k] = val_i[m]/np.math.factorial(m)
            k += 1

    def diff(i: int, j: int) -> float:
        if f_array[i][j] != None: return f_array[i][j]
        f_array[i][j] = (diff(i+1, j) - diff(i, j-1))/(lin_x_array[j] - lin_x_array[i])
        return f_array[i][j]    

    diff(0, len_m - 1)
    
    def func(x: float) -> float:
        return horner_newton(lin_x_array, f_array[0], x)

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
