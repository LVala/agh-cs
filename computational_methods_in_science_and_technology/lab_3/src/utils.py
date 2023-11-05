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

# spline functions interpolation
def quadratic_spline(x_array: list[float], y_array: list[float], boundaries_mode: int) -> Callable[[float], float]:
    n = len(x_array)
    A_matrix = [[0]*(3*(n-1)) for _ in range(3*(n-1))]
    B_matrix = [0 for _ in range(3*(n-1))]

    for i in range(n-1):
        A_matrix[i][i] = 1
        A_matrix[i][n-1+i] = x_array[i]
        A_matrix[i][2*(n-1)+i] = x_array[i]**2
        B_matrix[i] = y_array[i]
    
    for i in range(n-1):
        A_matrix[n-1+i][i] = 1
        A_matrix[n-1+i][n-1+i] = x_array[i+1]
        A_matrix[n-1+i][2*(n-1)+i] = x_array[i+1]**2
        B_matrix[n-1+i] = y_array[i+1]

    for i in range(n-2):
        A_matrix[2*(n-1)+i][n-1+i] = 1
        A_matrix[2*(n-1)+i][n+i] = -1
        A_matrix[2*(n-1)+i][2*(n-1)+i] = 2*x_array[i+1]
        A_matrix[2*(n-1)+i][2*(n-1)+i+1] = -2*x_array[i+1]

    delta = lambda i: (y_array[i+1] - y_array[i])/(x_array[i+1] - x_array[i])
    delta_2 = lambda i: (delta(i+1) - delta(i))/(x_array[i+2] - x_array[i])

    if boundaries_mode == 1:  # second derivative at the starting point set to 0
        A_matrix[3*(n-1)-1][2*(n-1)] = 1
    elif boundaries_mode == 2: # # second derivative at the starting point approximated with difference quotient
        A_matrix[3*(n-1)-1][n-1] = 1
        B_matrix[3*(n-1)-1] = delta_2(0)

    X_matrix = np.linalg.solve(np.array(A_matrix), np.array(B_matrix))

    def func(x):
        for i in range(n-1):
            if x_array[i] <= x <= x_array[i+1]:
                return X_matrix[i] + X_matrix[n-1+i]*x + X_matrix[2*(n-1)+i]*(x**2)

    return func

def cubic_spline(x_array: list[float], y_array: list[float], boundaries_mode: int) -> Callable[[float], float]:
    n = len(x_array)
    h_array = [x_array[i+1] - x_array[i] for i in range(n - 1)]
    delta_array = [(y_array[i+1] - y_array[i])/h_array[i] for i in range(n - 1)]
    sigma_matrix = [[0]*(n) for _ in range(n)]
    sigma_array = [0]*n

    for i in range(1,n-1):
        sigma_array[i] = delta_array[i] - delta_array[i-1]
        sigma_matrix[i][i-1] = h_array[i-1]
        sigma_matrix[i][i] = 2*(h_array[i-1] + h_array[i])
        sigma_matrix[i][i+1] = h_array[i]

    if boundaries_mode == 1:
        delta = lambda i: (y_array[i+1] - y_array[i])/(x_array[i+1] - x_array[i])
        delta_2 = lambda i: (delta(i+1) - delta(i))/(x_array[i+2] - x_array[i])
        delta_3 = lambda i: (delta_2(i+1) - delta_2(i))/(x_array[i+3] - x_array[i])
        sigma_array[0] = h_array[0]*h_array[0]*delta_3(0)
        sigma_array[n-1] = (-1)*h_array[n-2]*h_array[n-2]*delta_3(n-4)
        sigma_matrix[0][0] = (-1)*h_array[0]
        sigma_matrix[0][1] = h_array[0]
        sigma_matrix[n-1][n-2] = h_array[n-2]
        sigma_matrix[n-1][n-1] = (-1)*h_array[n-2]
    elif boundaries_mode == 2:  # naural cubic spline (free boundary)
        sigma_matrix[0][0] = 1
        sigma_matrix[n-1][n-1] = 1

    delta_sol = np.linalg.solve(np.array(sigma_matrix), np.array(sigma_array))

    b_i = [(y_array[i+1] - y_array[i])/h_array[i] - h_array[i]*(delta_sol[i+1] + 2*delta_sol[i]) for i in range(n-1)]
    c_i = [3*delta_sol[i] for i in range(n-1)]
    d_i = [(delta_sol[i+1] - delta_sol[i])/h_array[i] for i in range(n-1)]
        
    def func(x):
        for i in range(n-1):
            if x_array[i] <= x <= x_array[i+1]:
                return y_array[i] + b_i[i]*(x - x_array[i]) + c_i[i]*(x - x_array[i])**2 + d_i[i]*(x - x_array[i])**3
        
    return func
