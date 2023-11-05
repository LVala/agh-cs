#include <stdio.h>

long long square(long long n)
{
    return n*n;
}

long long odd(long long n)
{
    if (n == 0) return 0;
    if (n%2==1)
    {
        return (square((n+1)/2) + odd(n/2));
    } else
    {
        return (square(n/2) + odd(n/2));
    }
}

void main()
{
    long long n;
    scanf("%lld", &n);

    long long res = odd(n);
    printf("%lld", res);
}