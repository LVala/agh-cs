#include <stdio.h>
#include <stdlib.h>

int xor(int cur[], int arr[], int F[], int i)
{
    int a, b;
    int inp1 = arr[2*i];
    int inp2 = arr[2*i+1];
    if (inp1 < 0) a = cur[((-1)*inp1) - 1];
    else if (F[inp1] != -1) a = F[inp1];
    else a = xor(cur, arr, F, inp1);
    
    if (inp2 < 0) b = cur[((-1)*inp2) - 1];
    else if (F[inp2] != -1) b = F[inp2];
    else b = xor(cur, arr, F, inp2);

    F[i] = (a + b)%2;
    return F[i];
}

int is_smaller(int arr1[], int arr2[], int len)
{
    for (int i = 0; i < len; i++)
    {
        if (arr1[i] < arr2[i]) return 1;
        if (arr1[i] > arr2[i]) return 0;
    }
    return 1;
}

void add_1(int num[], int len)
{
    int rest = 1;
    for (int i = len-1; i >= 0; i--)
    {
        num[i] += rest;
        if (num[i] < 2) rest = 0;
        if (num[i] == 2)
        {
            num[i] = 0;
            rest = 1;
        }
    }
}

void get_net_polynomial(int arr[], int poly[], int n, int m, int exit)
{
    int *cur = (int *)malloc(n * sizeof(int));
    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < n; j++) cur[j] = 0;
        cur[i] = 1;
        int *F = (int *)malloc(m * sizeof(int));
        for (int j = 0; j < m; j++) F[j] = -1;
        poly[i] = xor(cur, arr, F, exit);
        free(F);
    }
    free(cur);
}

int poly_val(int poly[], int cur[], int n)
{
    int res = (poly[0]*cur[0] + poly[1]*cur[1])%2;
    for (int i = 2; i < n; i++)
    {
        res = (res + poly[i]*cur[i])%2;    
    }
    return res;
}

int net(int n, int l_bound[], int u_bound[], int poly[])
{
    int res = 0;
    while(is_smaller(l_bound, u_bound, n))
    {
        res += poly_val(poly, l_bound, n);
        add_1(l_bound, n);
    }
    return res;
}

void main()
{
    int n, m, exit;
    scanf("%d %d %d", &n, &m, &exit);
    exit--;

    int *arr = (int *)malloc(2 * m * sizeof(int));
    
    for (int i = 0; i < m; i++)
        scanf("%d %d", &arr[2*i], &arr[2*i+1]);
    for (int i = 0; i < m; i++)
    {
        if (arr[2*i] > 0) arr[2*i]--;
        if (arr[2*i+1] > 0) arr[2*i+1]--;
    }
    
    int *l_bound = (int *)malloc((n+1) * sizeof(int));
    int *u_bound = (int *)malloc((n+1) * sizeof(int));
    int *poly = (int *)malloc(n * sizeof(int));

    for (int i = 0; i < n; i++)
        scanf("%1d", &l_bound[i]);
    for (int i = 0; i < n; i++)
        scanf("%1d", &u_bound[i]);

    get_net_polynomial(arr, poly, n, m, exit);

    int res = net(n, l_bound, u_bound, poly);
    printf("%d", res);

    free(poly);
    free(arr);
    free(l_bound);
    free(u_bound);
}