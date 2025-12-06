import std/assertions
import std/sequtils
import std/strutils
import std/re
import std/sugar

type operator = (int, int) -> int

proc parseOperator(op: string): operator =
  if op == "*":
    (
      proc(a, b: int): int =
        a * b
    )
  elif op == "+":
    (
      proc(a, b: int): int =
        a + b
    )
  else:
    raiseAssert("should not happen")

proc task1(nums_list: seq[string], operators: seq[operator]): int =
  let data = nums_list.map(nums => nums.findAll(re"\d+").map(parseInt))

  for j in 0 .. operators.high:
    var tmp: seq[int] = @[]
    for i in 0 .. data.high:
      tmp.add(data[i][j])

    result += tmp.foldl(operators[j](a, b))

proc transform[T](s: seq[seq[T]]): seq[seq[T]] =
  result = newSeq[seq[T]](s[0].len)
  for i in 0 .. s[0].high:
    result[i] = newSeq[T](s.len)
    for j in 0 .. s.high:
      result[i][s.high - j] = s[s.high - j][i]

proc task2(data: seq[string], operators: seq[operator]): int =
  let nums = transform(data.map(a => toSeq(a.items))).map(a => a.join("").strip())

  var grouped_nums: seq[seq[int]] = @[@[]]
  for num in nums:
    if num == "":
      grouped_nums.add(@[])
    else:
      grouped_nums[^1].add(parseInt(num))

  assert(grouped_nums.len == operators.len)

  for _, (fn, nums) in zip(operators, grouped_nums):
    result += nums.foldl(fn(a, b))

let
  file_contents = readFile("example01.txt")
  lines = file_contents.split("\n")
  nums = lines[0 ..^ 2]
  operators = findAll(lines[^1], re"\+|\*").map(parseOperator)

echo "Task 1: ", task1(nums, operators)
echo "Task 2: ", task2(nums, operators)
