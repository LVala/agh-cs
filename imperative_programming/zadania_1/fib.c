#include <stdio.h>

int is_product(int n) {
    int a = 1, b = 0;
    while (a * b <= n) {
        if (a*b == n) return 1;
        int temp = a + b;
        b = a;
        a = temp;
    }
    return 0;
}

int main() {
    int a;
    scanf("%d", &a);
    int res = is_product(a);
    if (res == 1) {
        printf("YES");
    } else {
        printf("NO");
    }
    return 0;
}