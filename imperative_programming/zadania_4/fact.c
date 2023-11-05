#include <stdio.h>

void main() {
    int n;
    scanf("%d", &n);
    
    int arr[200] = {0};
    arr[0] = 1;
    
    for (int i = 2; i <= n; i++) {
        int temp = 0;
        for (int j = 0; j < 200; j++) {
            arr[j] *= i;
            arr[j] += temp;
            temp = arr[j] / 10;
            arr[j] = arr[j] % 10;
        }
    }

    int i = 199;
    while (arr[i] == 0) i--;

    for (int j = i; i >= 0; i--) {
        printf("%d", arr[i]);
    }

}