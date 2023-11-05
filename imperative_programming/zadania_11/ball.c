#include <stdio.h>
#include <stdlib.h>
#include <limits.h>

int get_sum(int** boxes, int* valid, int n)
{
    int res = 0;
    for (int i=0; i<n; i++)
        for (int j=0; j<3; j++)
            if (valid[i] != j) res += boxes[j][i];
    return res;
}

int ball(int** boxes, int n)
{
    int res = INT_MAX;
    int* valid = calloc(n, sizeof(int));
    int count[3] = {0};
    int exist[3] = {0};
    for (int i=0; i<n; i++)
    {
        for (int j=0; j<3; j++)
        {
            if (boxes[j][i] != 0) exist[j] = 1;
            if (boxes[j][i] > boxes[valid[i]][i] ||
            (boxes[j][i] == boxes[valid[i]][i] && count[j] < count[valid[i]])) valid[i] = j;
        }
        count[valid[i]]++;
    }

    int temp_count = exist[0] + exist[1] + exist[2];
    if (n == 1)
    {
        if (temp_count < 2)
        {
            free(valid);
            return 0;
        } else
        {
            free(valid);
            return -1;
        }
    }
    if (n == 2)
    {
        if (temp_count < 3)
        {
            res = get_sum(boxes, valid, n);
            free(valid);
            return res;
        } else
        {
            free(valid);
            return -1;
        }
    }

    if (count[0] != 0 && count[1] != 0 && count[2] != 0)
    {
        res = get_sum(boxes, valid, n);
        free(valid);
        return res;
    }

    int max_count = 0;
    for (int i=0; i<3; i++)
        if (count[i] > count[max_count]) max_count = i;
    
    int a = (max_count+1)%3;
    int b = (max_count+2)%3;

    if (count[a] < 2 && count[b] < 2)
    {
        for (int i=0; i<n; i++)
        {
            for (int j=0; j<n; j++)
            {
                if (i != j)
                {
                    int temp1 = valid[i];
                    int temp2 = valid[j];
                    valid[i] = a;
                    valid[j] = b;
                    int temp_res = get_sum(boxes, valid, n);
                    if (temp_res < res) res = temp_res;
                    valid[i] = temp1;
                    valid[j] = temp2;
                }
            }
        }
        free(valid);
        return res;
    }

    if (count[b] == 0) a = b;
    for (int i=0; i<n; i++)
    {
        int temp1 = valid[i];
        valid[i] = a;
        int temp_res = get_sum(boxes, valid, n);
        if (temp_res < res) res = temp_res;
        valid[i] = temp1;
    }
    free(valid);
    return res;
}


void main()
{
    int n;
    scanf("%d", &n);
    
    int** boxes = malloc(3*sizeof(int*));
    for (int i=0; i<3; i++)
        boxes[i] = malloc(n*sizeof(int));

    for (int i=0; i<3; i++)
        for (int j=0; j<n; j++)
            scanf("%d", &boxes[i][j]);

    int res = ball(boxes, n);
    printf("%d", res);

    for (int i=0; i<3; i++)
        free(boxes[i]);
    free(boxes);
}