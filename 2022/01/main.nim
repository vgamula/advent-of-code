import std/algorithm
import std/sequtils
import std/strutils
import std/sugar


let
  file_contents = readFile("input01.txt")
  calories = file_contents.split("\n\n").map(x => x.split().map(y => parseInt(y)))
  calories_grouped = calories.map(x => x.foldl(a + b))


echo "Task 1: ", calories_grouped.max
echo "Task 2: ", sorted(calories_grouped, SortOrder.Descending)[0..2].foldl(a + b)
