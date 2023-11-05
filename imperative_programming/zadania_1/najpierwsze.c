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

int malejace(int n) {
    int prev = n % 10;
    n /= 10;
    int next = n % 10;
    while (n > 0) {
        if (next > prev) return 0;
        n /= 10;
        prev = next;
        next = n % 10;
    }
    return 1;
}   

int main() {
    int a;
    scanf("%d", &a);
    for (int i = 2; i <= a; i++) {
        int cond1 = is_prime(i);
        if (cond1 == 1) {
            int cond2 = malejace(i);
            if (cond2 == 1) {
                printf("%d\n", i);
            }
        }
    }
    return 0;
}