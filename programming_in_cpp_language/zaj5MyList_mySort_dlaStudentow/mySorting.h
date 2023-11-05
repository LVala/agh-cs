#ifndef MY_SORTING_H
#define MY_SORTING_H

#include <iterator>
#include <array>
#include <vector>
#include <cstring>
#include <algorithm>
#include "myList.h"

template<typename T>
void mySort(T& container) {
    auto begin = std::begin(container);
    auto end = std::end(container);

    std::sort(begin, end);
}

template <typename T>
void mySort(MyList<T> &myList) {
    MyList<T> temp;
    
    while (myList.size() > 0) {
        temp.push_front(myList.pop_front());
    }

    while (temp.size() > 0) {
        myList.insert(temp.pop_front());
    }
}

template<size_t M>
int compareStrings(char s1[M], char s2[M]) {
    int i = 0;
    while (s1[i] && s2[i]) {
        if (std::tolower(s1[i]) < std::tolower(s2[i])) return 1;
        if (std::tolower(s1[i]) > std::tolower(s2[i])) return -1;
    }

    if (!s1[i] && !s2[i]) return 0;
    if (!s1[i]) return 1;
    else return -1;
}

template<size_t N, size_t M>
void mySort(char (&words)[N][M]) {
    char temp[M];
    for(int i=1; i<N; i++)
    {
        for(int j=0; j<N-i;j++)
        {
            int order = 0;
            for (int k=0; k<M; ++k) {
                if (std::tolower(words[j][k]) < std::tolower(words[j+1][k])) break;
                if (std::tolower(words[j][k]) > std::tolower(words[j+1][k])) {
                    order = 1;
                    break;
                }
            }


            if(order == 1)
            {
                for (int m=0;m<M; ++m) temp[m] = words[j][m];
                for (int m=0;m<M; ++m) words[j][m] = words[j+1][m];
                for (int m=0;m<M; ++m) words[j+1][m] = temp[m];
            }
        }
    }
}

#endif