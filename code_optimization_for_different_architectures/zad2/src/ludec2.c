#define A(i, j) a[i * n + j]
#define max(i, j) i > j ? i : j

#define BLK_SIZE 8

void LUPDecompose(int n, double *a) {
  register int i, j, k; 
  register double div1, div2;

  for (i = 0; i < n; i++) {
    div1 = A(i, i);
    for (j = i + 1; j < n; j++) {
      A(j, i) /= div1;
      div2 = A(j, i);

      for (k = i + 1; k < n;)
        if (k < (max(n - BLK_SIZE, 0))) {
          A(j, k) -= div2 * A(i, k);
          A(j, k+1) -= div2 * A(i, k+1);
          A(j, k+2) -= div2 * A(i, k+2);
          A(j, k+3) -= div2 * A(i, k+3);
          A(j, k+4) -= div2 * A(i, k+4);
          A(j, k+5) -= div2 * A(i, k+5);
          A(j, k+6) -= div2 * A(i, k+6);
          A(j, k+7) -= div2 * A(i, k+7);
          k += BLK_SIZE;
        } else {
          A(j, k) -= div2 * A(i, k);
          k++;
        }
    }
  }
}
