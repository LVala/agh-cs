#include <stdio.h>
#include <math.h>

int doskonala(int n) {
    if (n == 1) return 0;
    int count = 1, p = sqrt(n);
    for (int i = 2; i <= p; i++) {
        if (n % i == 0) {
            count += i + n/i;
        }
    }
    if (n == p*p) {
        count -= p;
    }
    if (count == n) return 1;
    return 0;
}

int main() {
    int tab[10];
    int a, b, count = 0, j = 0;
    scanf("%d %d", &a, &b);
    for (int i = a; i <= b; i++) {
        int res = doskonala(i);
        if (res != 0) {
            tab[j] = i;
            j++;
        }
        count += res;
    }
    printf("%d\n", count);
    for (int i = 0; i < count; i++) {
        printf("%d ", tab[i]);
    }
}