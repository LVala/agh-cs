#include <stdio.h>
#include <stdlib.h>

int triangles(int n, int *arr[])
{
    int count = 0;
    for (int i=0; i < n; i++)
    {
        for (int j = i + 1; j < n; j++)
        {
            for (int k = j + 1; k < n; k++)
            {
                if (arr[i][j] == arr[i][k] && arr[i][j] == arr[j][k]) count++;
            }
        }
    }
    return count;
}

void main()
{
    int n, m, a, b;
    scanf("%d %d", &n, &m);

    int **arr = (int **)malloc(n * sizeof(int *));
    for (int i = 0; i < n; i++)
        arr[i] = (int *)calloc(n, sizeof(int));

    for (int i = 0; i < m; i++)
    {
        scanf("%d %d", &a, &b);
        arr[a-1][b-1] = 1;
    }

    int res = triangles(n, arr);
    printf("%d", res);

    for (int i = 0; i < n; i++)
        free(arr[i]);
    free(arr);
}