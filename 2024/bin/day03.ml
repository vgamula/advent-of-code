open Core
open Common

let data = read_lines_from_stdin () |> String.concat

let perform_multiplication s =
  let number_pattern = Re.Pcre.regexp {|\d{1,3}|} in
  Re.matches number_pattern s |> List.map ~f:Int.of_string |> List.fold ~f:( * ) ~init:1
;;

let task1 =
  let pattern = Re.Pcre.regexp {|mul\(\d{1,3},\d{1,3}\)|} in
  Re.matches pattern data
  |> List.map ~f:perform_multiplication
  |> List.fold ~f:( + ) ~init:0
;;

Stdio.printf "Task 1: %d\n" task1

type accumulator =
  { mul_enabled : bool
  ; score : int
  }

let task2 =
  let pattern = Re.Pcre.regexp {|do\(\)|don't\(\)|mul\(\d{1,3},\d{1,3}\)|} in
  let result =
    Re.matches pattern data
    |> List.fold
         ~f:(fun acc x ->
           match x with
           | "do()" -> { acc with mul_enabled = true }
           | "don't()" -> { acc with mul_enabled = false }
           | mul_match ->
             if acc.mul_enabled
             then { acc with score = acc.score + perform_multiplication mul_match }
             else acc)
         ~init:{ mul_enabled = true; score = 0 }
  in
  result.score
;;

Stdio.printf "Task 2: %d\n" task2
