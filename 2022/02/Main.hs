import Data.List
import Data.Maybe

data Shape = Rock | Paper | Scissors deriving (Show, Eq)

data Result = Win | Loss | Draw deriving Show

strategyToShape :: String -> Shape
strategyToShape a =
  case a of
    "A" -> Rock
    "B" -> Paper
    "C" -> Scissors

roundResult :: Shape -> Shape -> Result
roundResult a b =
  case (a, b) of
    (Rock, Paper) -> Win
    (Paper, Scissors) -> Win
    (Scissors, Rock) -> Win
    _ -> if a == b then Draw else Loss

calculateRoundScore [a, b] =
  let selectedShapeScore =
        case b of
          Rock -> 1
          Paper -> 2
          Scissors -> 3
      roundScore =
        case roundResult a b of
          Win -> 6
          Draw -> 3
          Loss -> 0
  in selectedShapeScore + roundScore

neededShapeForResult :: Shape -> Result -> Shape
neededShapeForResult shape desiredResult =
  let priority = [Rock, Paper, Scissors]
      currentIndex = fromJust (elemIndex shape priority)
  in priority !! case desiredResult of
                  Win -> (currentIndex + 1) `mod` 3
                  Draw -> currentIndex
                  Loss -> (currentIndex + 2) `mod` 3

strategyForRound1 [a, b] =
  let aShape = strategyToShape a
      bShape = case b of
                 "X" -> Rock
                 "Y" -> Paper
                 "Z" -> Scissors
  in [aShape, bShape]

strategyForRound2 [a, b] =
  let aShape = strategyToShape a
      desiredResult =
        case b of
          "X" -> Loss
          "Y" -> Draw
          "Z" -> Win
  in [aShape, neededShapeForResult aShape desiredResult]

solver :: String -> ([String] -> [Shape]) -> Int
solver file bestStrategySelector =
  let strategies = map (bestStrategySelector . words) $ lines file
  in sum $ map calculateRoundScore strategies

main = do
  file <- readFile "input01.txt"
  putStrLn $ "Task 1: " ++ show (solver file strategyForRound1)
  putStrLn $ "Task 2: " ++ show (solver file strategyForRound2)
