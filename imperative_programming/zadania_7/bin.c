#include <stdio.h>
#include <stdlib.h>

int add_one(int n, int arr[], int* valid)
{
    int i = n-1;
    arr[i]++;
    while (arr[i] > 1)
    {
        if (i==0)
        {
            *valid = 0;
            return 0;
        }
        arr[i] = 0;
        arr[i-1]++;
        i--;
    }
    return 1;
}

int is_bad(int n, int arr[])
{
    for (int i = n-2; i >= 0; i--)
    {
        if (arr[i] == 1 && arr[i+1] == 1) return 1;
    }
    return 0;
}

void next_sqnc(int n, int arr[], int* valid)
{
    add_one(n, arr, valid);
    while (is_bad(n, arr)) add_one(n, arr, valid);
}

void main()
{
    int n, k;
    scanf("%d %d", &n, &k);
    int* arr = (int*) calloc(n, sizeof(int));

    int k_valid = 1;
    for (int j = 1; j < k; j++)
    {
        if (k_valid == 0) break;
        next_sqnc(n, arr, &k_valid);
    }
    
    if (k_valid == 0)
    {
        printf("%d", -1);
    } else
    {
        for (int i = 0; i < n; i++)
            printf("%d", arr[i]);
    }
    
    free(arr);
}