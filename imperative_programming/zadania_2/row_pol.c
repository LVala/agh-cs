#include <stdio.h>

int cmpr(int tab[], int n) {
    int l = 0, r = n-1;
    int sum_l = 0, sum_r = 0;
    while (l < r) {
        if (sum_l <= sum_r) {
            sum_l += tab[l];
            l++;
        } else {
            sum_r += tab[r];
            r--;
        }
    }
    return l;
}

int main() {
    int n;
    scanf("%d", &n);
    
    int tab[1000];
    for (int i=0; i<n; i++) {
        scanf("%d", &tab[i]);
    }
    int res = cmpr(tab, n);
    printf("%d", res);
    return 0;
}