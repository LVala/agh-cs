from utils import gen_points_equally, cubic_spline, quadratic_spline, get_accuracy_abs, get_accuracy_sqr
from plotting import plot_from_func

import numpy as np

# function
k = 0.5
m = 4
left_end = -6
right_end = 6
f = lambda x: x**2 - m*np.cos((np.pi*x)/k)

for num_of_points in range(4,51):
    eql_x, eql_y = gen_points_equally(f, left_end, right_end, num_of_points)
    cubic = cubic_spline(eql_x, eql_y, 1)
    quadratic = quadratic_spline(eql_x, eql_y, 1)
    plot_from_func([f, cubic, quadratic], ["f", "cubic spline", "quadratic spline"], left_end, right_end, 2000, (eql_x, eql_y), f"{num_of_points} Points")

for num_of_points in range(4,51):
    eql_x, eql_y = gen_points_equally(f, left_end, right_end, num_of_points)
    cubic1 = cubic_spline(eql_x, eql_y, 1)
    cubic2 = cubic_spline(eql_x, eql_y, 2)
    plot_from_func([f, cubic1, cubic2], ["f", "cubic - warunek 1", "cubic - warunek 2"], left_end, right_end, 2000, (eql_x, eql_y), f"{num_of_points} Points")
    
    print(f"{num_of_points} points SQR: CUB 1 = {get_accuracy_sqr(f, cubic1, left_end, right_end, 1000):.3f}, CUB 2 = {get_accuracy_sqr(f, cubic2, left_end, right_end, 1000):.3f}")
    print(f"{num_of_points} points ABS: CUB 1 = {get_accuracy_abs(f, cubic1, left_end, right_end, 1000):.3f}, CUB 2 = {get_accuracy_abs(f, cubic2, left_end, right_end, 1000):.3f}")

for num_of_points in range(4,51):
    eql_x, eql_y = gen_points_equally(f, left_end, right_end, num_of_points)
    quadratic1 = quadratic_spline(eql_x, eql_y, 1)
    quadratic2 = quadratic_spline(eql_x, eql_y, 2)
    plot_from_func([f, quadratic1, quadratic2], ["f", "quadratic - warunek 1", "quadratic - warunek 2"], left_end, right_end, 2000, (eql_x, eql_y), f"{num_of_points} Points")
    
    print(f"{num_of_points} points SQR: QUAD 1 = {get_accuracy_sqr(f, quadratic1, left_end, right_end, 1000):.3f}, QUAD 2 = {get_accuracy_sqr(f, quadratic2, left_end, right_end, 1000):.3f}, QUAD 3 = {get_accuracy_sqr(f, quadratic3, left_end, right_end, 1000):.3f}")
    print(f"{num_of_points} points ABS: QUAD 1 = {get_accuracy_abs(f, quadratic1, left_end, right_end, 1000):.3f}, QUAD 2 = {get_accuracy_abs(f, quadratic2, left_end, right_end, 1000):.3f}, QUAD 3 = {get_accuracy_abs(f, quadratic3, left_end, right_end, 1000):.3f}")
