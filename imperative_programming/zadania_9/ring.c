#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>

int is_prime(int n) 
{
    if (n == 2) return 1;
    if (n % 2 == 0 || n < 2) return 0;
    int p = sqrt(n);
    for (int i = 3; i <= p; i += 2) 
    {
        if (n % i == 0) return 0;
    }
    return 1;
}

int scmp(const char *str1, const char *str2)
{
    for(;*str1 && *str2;str1++,str2++)
    {
        if(*str1<*str2)return -1;
        if(*str1>*str2)return 1;
    }
    if(*str1 && ! *str2) return 1; // aX > a
    if(!*str1 && *str2) return -1; // a < aX
    return 0;
}

int find_min(char str[],int j,int len)
{
    char min = str[(j+2)%len];
    for (int i = 1; i < len; i++)
    {
        if (str[(j+i)%len] < min && is_prime(i)) 
        min = str[(j+i)%len];
    }
    return min;
}

void get_str(char str[], char res[], char temp[], int len, int n, int p, int j)
{
    if (n == len)
    {
        if (scmp(temp, res) == -1)
        {
            strcpy(res, temp);
        }
        return;
    }
    temp[n] = str[j];
    if (p != -1)
    {
        get_str(str, res, temp, len, n+1, p, (j + p)%len);
        return;
    }
    char min = find_min(str, j, len);

    for (int i = 1; i < len; i++)
    {
        if (str[(j+i)%len] == min && is_prime(i))
        {
            get_str(str, res, temp, len, n+1, i, (j+i)%len);
        }
    }
}

void main()
{
    char str[51];
    scanf("%s", str);
    char res[51];
    char temp[51];
    strcpy(res, str);
    int len = strlen(str);
    temp[len] = '\0';
    
    char min = str[0];
    for (int i = 1; i < len; i++)
    {
        if (str[i] < min) 
        {
            min = str[i];
        }
    }

    for (int i = 0; i < len; i++)
    {
        if (str[i] == min)
        {
            get_str(str, res, temp, len, 0, -1, i);
        }
    }
    
    printf("%s", res);
}