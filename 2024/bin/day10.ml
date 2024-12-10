open Core
open Common

let data = read_lines_from_stdin () |> List.map ~f:String.to_array |> List.to_array
let n = Array.length data
let m = Array.length data.(0)
let within_bounds (i, j) = 0 <= i && i < n && 0 <= j && j < m
let move (i, j) (di, dj) = i + di, j + dj

let neighbors point =
  [ -1, 0; 0, -1; 0, 1; 1, 0 ] |> List.map ~f:(move point) |> List.filter ~f:within_bounds
;;

let hash (i, j) = (i * (52 * 52)) + j
let target = String.to_array "0123456789"

module IntSet = Set.Make (Int)

let task1 =
  let rec check point k =
    let i, j = point in
    if not (Char.equal data.(i).(j) target.(k))
    then IntSet.empty
    else if Array.length target - 1 = k
    then IntSet.singleton (hash point)
    else
      neighbors point
      |> List.map ~f:(fun neighbor -> check neighbor (k + 1))
      |> List.fold ~init:IntSet.empty ~f:Set.union
  in
  let result = ref 0 in
  for i = 0 to n - 1 do
    for j = 0 to m - 1 do
      let point = i, j in
      result := !result + Set.length (check point 0)
    done
  done;
  !result
;;

Stdio.printf "Task 1: %d\n" task1

let task2 =
  let rec check point k =
    let i, j = point in
    if not (Char.equal data.(i).(j) target.(k))
    then 0
    else if Array.length target - 1 = k
    then 1
    else
      neighbors point
      |> List.map ~f:(fun neighbor -> check neighbor (k + 1))
      |> List.fold ~init:0 ~f:( + )
  in
  let result = ref 0 in
  for i = 0 to n - 1 do
    for j = 0 to m - 1 do
      let point = i, j in
      result := !result + check point 0
    done
  done;
  !result
;;

Stdio.printf "Task 2: %d\n" task2
