#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <time.h>

#include "ludec4.c"

#define A(i, j) a[i * n + j]
#define B(i, j) b[i * n + j]

#define PFIRST 40 
#define PLAST 800
#define PINC 40
#define MAX_RAND 1000
#define PRINT_CHECK 0

static double gtod_ref_time_sec = 0.0;

void random_matrix(int, double*);
void copy_matrix(int, double*, double*);
double check(int, double*);
double dclock();

int main(int argc, const char *argv[]) {
  double dtime, check_val, gflops;
  double *a, *copy;
  int *p;

  for (int n=PFIRST; n<=PLAST; n+=PINC) {
    gflops = (2 * n * n * n * 1.0e-09)/3;

    a = malloc(n * n * sizeof(double));
    random_matrix(n, a);

    dtime = dclock();
    LUPDecompose(n, a);
    dtime = dclock() - dtime;

    if (PRINT_CHECK) {
      check_val = check(n, a);
      printf("N = %d, CHECK = %f\n", n, check_val);
    }

    printf("%d %f\n", n, gflops / dtime);

    free(a);
  }

  return 0;
}

double check(int n, double *a) {
  double check = 0.0;
  for (int i=0; i<n; i++) {
    for (int j=0; j<n; j++) {
      check += A(i, j);
    }
  }
  return check;
}

void random_matrix(int n, double *a) {
  srand(1);

  for (int i=0; i<n; i++) {
    for (int j=0; j<n; j++) {
      A(i, j) = rand() % MAX_RAND;
    }
  }
}

/* Adapted from the bl2_clock() routine in the BLISS library */
double dclock() {
  double the_time, norm_sec;
  struct timeval tv;

  gettimeofday(&tv, NULL);

  if (gtod_ref_time_sec == 0.0)
    gtod_ref_time_sec = (double) tv.tv_sec;

  norm_sec = (double) tv.tv_sec - gtod_ref_time_sec;

  the_time = norm_sec + tv.tv_usec * 1.0e-6;

  return the_time;
}

