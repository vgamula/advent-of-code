open Core
open Common

let nums =
  read_lines_from_stdin ()
  |> List.hd_exn
  |> String.split ~on:' '
  |> List.map ~f:Int.of_string
;;

let split_number num =
  let num_digits = Float.to_int (Float.log10 (Float.of_int num)) + 1 in
  if num_digits mod 2 = 0
  then (
    let div = Int.pow 10 (num_digits / 2) in
    let left = num / div in
    let right = num mod div in
    Some (left, right))
  else None
;;

let solve n =
  let add_stone ~stone ~times map =
    Map.update map stone ~f:(function
      | None -> times
      | Some v -> v + times)
  in
  let rec iterate counter n =
    if n = 0
    then Map.data counter |> List.fold ~init:0 ~f:( + )
    else (
      let next_counter =
        Map.fold
          counter
          ~init:(Map.empty (module Int))
          ~f:(fun ~key:num ~data:times tmp_counter ->
            if num = 0
            then add_stone ~stone:1 ~times tmp_counter
            else (
              match split_number num with
              | Some (left, right) ->
                tmp_counter
                |> add_stone ~stone:left ~times
                |> add_stone ~stone:right ~times
              | None -> add_stone ~stone:(num * 2024) ~times tmp_counter))
      in
      iterate next_counter (n - 1))
  in
  let counter =
    List.fold
      nums
      ~init:(Map.empty (module Int))
      ~f:(fun next_counter num -> add_stone ~stone:num ~times:1 next_counter)
  in
  iterate counter n
;;

Stdio.printf "Task 1: %d\n" @@ solve 25;;
Stdio.printf "Task 2: %d\n" @@ solve 75
