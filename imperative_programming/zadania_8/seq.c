#include <stdio.h>
#include <string.h>

int cmpchr(char char1, char char2)
{
    if (char1 < char2) return -1;
    if (char1 > char2) return 1;
    return 0;
}

void seq(char *str, char *res, int len)
{
    int ind = 0;
    while (ind < len)
    {
        char max[2] = {str[ind], '\0'};
        int max_ind = ind;
        for (int i = ind; i < len; i++)
        {
            if (cmpchr(str[i], max[0]) == 1)
            {
                max[0] = str[i];
                max_ind = i;
            }
        }
        strcat(res, max);
        ind = max_ind + 1;
    }
}

void main()
{
    char str[51];
    scanf("%s", str);   
   
    int len = strlen(str);
    char res[51] = {""};

    seq(str, res, len);
    
    printf("%s", res);
}