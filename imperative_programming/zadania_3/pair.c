#include <stdio.h>
#include <stdlib.h>

int compare_ints(const void *p, const void *q) {
    int x = *(const int *)p;
    int y = *(const int *)q;
    if (x < y)
        return -1;
    else if (x > y)
        return 1;

    return 0;
}

int check(int arr[], int n, int i, int k) {
    int l = i-1, r = i+1;
    while (l >= 0 && arr[l] == arr[i]) l--;
    while (l < n && arr[r] == arr[i]) r++;
    if (l >= 0 && arr[l] >= arr[i] - k) return r-l-1;
    if (r < n && arr[r] <= arr[i] + k) return r-l-1;
    return 0;
}

int pair(int arr[], int n, int k) {
    int i = 0;
    int res = 0;
    while (i < n) {
        if (i+1 < n && arr[i+1] == arr[i]) {
            i++;
        } else {
            int temp = check(arr, n, i, k);
            res += temp;
            i++;
        }
    } 
    return res;
}

void main() {
    int n,k;
    scanf("%d %d", &n, &k);
    
    int* arr = (int*) malloc(n * sizeof(int));
    for (int i = 0; i < n; i++) {
        scanf("%d", &arr[i]);
    }

    qsort(arr, n, sizeof(int), compare_ints);

    int res = pair(arr, n, k);
    
    free(arr);
    printf("%d", res);
}