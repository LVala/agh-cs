#include <stdio.h>
#include <stdlib.h>

void int_2_bin(int arr[], int n, int m)
{
    for (int i = 0; i < n; i++)
    {
        arr[i] = m%2;
        m = m/2;
    }
}

int gra(int arr[], int n, int g)
{
    int *num = (int *)malloc(30 * sizeof(int));
    int **temp = (int **)malloc(n * sizeof(int *));
    for (int i = 0; i < n; i++)
        temp[i] = (int *)malloc(30 * sizeof(int));

    int_2_bin(num, 30, g);
    for (int i = 0; i < n; i++)
    {
        int_2_bin(temp[i], 30, arr[i]);
    }

    for (int i = 0; i < 30; i++)
    {
        if (num[i] == 0)
        {
            for (int j = 0; j  < n; j++)
            {
                if (temp[j][i] == 1) arr[j] = -1;
            }
        }
    }

    int res = n;
    for (int i = 0; i < 30; i++)
    {
        if (num[i] == 1)
        {
            int temp_res = 0;
            for (int j = 0; j  < n; j++)
            {
                if (temp[j][i] == 1 && arr[j] != -1) temp_res++;
            }
            if (temp_res == 0) return 0;
            if (temp_res < res) res = temp_res;
        }
    }

    for (int i = 0; i < n; i++)
        free(temp[i]);
    free(temp);

    return res;
}

void main()
{
    int n, g;
    scanf("%d %d", &n, &g);
    int *arr = (int *)malloc(n * sizeof(int));
    for (int i = 0; i < n; i++)
        scanf("%d", &arr[i]);

    int res = gra(arr, n, g);
    printf("%d", res);
    free(arr);
}