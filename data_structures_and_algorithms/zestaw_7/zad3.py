# W - waga jaką chcemy odmierzyć
# T - tablica z odważnikami
def max_weight(W, T):        
    T.sort(reverse=True)            # sortujemy elementy w T od max do min
    s = 0                           # s - ilosc odwaznikow uzyty przy pomiarze
    cp_W = W                        
 
    for i in range(len(T)):         # iterujemy po wszystkich odwaznikach              
        if T[i] <= W:
            s += 1                  
            W -= T[i]
    
    return cp_W - W, s              # zwracamy uzyskana wage oraz ilosc uzytych odwaznikow
