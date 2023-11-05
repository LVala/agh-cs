#include <stdio.h>

void main() {
    int n;
    int t1[100][100];
    
    scanf("%d", &n);
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n;j++) {
            scanf("%d", &t1[i][j]);
        }
    }
    
    int t2[10000];
    int arr[100] = {0};
    int k = 0;
    
    for (int i = 0; i < n*n; i++) {
        int min = 0;
        for (int j = 0; j < n; j++) {
            if (arr[min] >= n || (arr[j] < n && t1[j][arr[j]] < t1[min][arr[min]])) {
                min = j;
            }
        }
        if (k == 0 || t2[k-1] != t1[min][arr[min]]) {
            t2[k] = t1[min][arr[min]];
            k++;
        }
        arr[min]++;
    }

    for (int i = 0; i < k; i++) {
        printf("%d ", t2[i]);
    }
}
