import Data.Char
import Data.List
import Data.Maybe
import Text.Printf

type Bank = [Int]

slice :: [a] -> Int -> Int -> [a]
slice xs from to = take (to - from) (drop from xs)

maxJoltage :: Bank -> Int -> Int -> Int -> Int
maxJoltage bank since left result =
  if left == 0
    then result
    else
      let s = slice bank since (length bank - left + 1)
          maxSoFar = maximum s
          idx = fromJust $ elemIndex maxSoFar s
       in maxJoltage bank (since + idx + 1) (left - 1) (result * 10 + maxSoFar)

totalOutput :: Int -> [Bank] -> Int
totalOutput cellsCount banks =
  let poweredBanks = map (\bank -> maxJoltage bank 0 cellsCount 0) banks
   in sum poweredBanks

main :: IO ()
main = do
  content <- readFile "example01.txt"
  let deserializeBank = map digitToInt
      banks = map deserializeBank $ lines content
      t1 = totalOutput 2 banks
      t2 = totalOutput 12 banks
   in do
        printf "Task 1: %d\n" t1
        printf "Task 2: %d\n" t2
