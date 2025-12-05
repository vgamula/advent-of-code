import gleam/int
import gleam/io
import gleam/list
import gleam/order
import gleam/result
import gleam/string
import simplifile

type Ingredient =
  Int

type Range {
  Range(start: Ingredient, end: Ingredient)
}

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
      Range(start: a, end: b)
    })
  let assert Ok(ingredients) =
    ingredients_str
    |> string.split(on: "\n")
    |> list.map(int.parse)
    |> result.all
  #(ranges, ingredients)
}

fn merge_sorted_ranges(merged: List(Range), rest: List(Range)) -> List(Range) {
  case merged, rest {
    _, [] -> list.reverse(merged)
    [], [rh, ..rt] -> merge_sorted_ranges([rh], rt)
    [mh, ..mt], [rh, ..rt] -> {
      case rh.start <= mh.end {
        True ->
          merge_sorted_ranges(
            [Range(start: mh.start, end: int.max(mh.end, rh.end)), ..mt],
            rt,
          )
        False -> merge_sorted_ranges([rh, ..merged], rt)
      }
    }
  }
}

fn merge_ranges(ranges: List(Range)) -> List(Range) {
  let sorted_ranges =
    list.sort(ranges, fn(a, b) {
      case int.compare(a.start, b.start) {
        order.Eq -> int.compare(a.end, b.end)
        x -> x
      }
    })
  merge_sorted_ranges([], sorted_ranges)
}

fn count_valid_ingredients(
  ranges: List(Range),
  ingredients: List(Ingredient),
) -> Int {
  ingredients
  |> list.count(fn(ingredient) {
    ranges |> list.any(fn(a) { a.start <= ingredient && ingredient <= a.end })
  })
}

fn total_possible_valid_ingredients(ranges: List(Range)) -> Int {
  list.map(ranges, fn(x) { x.end - x.start + 1 }) |> int.sum
}

pub fn main() -> Nil {
  let assert Ok(content) = simplifile.read("example01.txt")
  let #(ranges, ingredients) = parse_input(content)
  let ranges = merge_ranges(ranges)
  io.println(
    "Task 1: " <> int.to_string(count_valid_ingredients(ranges, ingredients)),
  )
  io.println(
    "Task 2: " <> int.to_string(total_possible_valid_ingredients(ranges)),
  )
}
