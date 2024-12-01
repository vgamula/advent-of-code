open Core
open Common

let data =
  read_lines_from_stdin ()
  |> List.map ~f:(fun s ->
    String.split s ~on:' ' |> List.filter ~f:(fun s -> String.length s > 0))
  |> List.map ~f:(function
    | [ a; b ] -> Int.of_string a, Int.of_string b
    | _ -> failwith "Wrong input format")
;;

let first_column = List.map data ~f:fst
let second_column = List.map data ~f:snd

let task1 =
  let rec diff_sum a b =
    match a, b with
    | a :: aa, b :: bb -> (abs @@ (a - b)) + diff_sum aa bb
    | _ -> 0
  in
  let first_column_sorted = List.sort first_column ~compare:Int.compare in
  let second_column_sorted = List.sort second_column ~compare:Int.compare in
  diff_sum first_column_sorted second_column_sorted
;;

Stdio.printf "Task 1: %d\n" task1

let task2 =
  let freqs =
    List.fold
      second_column
      ~init:(Map.empty (module Int))
      ~f:(fun acc element ->
        Map.update acc element ~f:(function
          | None -> 1
          | Some count -> count + 1))
  in
  List.fold first_column ~init:0 ~f:(fun acc a ->
    let freq = Map.find freqs a |> Option.value ~default:0 in
    (freq * a) + acc)
;;

Stdio.printf "Task 2: %d\n" task2
