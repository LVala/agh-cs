#include <immintrin.h>

#define A(i, j) a[i * n + j]
#define max(i, j) i > j ? i : j

#define BLK_SIZE 8

void LUPDecompose(int n, double *a) {
  register int i, j, k; 
  register double div1;
  register __m256d div2, tmp0, tmp1;
  __m128d div_tmp;

  for (i = 0; i < n; i++) {
    div1 = A(i, i);
    for (j = i + 1; j < n; j++) {
      A(j, i) /= div1;
      div_tmp = _mm_loaddup_pd(&A(j, i));
      div2 = _mm256_broadcast_pd(&div_tmp);

      for (k = i + 1; k < n;)
        if (k < (max(n - BLK_SIZE, 0))) {
          tmp0 = _mm256_loadu_pd(&A(i, k));
          tmp1 = _mm256_loadu_pd(&A(i, k+4));

          tmp0 = _mm256_mul_pd(div2, tmp0);
          tmp1 = _mm256_mul_pd(div2, tmp1);

          A(j, k) -= tmp0[0];
          A(j, k+1) -= tmp0[1];
          A(j, k+2) -= tmp0[2];
          A(j, k+3) -= tmp0[3];
          A(j, k+4) -= tmp1[0];
          A(j, k+5) -= tmp1[1];
          A(j, k+6) -= tmp1[2];
          A(j, k+7) -= tmp1[3];
          k += BLK_SIZE;
        } else {
          A(j, k) -= A(j, i) * A(i, k);
          k++;
        }
    }
  }
}
