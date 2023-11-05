from utils import gen_points_equally, get_accuracy_abs, get_accuracy_sqr, trigpoly_approx
from plotting import plot_from_func

import numpy as np

# function
k = 0.5
m = 4
left_end = -6
right_end = 6
f = lambda x: x**2 - m*np.cos((np.pi*x)/k)

# for degree in range(13, 21):
#     for num_of_points in range(2*degree+1,52):
#         eql_x, eql_y = gen_points_equally(f, left_end, right_end, num_of_points)
#         weights = [1]*num_of_points
#         tri = trigpoly_approx(eql_x, eql_y, weights, degree)

#         plot_from_func([f, tri], ["f", f"approximation with trigonometric polynomials of {degree}th degree"], left_end, right_end, 2000, (eql_x, eql_y), f"{num_of_points} Points")
#         # print(f"{num_of_points} points | SQR = {get_accuracy_sqr(f, tri, left_end, right_end, 1000):.3f}, ABS = {get_accuracy_abs(f, tri, left_end, right_end, 1000):.3f}")


for num_of_points in range(7,52):
    print(f"{num_of_points}", end=" & ")
    for degree in range(3, 21):
        if degree == 20:
                end = " "
        else: end = " & "
        
        if degree == 13:
            print("...", end=end)
        elif degree > 13 and degree < 20:
            pass
        elif num_of_points > 2*degree:
            eql_x, eql_y = gen_points_equally(f, left_end, right_end, num_of_points)
            weights = [1]*num_of_points
            tri = trigpoly_approx(eql_x, eql_y, weights, degree)
            if degree < 12:
                print(f"{get_accuracy_abs(f, tri, left_end, right_end, 1000):.2f}", end=end)
            else:
                print(f"{get_accuracy_abs(f, tri, left_end, right_end, 1000):.3f}", end=end)
        else:
            print("X", end=end)
    print("\\\\ \\hline")
