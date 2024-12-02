open Core
open Common

let data =
  read_lines_from_stdin ()
  |> List.map ~f:(fun s -> String.split s ~on:' ' |> List.map ~f:Int.of_string)
;;

let is_floor_report_safe l =
  let calculate_floor_diffs l =
    let rec inner previous l =
      match l with
      | current :: next -> (previous - current) :: inner current next
      | _ -> []
    in
    match l with
    | current :: next -> inner current next
    | _ -> []
  in
  let are_floor_diffs_acceptable l =
    List.for_all l ~f:(fun x -> 1 <= abs x && abs x <= 3)
    && (List.for_all l ~f:(( < ) 0) || List.for_all l ~f:(( > ) 0))
  in
  let diffs = calculate_floor_diffs l in
  are_floor_diffs_acceptable diffs
;;

let task1 = data |> List.count ~f:is_floor_report_safe;;

Stdio.printf "Task 1: %d\n" task1

let task2 =
  let generate_subreports l =
    List.init (List.length l) ~f:(( + ) 1)
    |> List.map ~f:(fun i -> List.filteri l ~f:(fun j _ -> i <> j + 1))
  in
  data
  |> List.map ~f:generate_subreports
  |> List.count ~f:(List.exists ~f:is_floor_report_safe)
;;

Stdio.printf "Task 2: %d\n" task2
