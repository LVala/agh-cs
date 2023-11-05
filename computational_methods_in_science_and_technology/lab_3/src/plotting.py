from typing import Callable

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

def plot_from_array(array_x: list[float], array_y: list[float]) -> None:
    if len(array_x) != len(array_y):
        print("Error: length of arrays are different")
        return

    plt.style.use('seaborn')
    fig, ax = plt.subplots()
    ax.plot(array_x, array_y, color="black", marker=".")
    plt.xlabel("x")
    plt.ylabel("f(x)")

    plt.show()

def plot_from_func(funcs: list[Callable[[float], float]], 
                    names: list[str], 
                    left_end: int, 
                    right_end: int, 
                    num_of_points: int, 
                    knots: tuple[list[float], list[float]],
                    title: str) -> None:
    if (right_end < left_end):
        print("Error: right_end must be equal or greater than left_end")
        return
    if (num_of_points <= 0):
        print("Error: nmum_of_points must be positive")
        return

    plt.style.use('seaborn')
    fig, ax = plt.subplots()
    plt.title(title)
    plt.xlabel("x")
    plt.ylabel("f(x)")
    ax.plot(knots[0], knots[1], linestyle="None", marker="o", markerfacecolor="black", label="Equal points")
    
    for func, name, mcolor in zip(funcs, names, mcolors.BASE_COLORS.keys()):
        array_x = np.linspace(left_end, right_end, num_of_points)
        array_y = [func(i) for i in array_x]
        ax.plot(array_x, array_y, color=mcolor, label=name,)
        ax.legend()
    
    plt.show()
    # a = title.split(" ")[0]
    # plt.savefig(f"../img/quadratic_{a}")
    # plt.close()
