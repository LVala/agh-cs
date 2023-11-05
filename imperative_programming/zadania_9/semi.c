#include <stdio.h>

int power(int a, int b)
{
    int res = 1;
    for (int i = 0; i < b; i++) 
        res *= a;
    return res;

}

void main()
{
    int n, m;
    scanf("%d %d", &n, &m);
    int res = 0;
    int zakres = power(2, n)-1;

    if (m==1)
    {
        printf("%d", 0);
        return;
    }
    
    for (int i = 1; i <= zakres; i++)
    {
        if (i%m==0) continue;
        for (int j = 0; j < n; j++)
        {
            int cos = i ^ (1 << j);
            if (cos != 0 && cos%m==0) 
            {
                res++;
                break;
            }
        }
    }

    printf("%d", res);
}