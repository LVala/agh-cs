#include <stdio.h>
#include <stdlib.h>

int blk_num(int n, int *arr[], int board[][200]) 
{   
    int blk_count = 0;
    for (int i = 0; i < n; i++)
    {
        for (int k = arr[i][0] + 100; k < arr[i][2] + 100; k++)
        {
            for (int m = arr[i][1] + 100; m < arr[i][3] + 100; m++)
            {
                if (board[k][m] == 0)
                {
                    blk_count++;
                    board[k][m] = 1;
                } else
                {
                    blk_count--;
                    board[k][m] = 0;
                }
            }
        }
    }
    return blk_count;
}

void main()
{
    int n;
    scanf("%d", &n);
    
    int **arr = (int **)malloc(n * sizeof(int *));
    for (int i = 0; i < n; i++)
        arr[i] = (int *)calloc(4, sizeof(int));
    
    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < 4; j++)
            scanf("%d", &arr[i][j]);
    }

    int board[200][200] = {0};
    int res = blk_num(n, arr, board);
    printf("%d", res);

    for (int i = 0; i < n; i++)
        free(arr[i]);
    free(arr);
}