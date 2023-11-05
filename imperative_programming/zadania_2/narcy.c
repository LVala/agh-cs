#include <stdio.h>

int power(int a, int b) {
    int res = 1;
    for (int i = 0; i < b; i++) {
        res = res * a;
    }
    return res;
}

char int_to_char(int input) {
    if (input >= 0 && input <= 9) {
        char res = input + '0';
        return res;
    } else {
        char res = input - 10 + 'A';
        return res;
    }
}

int char_to_int(char input) {
    if (input >= '0' && input <= '9') {
        int res = input - '0';
        return res;
    } else {
        int res = input + 10 -'A';
        return res;
    }
}

void revstr(char str[], int len) {
    for (int i=0; i <len/2; i++) {
        char temp = str[i];
        str[i] = str[len-1-i];
        str[len-1-i] = temp;
    }
}

void dec2base(char res[], int base, int input, int len) {
    int i = 0;
    while (input > 0) {
        res[i++] = int_to_char(input % base);
        input /= base;
    }
    res[i] = '\0';
    revstr(res, len);
}

int is_narc(char arr[], int len, int i) {
    int sum = 0;
    for (int i = 0; i < len; i++) {
        int temp = char_to_int(arr[i]);
        sum += power(temp, len);
    }
    if (sum == i) return 1;
    else return 0;
}

void main() {
    int len, base, flag = 0;
    scanf("%d %d", &len, &base);
    char arr[9];
    
    for (int i = power(base, len-1); i < power(base, len); i++) {
        dec2base(arr, base, i, len);

        int temp = is_narc(arr, len, i);
        if (temp == 1) {
            flag = 1;
            for (int i=0; i<len; i++) {
            printf("%c", arr[i]);
            }
            printf(" ");
        }
    }
    if (flag != 1) {
        printf("NO");
    }
}