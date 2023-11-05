from typing import Callable
import numpy as np

def secant_roots(f: Callable[[float], float], a: float, b: float, epsilon: float, exit: int) -> float:
    b1 = b
    a1 = a
    iters = 0
    while True:
        x = (f(a1)*b1 - f(b1)*a1)/(f(a1) - f(b))
        iters += 1
        if f(x)*f(a1) > 0:
            a1, a = x, a1
            if exit == 1:
                if abs(a1-a) < epsilon: return b, iters
        elif f(x)*f(b1) > 0:
            b1, b = x, b1
            if exit == 1:
                if abs(b1-b) < epsilon: return b, iters
        if exit == 2:
            if abs(f(x)) < epsilon: return b, iters
        if iters > 3000:
            return 0, 0

def newton_roots(f: Callable[[float], float], d_f: Callable[[float], float], x: float, epsilon: float, exit: int) -> float:
    iters = 0
    while True:
        a = x
        x = x - f(x)/d_f(x)
        b = x
        iters += 1
        if exit == 2:
            if abs(f(b)) < epsilon: return b, iters
        elif exit == 1:
            if abs(b-a) < epsilon: return b, iters


def newton_matrix(F: Callable[[list[float]], list[float]], J: Callable[[list[float]], list[float]], X: list[float], epsilon: float, exit: int) -> list[float]:
    X = np.array(X)
    iters = 0
    while True:
        A = np.copy(X)
        try:
            S = np.linalg.solve(J(X), F(X))
        except np.linalg.LinAlgError:
            return ['x', 'x', 'x'], 'x'
        X = X - S
        iters += 1
        if exit == 1:
            if np.linalg.norm(X-A) < epsilon: return X, iters
        elif exit == 2:
            if np.linalg.norm(F(X)) < epsilon: return X, iters
        if iters > 500:
            return ['x','x','x'], 'x'