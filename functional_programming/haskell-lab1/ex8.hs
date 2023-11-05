not' :: Bool -> Bool
not' b = case b of
          True  -> False
          False -> True

absInt n =
 case (n >= 0) of
   True -> n
   _    -> -n