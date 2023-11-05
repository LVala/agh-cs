# tworzona jest kopia grafu, gdzie każdy wierzchołek z grafu bazowego
# reprezentowany jest przez dwa wierzchołki IN i OUT, gdzie out ma krawędzie
# wychodzące z wierzchołka bazowego, a in wchodząte. Wierzchołki in i out łączy krawędź o
# o wadze 1, inne krawędzie mają wagi inf
# wówczas na takim grafie wywołujemy max_flow i jego wynik to ilość wierzchołkowo 
# rozłącznych ścieżek (ponieważ in -> out ma wagę 1, to z jednego wierzchołka nie
# wychodzić kilka ścieżek)