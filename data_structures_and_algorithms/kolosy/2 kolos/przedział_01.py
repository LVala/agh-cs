#brzmi trochę dynamicznie, trochę zachłannie, idk
# f(i, j) = min ilość przedzialów potrzebna do zapełnianie przedziału (i,j)
# f(i, j) = min(f(i, k) + f(k+1, j))
# dla każdego przedziału w wejściu f(i,j) = 1
# szukane f(0,1)
# tylko to będzi słabe dla liczb nie całkowitych
# na upartego można przemnożyć wszystko o 10^x
# x w zależności od dokładności tych zakresów i jakoś będzie
# ale pewnie tu chodzi o jakiś zachłanny algorytm
