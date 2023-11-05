#include <stdio.h>
#include <math.h>

int is_prime(int n) {
    if (n == 2) return 1;
    if (n % 2 == 0 || n < 2) return 0;
    int p = sqrt(n);
    for (int i = 3; i <= p; i += 2) {
        if (n % i == 0) return 0;
    }
    return 1;
}

int is_jdkw(int n) {
    int res = 0;
    while (n != 1 && n != 4) {
        while (n > 0) {
            int temp = (n%10)*(n%10);
            res += temp;
            n /= 10;
        }
        n = res;
        res = 0;
    }
    return n;
}

int pri(int l, int u, int k) {
    int count = 0;
    int res = 0;

    if (l%2==0) l+= 1;
    for (int i = l; i <= u; i += 2) {
        if (count == k) return res;
        if (is_prime(i) == 1 && is_jdkw(i) == 1) {
            count += 1;
            res = i;
        }
    }
    return -1;
}   

void main() {
    int l,u,k;
    scanf("%d %d %d", &l, &u, &k);

    int res = pri(l, u, k);

    printf("%d", res);
}