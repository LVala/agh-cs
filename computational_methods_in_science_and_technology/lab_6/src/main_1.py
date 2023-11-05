from utils import gaussian_elimination
import numpy as np

for n in range(3, 101):
    print(n, end=" & ")
    for fltype in (np.float32, np.float64, np.float128):
        A = np.array([[1/(i+j-1) if i != 1 else 1 for j in range(1,n+1)] for i in range(1,n+1)]).astype(fltype)
        X_known = np.array([1 if i%2==0 else -1 for i in range(n)]).astype(fltype)  # alternating 1, -1, 1, -1, ...
        B = A @ X_known
        X = gaussian_elimination(A, B)
        norm = np.linalg.norm(X_known-X)
        if fltype != np.float128:
            print(f"{norm:.5e}", end=" & ")
        else:
            print(f"{norm:.5e}", end=" \\\\ \\hline\n")
