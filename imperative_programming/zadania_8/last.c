#include <stdio.h>

long long is_valid(long long s)
{
    long long res = 0;
    while (s > 0)
    {
        res += s;
        s = s/10;
    }
    return res;
}

long long bin_search(long long s, long long l, long long r)
{
    long long temp;
    while (r-l > 1)
    {
        long long mid = l + (r-l)/2;
        temp = is_valid(mid);
        if (temp == s) return mid;
        else if (temp > s) r = mid;
        else l = mid;
    }
    return -1;
}

void main()
{
    long long s;
    scanf("%lld", &s);
    long long res = -1;

    res = bin_search(s, s/2, s+1);
    printf("%lld", res);
}