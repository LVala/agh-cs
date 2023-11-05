#include <stdio.h>

int weight(int arr[], int masa, int n, int index) {
    if (masa == 0) return 1;
    if (index >= n) return 0;
    int res1 = weight(arr, masa - arr[index], n, index + 1);
    int res2 = weight(arr, masa + arr[index], n, index + 1);
    if (res1 + res2 >= 1) return 1;
    else return 0;
}

void main() {
    int n, masa;
    scanf("%d %d", &n, &masa);
    int arr[100];
    for (int i = 0; i < n; i++) {
        scanf("%d", &arr[i]);
    }
    int res = weight(arr, masa, n, 0);
    if (res == 1) {
        printf("YES");
    } else {
        printf("NO");
    }
}