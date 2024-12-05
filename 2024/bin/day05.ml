open Core
open Common

let lines =
  read_lines_from_stdin ()
  |> List.map ~f:String.strip
  |> List.filter ~f:(fun s -> not (String.is_empty s))
;;

let rules =
  lines
  |> List.filter ~f:(fun s -> String.contains s '|')
  |> List.map ~f:(fun s ->
    let parts = String.split s ~on:'|' in
    Int.of_string @@ List.nth_exn parts 0, Int.of_string @@ List.nth_exn parts 1)
;;

let add_to_map map (key : int) (value : int) =
  Map.update map key ~f:(function
    | None -> Set.singleton (module Int) value
    | Some set -> Set.add set value)
;;

let before, after =
  List.fold
    rules
    ~f:(fun (before, after) (a, b) -> add_to_map before b a, add_to_map after a b)
    ~init:(Map.empty (module Int), Map.empty (module Int))
;;

let updates =
  lines
  |> List.filter ~f:(fun s -> String.contains s ',')
  |> List.map ~f:(String.split ~on:',')
  |> List.map ~f:(List.map ~f:Int.of_string)
;;

let comparator a b =
  let includes tbl key1 key2 =
    match Map.find tbl key1 with
    | Some set -> Set.mem set key2
    | None -> false
  in
  if includes before b a && includes after a b then -1 else 1
;;

let task1 =
  updates
  |> List.filter ~f:(fun update ->
    let sorted = List.sort update ~compare:comparator in
    List.equal ( = ) update sorted)
  |> List.map ~f:(fun l -> List.nth_exn l (List.length l / 2))
  |> List.fold ~f:( + ) ~init:0
;;

Stdio.printf "Task 1: %d\n" task1

let task2 =
  updates
  |> List.filter_map ~f:(fun update ->
    let sorted = List.sort update ~compare:comparator in
    if not (List.equal ( = ) update sorted) then Some sorted else None)
  |> List.map ~f:(fun l -> List.nth_exn l (List.length l / 2))
  |> List.fold ~f:( + ) ~init:0
;;

Stdio.printf "Task 2: %d\n" task2
