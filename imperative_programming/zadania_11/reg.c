#include <stdio.h>

void recur(char* res, char* temp, int* max_n, int s, int t, int n, int* flag)
{
    if (s == t)
    {
        if (n < *max_n)
        {
            for (int i=0; i<n; i++)
                res[i] = temp[i];
            *max_n = n;
            *flag = 1;

        }
        return;
    }
    if (s > t || s <= 0) return;

    if (s != 1 && s < 46342)
    {
        temp[n] = '*';
        recur(res, temp, max_n, s*s, t, n+1, flag);
    }

    if (s < 1073741830)
    {
        temp[n] = '+';
        recur(res, temp, max_n, 2*s, t, n+1, flag);
    }
}

void reg(char* res, char* temp, int* max_n, int s, int t, int* flag)
{ 
    recur(res, temp, max_n, s, t, 0, flag);

    temp[0] = '/';
    recur(res, temp, max_n, 1, t, 1, flag);
}

void main()
{
    int s, t;
    scanf("%d %d", &s, &t);

    int flag = 0;
    int max_n = 256;
    char res[256];
    char temp[256];
    reg(res, temp, &max_n, s, t, &flag);

    if (flag==0)
    {
        printf("NO");
    } else
    {
        for (int i=0; i<max_n; i++)
            printf("%c", res[i]);
    }
}