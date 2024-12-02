open Core
open Common

let data =
  read_lines_from_stdin ()
  |> List.map ~f:(fun s -> String.split s ~on:' ' |> List.map ~f:Int.of_string)
;;

let is_safe_report l =
  let is_safe l =
    List.for_all l ~f:(fun x -> 1 <= abs x && abs x <= 3)
    && (List.for_all l ~f:(fun x -> x < 0) || List.for_all l ~f:(fun x -> 0 < x))
  in
  let calculate_diffs l =
    let rec inner previous l =
      match l with
      | [ current ] -> [ previous - current ]
      | current :: next -> (previous - current) :: inner current next
      | _ -> []
    in
    match l with
    | current :: next -> inner current next
    | _ -> []
  in
  calculate_diffs l |> is_safe
;;

let task1 = data |> List.filter ~f:is_safe_report |> List.length;;

Stdio.printf "Task 1: %d\n" task1

let task2 =
  let generate_sublists l =
    List.init (List.length l) ~f:(( + ) 1)
    |> List.map ~f:(fun i -> List.filteri l ~f:(fun j _ -> i <> j + 1))
  in
  data
  |> List.map ~f:generate_sublists
  |> List.filter ~f:(List.exists ~f:is_safe_report)
  |> List.length
;;

Stdio.printf "Task 2: %d\n" task2
