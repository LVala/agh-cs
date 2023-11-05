#include <stdio.h>
#include <stdlib.h>

void main() {
    int n, r;
    int F[100][100];
    scanf("%d %d", &n, &r);
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            scanf("%d", &F[i][j]);
        }
    }

    int W[100][100];
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            W[i][j] = 0;
        }
    }

    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            if (F[i][j] == 1) {
                for (int x = i - r; x <= i + r; x++) {
                    for (int y = j - r; y <= j + r; y++) {
                        if (x >= 0 && x < n && y >= 0 && y <n) {
                            W[x][y]++;
                        }
                    }
                }
                
            }
        }
    }
    
    for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                printf("%d ", W[i][j]);
            }
            printf("\n");
        }

}
