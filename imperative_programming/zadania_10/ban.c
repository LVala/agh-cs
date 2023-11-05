#include <stdio.h>
#include <string.h>

int div_2(int num[], int len)
{
    int rest = 0;
    int new_rest;
    for (int i = 0; i < len; i++)
    {
        new_rest = (num[i] + rest * 10) % 2;
        num[i] = (num[i] + rest * 10) / 2;
        rest = new_rest;
    }
    return rest;
}

void add_1(int num[], int len)
{
    int rest = 1;
    int i = len - 1;
    while (i >= 0 && rest == 1)
    {
        num[i] += 1;
        num[i] = num[i] % 10;
        if (num[i] != 0) rest = 0;
    }
}

int mod(int num[], int len)
{   
    if (num[len-1]%2==1) return 1;
    else return 0;
}

int is_0(int num[], int len)
{
    for (int i = 0; i < len; i++)
        if (num[i] != 0) return 0;
    return 1;
}

int ban(int res[], int num[], int len, int m)
{
    int i = 0;
    while (i < 100 && is_0(num, len) == 0)
    {
        res[i] = mod(num, len);
        if (i%2==m && res[i] == 1) add_1(num, len);
        div_2(num, len);
        i++;
    }

    if (is_0(num, len) == 0) return 0;
    else return 1;
}

void main()
{
    char arr[35];
    scanf("%s", arr);
    
    int len = strlen(arr);
    int num1[35];
    int num2[35];
    for (int i = 0; i < len;i++)
    {
        num1[i] = arr[i] - '0';
        num2[i] = arr[i] - '0';
    }

    int res1[100] = {0};
    int res2[100] = {0};

    int is_valid1 = ban(res1, num1, len, 1);
    int is_valid2 = ban(res2, num2, len, 0);
    
    if (is_valid1 == 1)
    {
        for (int j = 0; j < 100 ; j++)
            if (res1[j] == 1) printf("%d ", j);
    } else printf("NO");
    printf("\n");
    if (is_valid2 == 1)
    {
        for (int j = 0; j < 100 ; j++)
            if (res2[j] == 1) printf("%d ", j);
    } else printf("NO");
}