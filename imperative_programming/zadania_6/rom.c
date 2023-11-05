#include <stdio.h>
#include <string.h>

char ROMS[4000][5];

void fill(char ROMS[][5])
{
    strcpy(ROMS[1], "I");
    strcpy(ROMS[2], "II");
    strcpy(ROMS[3], "III");
    strcpy(ROMS[4], "IV");
    strcpy(ROMS[5], "V");
    strcpy(ROMS[6], "VI");
    strcpy(ROMS[7], "VII");
    strcpy(ROMS[8], "VIII");
    strcpy(ROMS[9], "IX");
    strcpy(ROMS[10], "X");
    strcpy(ROMS[20], "XX");
    strcpy(ROMS[30], "XXX");
    strcpy(ROMS[40], "XL");
    strcpy(ROMS[50], "L");
    strcpy(ROMS[60], "LX");
    strcpy(ROMS[70], "LXX");
    strcpy(ROMS[80], "LXXX");
    strcpy(ROMS[90], "XC");
    strcpy(ROMS[100], "C");
    strcpy(ROMS[200], "CC");
    strcpy(ROMS[300], "CCC");
    strcpy(ROMS[400], "CD");
    strcpy(ROMS[500], "D");
    strcpy(ROMS[600], "DC");
    strcpy(ROMS[700], "DCC");
    strcpy(ROMS[800], "DCCC");
    strcpy(ROMS[900], "CM");
    strcpy(ROMS[1000], "M");
    strcpy(ROMS[2000], "MM");
    strcpy(ROMS[3000], "MMM");
}

void int_2_rom(int num)
{
    for (int i = 1000; i > 0; i = i/10)
    {
        if (num >= i)
        {
            int digit = num / i;
            printf("%s", ROMS[digit*i]);
            num = num % i;
        }
    }
    printf("\n");
}

int compare(char num[], int i)
{
    if (strncmp(num, ROMS[i], strlen(ROMS[i])) == 0)
    {
        char *p = num + strlen(ROMS[i]);
        strcpy(num, p);
        return i;
    }
    return 0;
}

int rom_2_int(char num[])
{
    int res = 0;
    for (int i = 3000; i >= 1000; i -= 1000)
    {
        res += compare(num, i);
    }
    for (int i = 900; i >= 100; i -= 100)
    {
        res += compare(num, i);
    }
    for (int i = 90; i >= 10; i -= 10)
    {
        res += compare(num, i);
    }
    for (int i = 9; i >= 1; i--)
    {
        res += compare(num, i);
    }
    return res;

}

void main()
{
    fill(ROMS);

    char num1[15], num2[15];
    scanf("%s %s", &num1, &num2);

    int int_num1 = rom_2_int(num1);
    int int_num2 = rom_2_int(num2);
    int int_res = int_num1 + int_num2;
    
    int_2_rom(int_res);
}