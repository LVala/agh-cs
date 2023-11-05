sgn :: Int -> Int 
sgn n = 
    if n < 0
    then -1
    else if n == 0
        then 0
        else 1
