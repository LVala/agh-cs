#define A(i, j) a[i * n + j]

/* INPUT: a - array representing matrix of size n x n
 * OUTPUT: Matrix a is changed: a=(L-E)+U such that old a=L*U.
 */
void LUPDecompose(int n, double *a) {
  register int i, j, k; 
  register double div1, div2;

  for (i = 0; i < n; i++) {
    div1 = A(i, i);
    for (j = i + 1; j < n; j++) {
      A(j, i) /= div1;
      div2 = A(j, i);

      for (k = i + 1; k < n; k++)
        A(j, k) -= div2 * A(i, k);
    }
  }
}
