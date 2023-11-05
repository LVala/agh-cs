#include <x86intrin.h>

#define A(i, j) a[i * n + j]
#define max(i, j) i > j ? i : j

#define BLK_SIZE 8

void LUPDecompose(int n, double *a) {
  register int i, j, k; 
  register double div1;
  register __m128d div2, tmp0, tmp1, tmp2, tmp3;

  for (i = 0; i < n; i++) {
    div1 = A(i, i);
    for (j = i + 1; j < n; j++) {
      A(j, i) /= div1;
      div2 = _mm_loaddup_pd(&A(j, i));

      for (k = i + 1; k < n;)
        if (k < (max(n - BLK_SIZE, 0))) {
          tmp0 = _mm_loadu_pd(&A(i, k));
          tmp1 = _mm_loadu_pd(&A(i, k+2));
          tmp2 = _mm_loadu_pd(&A(i, k+4));
          tmp3 = _mm_loadu_pd(&A(i, k+6));

          tmp0 = _mm_mul_pd(div2, tmp0);
          tmp1 = _mm_mul_pd(div2, tmp1);
          tmp2 = _mm_mul_pd(div2, tmp2);
          tmp3 = _mm_mul_pd(div2, tmp3);

          A(j, k) -= tmp0[0];
          A(j, k+1) -= tmp0[1];
          A(j, k+2) -= tmp1[0];
          A(j, k+3) -= tmp1[1];
          A(j, k+4) -= tmp2[0];
          A(j, k+5) -= tmp2[1];
          A(j, k+6) -= tmp3[0];
          A(j, k+7) -= tmp3[1];
          k += BLK_SIZE;
        } else {
          A(j, k) -= A(j, i) * A(i, k);
          k++;
        }
    }
  }
}
