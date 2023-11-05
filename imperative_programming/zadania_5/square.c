#include <stdio.h>
#include <stdlib.h>

int count_squares(int n, int k, int *arr[], int *cords[])
{
    int c_num = 0;

    for (int i = 1; i < n-1; i++)
    {
        for (int j = 1; j < n-1; j++)
        {
            int m = 1;
            while (i - m >= 0 && i + m < n && j - m >= 0 && j + m < n)
            {
                int temp_sum = 0;
                for (int a = j - m; a <= j + m; a++)
                {
                    temp_sum += arr[i+m][a];
                    temp_sum += arr[i-m][a];
                }
                for (int a = i - m + 1; a < i + m; a++)
                {
                    temp_sum += arr[a][j-m];
                    temp_sum += arr[a][j+m];
                }
                if (temp_sum == k)
                {
                    cords[c_num][0] = i;
                    cords[c_num][1] = j;
                    c_num++;
                }
                m++;
            }
        }
    }
    return c_num;
}


void main()
{
    int n, k;
    scanf("%d %d", &n, &k);

    int **arr = (int **)malloc(n * sizeof(int *));
    for (int i = 0; i < n; i++)
        arr[i] = (int *)malloc(n * sizeof(int));
    
    int **cords = (int **)malloc(n * sizeof(int *));
    for (int i = 0; i < n; i++)
        cords[i] = (int *)malloc(2 * sizeof(int));
    
    for (int i = 0; i < n; i++) 
    {
        for (int j = 0; j < n; j++) 
        {
            scanf("%d", &arr[i][j]);
        }
    }

    int res = count_squares(n, k, arr, cords);
    printf("%d\n", res);

    for (int i = 0; i < res; i++)
    {
        printf("%d %d\n", cords[i][0], cords[i][1]);
    }

    for (int i = 0; i < n; i++)
    {
        free(arr[i]);
    }
    free(arr);
}
