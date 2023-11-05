#include <stdio.h>

int find_field(int n, int arr[][100])
{
    int left[100] = {0};
    int right[100];
    for (int i = 0; i < n; i++) right[i] = n;
    int height[100] = {0};
    int maxarea = 0;
    for (int i = 0; i < n; i++) 
    {
        int cur_left = 0, cur_right = n;
        for (int j = 0; j < n; j++)
        {
            if (arr[i][j] == 0) height[j]++;
            else height[j] = 0;
        }
        for (int j = 0; j < n; j++)
        {
            if (arr[i][j] == 0) 
            {
                if (left[j] < cur_left) left[j] = cur_left;
            } 
            else 
            {
                left[j] = 0;
                cur_left = j + 1;
            }
        }
        for (int j = n - 1; j >= 0; j--)
        {
            if (arr[i][j] == 0)
            {
                if (right[j] > cur_right) right[j] = cur_right;
            }
            else
            {
                right[j] = n;
                cur_right = j;
            }
        }
        for (int j = 0; j < n; j++)
        {
            if ( height[j]*(right[j] - left[j]) > maxarea)
            {
                maxarea = height[j]*(right[j] - left[j]);
            }
        }
    }
    return maxarea;
}

void main() 
{
    int n;
    int arr[100][100];
    scanf("%d", &n);
    for (int i = 0; i < n; i++) 
    {
        for (int j = 0; j < n; j++) 
        {
            scanf("%d", &arr[i][j]);
        }
    }
    int res = find_field(n, arr);
    printf("%d", res);
}