open Core
open Common

let data =
  read_lines_from_stdin ()
  |> List.map ~f:(fun s ->
    let parts = String.split s ~on:':' in
    let nums =
      List.nth_exn parts 1
      |> String.strip
      |> String.split ~on:' '
      |> List.map ~f:String.strip
      |> List.map ~f:Int.of_string
      |> List.to_array
    in
    Int.of_string (List.nth_exn parts 0), nums)
;;

let task1 =
  let rec go target nums idx current_sum =
    if current_sum > target
    then false
    else if idx = Array.length nums
    then current_sum = target
    else
      go target nums (idx + 1) (current_sum + nums.(idx))
      || go target nums (idx + 1) (current_sum * nums.(idx))
  in
  data
  |> List.filter_map ~f:(fun (target, nums) ->
    if go target nums 0 0 then Some target else None)
  |> List.fold ~f:( + ) ~init:0
;;

Stdio.printf "Task 1: %d\n" task1

let task2 =
  let rec go target nums idx current_sum =
    if current_sum > target
    then false
    else if idx = Array.length nums
    then current_sum = target
    else
      go target nums (idx + 1) (current_sum + nums.(idx))
      || go target nums (idx + 1) (current_sum * nums.(idx))
      || go
           target
           nums
           (idx + 1)
           (Int.of_string (Printf.sprintf "%d%d" current_sum nums.(idx)))
  in
  data
  |> List.filter_map ~f:(fun (target, nums) ->
    if go target nums 0 0 then Some target else None)
  |> List.fold ~f:( + ) ~init:0
;;

Stdio.printf "Task 2: %d\n" task2
