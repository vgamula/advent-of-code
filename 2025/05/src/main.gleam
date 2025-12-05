import gleam/int
import gleam/io
import gleam/list
import gleam/order
import gleam/result
import gleam/string
import simplifile

type Ingredient =
  Int

type Range =
  #(Ingredient, Ingredient)

fn parse_input(content: String) -> #(List(Range), List(Ingredient)) {
  let content = string.trim(content)
  let assert Ok(#(ranges_str, ingredients_str)) =
    string.split_once(content, on: "\n\n")
  let ranges =
    ranges_str
    |> string.split("\n")
    |> list.map(fn(x) {
      let assert Ok(#(a, b)) = string.split_once(x, on: "-")
      let assert Ok(a) = int.parse(a)
      let assert Ok(b) = int.parse(b)
      #(a, b)
    })
  let assert Ok(ingredients) =
    ingredients_str |> string.split("\n") |> list.map(int.parse) |> result.all
  #(ranges, ingredients)
}

fn merge_sorted_ranges(merged: List(Range), rest: List(Range)) -> List(Range) {
  case merged, rest {
    _, [] -> list.reverse(merged)
    [], [rh, ..rt] -> merge_sorted_ranges([rh], rt)
    [mh, ..mt], [rh, ..rt] -> {
      case rh.0 <= mh.1 {
        True -> merge_sorted_ranges([#(mh.0, int.max(mh.1, rh.1)), ..mt], rt)
        False -> merge_sorted_ranges([rh, ..merged], rt)
      }
    }
  }
}

fn merge_ranges(ranges: List(Range)) -> List(Range) {
  let sorted_ranges =
    list.sort(ranges, fn(a, b) {
      case int.compare(a.0, b.0) {
        order.Eq -> int.compare(a.1, b.1)
        x -> x
      }
    })
  merge_sorted_ranges([], sorted_ranges)
}

fn task1(ranges: List(Range), ingredients: List(Ingredient)) -> Int {
  ingredients
  |> list.count(fn(ingredient) {
    ranges |> list.any(fn(a) { a.0 <= ingredient && ingredient <= a.1 })
  })
}

fn task2(ranges: List(Range)) -> Int {
  list.fold(ranges, 0, fn(acc, x) { acc + x.1 - x.0 + 1 })
}

pub fn main() -> Nil {
  let assert Ok(content) = simplifile.read("example01.txt")
  let #(ranges, ingredients) = parse_input(content)
  let ranges = merge_ranges(ranges)
  io.println("Task 1: " <> int.to_string(task1(ranges, ingredients)))
  io.println("Task 2: " <> int.to_string(task2(ranges)))
}
