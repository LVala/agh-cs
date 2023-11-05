#include <stdio.h>
#include <stdlib.h>

//does not work in some cases, dunno why

double dist(double** polygons, int ind, int a, int b)
{
    int x1 = polygons[ind][2*a];
    int y1 = polygons[ind][2*a+1];
    int x2 = polygons[ind][2*b];
    int y2 = polygons[ind][2*b+1];
    return (x1-x2)*(x1-x2) + (y1-y2)*(y1-y2);
}

int axes(double** polygons, int len, int ind)
{
    int res = 0;
    for (int i=0; i<len; i++)
    {
        int a = i, b = i+len;
        for (int j=0; j<len; j++)
        {
            if (dist(polygons, ind, a, (2*len+a-j)%(2*len)) != dist(polygons, ind, a, (2*len+a+j)%(2*len))) break;
            if (dist(polygons, ind, b, (2*len+a-j)%(2*len)) != dist(polygons, ind, b, (2*len+a+j)%(2*len))) break;
            if (j==len-1) res++;
        }
    }
    return res;
}

void main()
{
    int t;
    scanf("%d", &t);
    int* t_sizes = malloc(t*sizeof(int));
    double** polygons = malloc(t*sizeof(double*));
    for (int i=0; i<t; i++)
    {
        scanf("%d", &t_sizes[i]);
        polygons[i] = malloc(4*t_sizes[i]*sizeof(double));
        for (int j=0; j<t_sizes[i]; j++)
            scanf("%lf %lf", &polygons[i][4*j], &polygons[i][4*j+1]);
        for (int j=0; j<t_sizes[i]; j++)
        {
            polygons[i][4*j+2] = (polygons[i][4*j] + polygons[i][(4*j+4)%(4*t_sizes[i])])/2;
            polygons[i][4*j+3] = (polygons[i][4*j+1] + polygons[i][(4*j+5)%(4*t_sizes[i])])/2;
        }
    }
        
    int *res = malloc(t*sizeof(int));

    for (int i=0; i<t; i++)
        res[i] = axes(polygons, t_sizes[i], i);
    
    for (int i=0; i<t; i++)
        printf("%d\n", res[i]);

    for (int i=0; i<t; i++)
        free(polygons[i]);
    free(res);
    free(t_sizes);
    free(polygons);
}