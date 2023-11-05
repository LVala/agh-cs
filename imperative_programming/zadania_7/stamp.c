#include <stdio.h>
#include <stdlib.h>

int stamp_max(int n, int k, int l, int* T[], int* P[])
{
    int res = 0;
    for (int i = 0; i <= n-k; i++)
    {
        for (int j = 0; j <= n-l; j ++)
        {
            int temp_res = 0;
            for (int a = 0; a < k; a++)
            {
                for (int b = 0; b < l; b++)
                {
                    if (P[a][b] == 1) temp_res += T[i+a][j+b];
                }
            }
            if (temp_res > res) res = temp_res;
        }
    }
    return res;
}

void main()
{
    int n, k, l;
    scanf("%d %d %d", &n, &k, &l);
    
    int **T = (int **)malloc(n * sizeof(int *));
    for (int i = 0; i < n; i++)
        T[i] = (int *)malloc(n * sizeof(int));

    int **P = (int **)malloc(k * sizeof(int *));
    for (int i = 0; i < k; i++)
        P[i] = (int *)malloc(l * sizeof(int));

    for (int i =  0; i < n; i++)
        for (int j = 0; j < n; j++)
            scanf("%d", &T[i][j]);

    for (int i =  0; i < k; i++)
        for (int j = 0; j < l; j++)
            scanf("%d", &P[i][j]);

    int res = stamp_max(n, k, l, T, P);
    printf("%d", res);

    for (int i =  0; i < n; i++)
        free(T[i]);
    free(T);

    for (int i =  0; i < k; i++)
        free(P[i]);
    free(P);
}