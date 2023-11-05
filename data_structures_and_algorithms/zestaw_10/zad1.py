# algorytmo opiera się na zbudowaniu grafu implikacji
# na podstawie klauzul
# następnie znalezienie silnie spójnych składowych za pomocą 
# algorytmu Kosaraju, jeżeli x oraz ~x znajdują się w tej samej SCC,
# wówczas formuła jest niespełnialna
# sortujemy silnie spójne składowe topologicznie i nadajemy wartości 
# zgodnie z porządkiem topologicznym najpierw False, potem True
# (mamy gwarancję, że nie nastąpi True -> False)
# O(V+Es) 