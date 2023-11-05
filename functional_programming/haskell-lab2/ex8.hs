isOdd :: (Ord a, Num a) => a -> Bool
isOdd n | n <= 0    = False
        | otherwise = isEven (n-1)

isEven :: (Ord a, Num a) => a -> Bool
isEven n | n < 0     = False
         | n == 0    = True
         | otherwise = isOdd (n-1)

ackerFun m n
 | m == 0    = n + 1
 | n == 0    = ackerFun (m - 1) 1
 | otherwise = ackerFun (m - 1) (ackerFun m (n - 1))