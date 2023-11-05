#include <stdio.h>
#include <stdlib.h>

void wPrawo(int i,int* arr)
{
    arr[i]--;
    arr[i+1]--;
    arr[i+2]++;
}

void wLewo(int i,int* arr)
{
    arr[i]--;
    arr[i-1]++;
    arr[i-2]++;
}


int main()
{
    unsigned int n;
    int move = 40;
    if(scanf("%d",&n) <= 0)
    {
        return 1;
    }
    int* tmp1 = malloc(sizeof(int)*n);
    int* tmp2 = malloc(sizeof(int)*n);
    for(int i = 0;i<n;i++) 
    {
        
        if(scanf("%d %d",&tmp1[i],&tmp2[i]) <= 0)
        {
            return 1;
        }
    }
    unsigned int m = (unsigned int) ( tmp1[n-1]+2*move );
    int* arr = calloc(m,sizeof(int));
    for(unsigned int i = 0;i < n;i++) arr[tmp1[i]+move] = tmp2[i];
    free(tmp1);
    free(tmp2);
    //Faza 1 - usuwanie wież o co najmnniej 3 pionkach
    int flag = 1;
    while(flag == 1)
    {
        flag = 0;
        for(int i = 0;i < m;i++)
        {
            while(arr[i] >= 3)//rozładowanie wieży
            {
                arr[i-2]++;
                arr[i] -= 3;
                arr[i+2]++;
                flag = 1;
            }
        }
    }
    //Faza 2 
    // pole := numer skrajnie prawego niepustego pola;
    int idx;
    for(unsigned int i = m-1;i >= 0;i--)
    {
        if(arr[i] != 0)
        {
            idx = (int) i;
            break;
        }
    }
    // pole := pole − 1;
    idx--;
    // while konfiguracja nie jest końcowa do
    flag = 1;
    while(flag)
    {    
        // case
        // pion(pole) > 0 i pion(pole + 1) > 0:
        if(arr[idx] > 0 && arr[idx+1] > 0)
        {
            // wykonaj ruch w prawo z pole;
            wPrawo(idx,arr);
            // pole := pole + 2;
            idx += 2;
        }
        // pion(pole) = 2 i pion(pole − 1) > 0:
        else if(arr[idx] == 2 && arr[idx-1] > 0)
        {
            // pole := pole − 1;
            idx--;
        }
            // pion(pole) = 2 i pion(pole + 1) = 0:
        else if(arr[idx] == 2 && arr[idx+1] == 0)
        {
            wLewo(idx,arr);
            wPrawo(idx-1,arr);
            idx++;
            //wykonaj ruch w lewo z pole;
            //wykonaj ruch w prawo z pole − 1;
            //pole := pole + 1;
        }
        else if(arr[idx] == 3)
        {
            //chyba działa
            arr[idx-2]++;
            arr[idx] -= 3;
            arr[idx+2]++;
            idx += 2;
            //pion(pole) = 3:
            // rozładuj pole;
            // pole := pole + 2
        }
        else
        {
            // pole jest numerem skrajnie lewego niepustego pola:
            // zakończ fazę 2.;
            // w pozostałych przypadkach:
            // pole := numer następnego niepustego pola z lewej;
            flag = 0;
            for(int i = idx-1;i>=0;i--)
            {
                if(arr[i] != 0)
                {
                    idx = i;
                    flag = 1;
                    break;
                }
            }
        }
    }
    for(int i = 0;i<m;i++) if(arr[i] != 0)printf("%d ",i-move);
    return 0;
}