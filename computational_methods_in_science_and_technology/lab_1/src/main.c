#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include <float.h>
#include <math.h>

// for long double
long double *ldouble_mul_poly(long double *poly1, int len1, long double *poly2, int len2) {
    long double *prod = calloc(len1 + len2 + 1, sizeof(long double));
    for (int i=0; i<len1; i++)
        for (int j=0; j<len2; j++)
            prod[i+j] += poly1[i] * poly2[j];
    return prod;
}

long double ldouble_get_value_sum(long double *poly, int len, long double arg) {
    long double prod = 0;
    for (int i=0; i<len; i++) {
        prod += pow(arg, i) * poly[i];
        // printf("PROD: %.15Lf\n", prod);
    }
    return prod;
}

long double ldouble_get_value_horner(long double *poly, int len, long double arg) {
    long double prod = poly[len-1];
    for (int i=len-2; i>=0; i--) {
        prod = prod * arg + poly[i];
        // printf("PROD: %.15Lf\n", prod);
    }
    return prod;
}

void ldouble_poly() { 
    long double poly1[21] = {-1, 1, 0};
    long double poly2[2] = {-2, 1};
    int len1, len2;
    len1 = len2 = 2;
    long double *prod;

    for (int i=1; i<20; i++) {
        prod = ldouble_mul_poly(poly1, len1, poly2, len2);
        ++len1;
        --poly2[0];
        for (int j=0; j<len1; j++)
            poly1[j] = prod[j];
        free(prod);
    }

    for (int i = 0; i < 21; i++)
        printf("a%d: %.15Lf\n", i, poly1[i]);
    printf("\n");

    long double horner = ldouble_get_value_horner(poly1, len1, 1.0);
    printf("WYNIK x=1.0 HORNER: %.15Lf\n\n", horner);
    long double sum = ldouble_get_value_sum(poly1, len1, 1.0);
    printf("WYNIK x=1.0 SUMA: %.15Lf\n\n", sum);
    long double horner2 = ldouble_get_value_horner(poly1, len1, 20.0);
    printf("WYNIK x=20.0 HORNER: %.15Lf\n\n", horner2);
    long double sum2 = ldouble_get_value_sum(poly1, len1, 20.0);
    printf("WYNIK x=20.0 SUMA: %.15Lf\n\n", sum2);

    poly1[19] += 0.000000000000001;
    long double horner3 = ldouble_get_value_horner(poly1, len1, 1.0);
    printf("WYNIK x=1.0 SHIFTED HORNER: %.17Lf\n\n", horner3);
    long double horner4 = ldouble_get_value_horner(poly1, len1, 20.0);
    printf("WYNIK x=20.0 SHIFTED HORNER: %.17Lf\n\n", horner4);

}

// for double
double *double_mul_poly(double *poly1, int len1, double *poly2, int len2) {
    double *prod = calloc(len1 + len2 + 1, sizeof(double));
    for (int i=0; i<len1; i++)
        for (int j=0; j<len2; j++)
            prod[i+j] += poly1[i] * poly2[j];
    return prod;
}

double double_get_value_sum(double *poly, int len, double arg) {
    double prod = 0;
    for (int i=0; i<len; i++) {
        prod += (pow(arg, i) * poly[i]);
        // printf("PROD: %.15f\n", prod);
    }
    return prod;
}

double double_get_value_horner(double *poly, int len, double arg) {
    double prod = poly[len-1];
    for (int i=len-2; i>=0; i--) {
        prod = prod * arg + poly[i];
        // printf("PROD: %.15f\n", prod);
    }
    return prod;
}

void double_poly() { 
    double poly1[21] = {-1, 1, 0};
    double poly2[2] = {-2, 1};
    int len1, len2;
    len1 = len2 = 2;
    double *prod;

    for (int i=1; i<20; i++) {
        prod = double_mul_poly(poly1, len1, poly2, len2);
        ++len1;
        --poly2[0];
        for (int j=0; j<len1; j++)
            poly1[j] = prod[j];
        free(prod);
    }

    for (int i = 0; i < 21; i++)
        printf("a%d: %.15f\n", i, poly1[i]);
    printf("\n");

    double horner = double_get_value_horner(poly1, len1, 1.0);
    printf("WYNIK x=1.0 HORNER: %.15f\n\n", horner);
    double sum = double_get_value_sum(poly1, len1, 1.0);
    printf("WYNIK x=1.0 SUMA: %.15f\n\n", sum);
    double horner2 = double_get_value_horner(poly1, len1, 20.0);
    printf("WYNIK x=20.0 HORNER: %.15f\n\n", horner2);
    double sum2 = double_get_value_sum(poly1, len1, 20.0);
    printf("WYNIK x=20.0 SUMA: %.15f\n\n", sum2);
}

// for long long
long long *ll_mul_poly(long long *poly1, int len1, long long *poly2, int len2) {
    long long *prod = calloc(len1 + len2 + 1, sizeof(long long));
    for (int i=0; i<len1; i++)
        for (int j=0; j<len2; j++)
            prod[i+j] += poly1[i] * poly2[j];
    return prod;
}

long long ll_get_value_sum(long long *poly, int len, long long arg) {
    long long prod = 0;
    for (int i=0; i<len; i++) {
        prod += (pow(arg, i) * poly[i]);
        // printf("PROD: %lld\n", prod);
    }
    return prod;
}

long long ll_get_value_horner(long long *poly, int len, long long arg) {
    long long prod = poly[len-1];
    for (int i=len-2; i>=0; i--) {
        prod = prod * arg + poly[i];
        // printf("PROD: %lld\n", prod);
    }
    return prod;
}

void ll_poly() { 
    long long poly1[21] = {-1, 1, 0};
    long long poly2[2] = {-2, 1};
    int len1, len2;
    len1 = len2 = 2;
    long long *prod;

    for (int i=1; i<20; i++) {
        prod = ll_mul_poly(poly1, len1, poly2, len2);
        ++len1;
        --poly2[0];
        for (int j=0; j<len1; j++)
            poly1[j] = prod[j];
        free(prod);
    }

    for (int i = 0; i < 21; i++)
        printf("a%d: %lld\n", i, poly1[i]);
    printf("\n");

    long long horner = ll_get_value_horner(poly1, len1, 1);
    printf("WYNIK x=1.0 HORNER: %lld\n\n", horner);
    long long sum = ll_get_value_sum(poly1, len1, 1);
    printf("WYNIK x=1.0 SUMA: %.lld\n\n", sum);
    long long horner2 = ll_get_value_horner(poly1, len1, 20);
    printf("WYNIK x=20.0 HORNER: %lld\n\n", horner2);
    long long sum2 = ll_get_value_sum(poly1, len1, 20);
    printf("WYNIK x=20.0 SUMA: %lld\n\n", sum2);
}


int main() {
    printf("-----DOUBLE-----\n");
    double_poly();
    printf("-----LONG DOUBLE-----\n");
    ldouble_poly();
    printf("-----LONG LONG INT-----\n");
    ll_poly();
    return 0;
}