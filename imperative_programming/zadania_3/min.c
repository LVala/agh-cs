#include <stdio.h>
#include <stdlib.h>

void main() {
    int n,k;
    scanf("%d %d", &n, &k);
    
    int* arr = (int*) calloc(n, sizeof(int));
    for (int i = 0; i < n; i++) {
        scanf("%d", &arr[i]);
    }
    
    int res = 0, index = 0;
    for (int i = 0; i < k; i++) {
        res = index = 0;
        for (int j = 0; j < n; j++) {
            if (arr[j] > res) {
                res = arr[j];
                index = j;
            }
        }
        arr[index] = res / 2;
    }
    
    int suma = 0;
    for (int i = 0; i < n; i++) {
        suma += arr[i];
    }
    
    printf("%d", suma);
    free(arr);
}
