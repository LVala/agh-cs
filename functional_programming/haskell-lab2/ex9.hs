qSort :: Ord a => [a] -> [a]
qSort []     = []
qSort (x:xs) = qSort (leftPart xs) ++ [x] ++ qSort (rightPart xs)
 where
   leftPart  xs = [ y | y <- xs, y <= x ]
   rightPart xs = [ y | y <- xs, y > x  ]