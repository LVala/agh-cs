import numpy as np

from utils import gen_points_chebyshev, gen_points_equally, hermite_intpol, get_accuracy_sqr, get_accuracy_abs
from plotting import plot_from_func

# function
k = 0.5
m = 4
left_end = -6
right_end = 6
f = lambda x: x**2 - m*np.cos((np.pi*x)/k)
d_f = lambda x: 2*x + m*np.sin((np.pi*x)/k)*np.pi/k

for num_of_points in range(13,14):
    cheb_x, cheb_y = gen_points_chebyshev(f, d_f, left_end, right_end, num_of_points)
    eql_x, eql_y = gen_points_equally(f, d_f, left_end, right_end, num_of_points)
    vals_cheb_y = [i[0] for i in cheb_y]
    vals_eql_y = [i[0] for i in eql_y]

    # using newton and lagrange interpolation methods
    herm_cheb = hermite_intpol(cheb_x, cheb_y)
    herm_eql = hermite_intpol(eql_x, eql_y)

    plot_from_func([f, herm_cheb, herm_eql], ["f", "Hermite chebyshev", "Hermite equally"], left_end, right_end, 2000, [(cheb_x, vals_cheb_y), (eql_x, vals_eql_y)], f"{num_of_points} Points")
    plot_from_func([f, herm_cheb], ["f", "Hermite chebyshev"], left_end, right_end, 2000, [(cheb_x, vals_cheb_y), (eql_x, vals_eql_y)], f"{num_of_points} Points")

    print(f"{num_of_points} points SQR: HERMITE CHEB = {get_accuracy_sqr(f, herm_cheb, left_end, right_end, 1000):.8f}, EQL = {get_accuracy_sqr(f, herm_eql, left_end, right_end, 1000):.3f}")
    print(f"{num_of_points} points ABS: HERMITE CHEB = {get_accuracy_abs(f, herm_cheb, left_end, right_end, 1000):.3f}, EQL = {get_accuracy_abs(f, herm_eql, left_end, right_end, 1000):.3f}")


# searching for the best polynomial
best_poly = 1
best_poly_acc = float('inf')
for i in range(1, 100):
    cheb_x, cheb_y = gen_points_chebyshev(f, d_f, left_end, right_end, num_of_points)

    herm_cheb = hermite_intpol(cheb_x, cheb_y)
    acc = get_accuracy_sqr(f, herm_cheb, left_end, right_end, 1000)
    if (acc < best_poly_acc):
        print(i)
        best_poly = i
        best_poly_acc = acc

print(best_poly)
best_x, best_y = gen_points_chebyshev(f, left_end, right_end, 40)
best_newt = hermite_intpol(best_x, best_y)
plot_from_func([best_newt], [f"najlepszy hermite, dla {best_poly} pkt"], left_end, right_end, 2000)