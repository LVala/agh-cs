#include <stdio.h>
#include <stdlib.h>

int max_seg(int n, int k, int* arr[])
{
    int res = 0;
    for (int i = 0; i < n; i++)
    {
        for(int j = 0; j < n; j++)
        {
            int res_col = 0, res_row = 0;
            int res_diag_l = 0, res_diag_r = 0;
            for (int m = 0; m < k; m++)
            {
                res_col += arr[(i+m)%n][j];
                res_row += arr[i][(j+m)%n];
                res_diag_r += arr[(i+m)%n][(j+m)%n];
                res_diag_l += arr[(i-m+n)%n][(j+m)%n];
            }
            if (res_col > res) res = res_col;
            if (res_row > res) res = res_row;
            if (res_diag_l > res) res = res_diag_l;
            if (res_diag_r > res) res = res_diag_r;
        }
    }
    return res;
}

void main()
{
    int n, k;
    scanf("%d %d", &n, &k);
    int **arr = (int **)malloc(n * sizeof(int *));
    
    for (int i = 0; i < n; i++)
        arr[i] = (int *)malloc(n * sizeof(int));
    
    for (int i =  0; i < n; i++)
        for (int j = 0; j < n; j++)
            scanf("%d", &arr[i][j]);

    int res;
    res = max_seg(n, k, arr);

    printf("%d", res);

    for (int i =  0; i < n; i++)
        free(arr[i]);
    free(arr);
}