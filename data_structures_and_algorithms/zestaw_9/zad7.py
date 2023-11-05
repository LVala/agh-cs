# bez implementacji, było na Bicie
# tworzymy dla każdego wierzcholka D nowych wierzcholków
# o własnościach (pozycja, paliwo), czyli nowy graf
# ma V*D, gdzie krawędz istnieje pomiędzy wierzchołkami
# jeżeli istniała krawędź w podstawowym grafie, pomiędzy wierzchołkami
# (x, paliwo) do (y, paliwo - d(x,y))  o wadze 0, oraz istnieją krawędzie
# (x,paliwo) do (x,paliwo + 1) o wadze kosztu paliwa za jednostkę
# oraz paliwo nie może przekroczyć pojemności baku pojazdu
# na tym dijkstra