#define A(i, j) a[i * n + j]

/* INPUT: a - array representing matrix of size n x n
 * OUTPUT: Matrix a is changed: a=(L-E)+U such that old a=L*U.
 */
int LUPDecompose(int n, double *a) {
  int i, j, k; 

  for (i = 0; i < n; i++) {
    for (j = i + 1; j < n; j++) {
      A(j, i) /= A(i, i);

      for (k = i + 1; k < n; k++)
        A(j, k) -= A(j, i) * A(i, k);
    }
  }
}
