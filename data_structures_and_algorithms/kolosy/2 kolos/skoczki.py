# graf, gdzie wierzchołkami są skoczki
# a krawędzie pomiędzy nimi istnieją, jeżeli się wzajemnie szachują
# wtedy wystarczy sprawdzić, czy graf ma ścieżkę hamiltona
# można to zrobić jakimś DFSem zmodyfikowanym, który, dojdzie do liścia
# to sprawdza czy przeszedł przez wszystkie wierzchołki
# a gdy się cofa to je odznacza