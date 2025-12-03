import Data.List
import Data.Maybe
import Text.Printf

slice :: [a] -> Int -> Int -> [a]
slice xs from to = take (to - from) (drop from xs)

maxJoltage :: String -> [Char] -> Int -> Int -> Int
maxJoltage bank result since left =
  if left == 0
    then read result :: Int
    else
      let s = slice bank since (length bank - left + 1)
          maxSoFar = maximum s
          idx = fromJust $ elemIndex maxSoFar s
       in maxJoltage bank (result ++ [maxSoFar]) (since + idx + 1) (left - 1)

solve :: Int -> [String] -> Int
solve expectedLength banks =
  let poweredBanks = map (\bank -> maxJoltage bank [] 0 expectedLength) banks
   in sum poweredBanks

main :: IO ()
main = do
  content <- readFile "example01.txt"
  let banks = lines content
      t1 = solve 2 banks
      t2 = solve 12 banks
   in do
        printf "Task 1: %d\n" t1
        printf "Task 2: %d\n" t2
