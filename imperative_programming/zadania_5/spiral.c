#include <stdio.h>
#include <stdlib.h>

void fill_spiral(int n, int *arr[])
{
    int lczb = 1, x = 0, y = 0;
    while (lczb <= n*n)
    {
        while (y < n && arr[x][y] == 0)
        {
            arr[x][y] = lczb;
            lczb++;
            y++;
        }
        y--;
        x++;
        while (x < n && arr[x][y] == 0)
        {
            arr[x][y] = lczb;
            lczb++;
            x++;
        }
        x--;
        y--;
        while (y >= 0 && arr[x][y] == 0)
        {
            arr[x][y] = lczb;
            lczb++;
            y--;
        }
        y++;
        x--;
        while (x >= 0 && arr[x][y] == 0)
        {
            arr[x][y] = lczb;
            lczb++;
            x--;
        }
        x++;
        y++;
    }
}


void main()
{
    int n;
    scanf("%d", &n);

    int **arr = (int **)malloc(n * sizeof(int *));
    for (int i = 0; i < n; i++)
        arr[i] = (int *)calloc(n, sizeof(int));
    
    fill_spiral(n, arr);

    for (int i = 0; i < n; i++) 
    {
        for (int j = 0; j < n; j++)
        {
            printf("%d ", arr[i][j]);
        }
        printf("\n");
    }
    for (int i = 0; i < n; i++)
    {
        free(arr[i]);
    }
    free(arr);

}