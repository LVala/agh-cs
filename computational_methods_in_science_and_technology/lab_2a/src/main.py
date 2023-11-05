import numpy as np

from utils import gen_points_chebyshev, gen_points_equally, newton_intpol, lagrange_intpol, get_accuracy_sqr, get_accuracy_abs
from plotting import plot_from_func

# function
k = 0.5
m = 4
left_end = -6
right_end = 6
f = lambda x: x**2 - m*np.cos((np.pi*x)/k)

# interpolation using different methods and different distributions of points for increasing number of points
for num_of_points in range(1,51,2):
    cheb_x, cheb_y = gen_points_chebyshev(f, left_end, right_end, num_of_points)
    eql_x, eql_y = gen_points_equally(f, left_end, right_end, num_of_points)

    # using newton and lagrange interpolation methods
    newt_cheb = newton_intpol(cheb_x, cheb_y)
    newt_eql = newton_intpol(eql_x, eql_y)
    lagr_cheb = lagrange_intpol(cheb_x, cheb_y)
    lagr_eql = lagrange_intpol(eql_x, eql_y)

    plot_from_func([f, newt_cheb, newt_eql], ["f", "Newton chebyshev", "Newton equally"], left_end, right_end, 2000, [(cheb_x, cheb_y), (eql_x, eql_y)], f"{num_of_points} Points")
    plot_from_func([f, lagr_cheb, lagr_eql], ["f", "Lagrange chebyshev", "Lagrange equally"], left_end, right_end, 2000, [(cheb_x, cheb_y), (eql_x, eql_y)], f"{num_of_points} Points")

    print(f"{num_of_points} points SQR: NEWTON CHEB = {get_accuracy_sqr(f, newt_cheb, left_end, right_end, 1000):.8f}, EQL = {get_accuracy_sqr(f, newt_eql, left_end, right_end, 1000):.2f} \
        LAGRANGE CHEB = {get_accuracy_sqr(f, lagr_cheb, left_end, right_end, 1000):.8f}, EQL = {get_accuracy_sqr(f, lagr_eql, left_end, right_end, 1000):.2f}")
    print(f"{num_of_points} points ABS: NEWTON CHEB = {get_accuracy_abs(f, newt_cheb, left_end, right_end, 1000):.8f}, EQL = {get_accuracy_abs(f, newt_eql, left_end, right_end, 1000):.8f} \
        LAGRANGE CHEB = {get_accuracy_abs(f, lagr_cheb, left_end, right_end, 1000):.8f}, EQL = {get_accuracy_abs(f, lagr_eql, left_end, right_end, 1000):.8f}")
    


# searching for the best polynomial
best_poly = 1
best_poly_acc = float('inf')
for i in range(1, 100):
    x, y = gen_points_chebyshev(f, left_end, right_end, i)
    newt = lagrange_intpol(x, y)
    acc = get_accuracy_sqr(f, newt, left_end, right_end, 10000)
    if (acc < best_poly_acc):
        print(i)
        best_poly = i
        best_poly_acc = acc

print(best_poly)
best_x, best_y = gen_points_chebyshev(f, left_end, right_end, 40)
best_newt = lagrange_intpol(best_x, best_y)
plot_from_func([best_newt], [f"najlepszy newton, dla {best_poly} pkt"], left_end, right_end, 2000)