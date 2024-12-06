open Core
open Common

let data = read_lines_from_stdin () |> List.map ~f:String.to_array |> List.to_array
let n = Array.length data
let m = Array.length data.(0)

let start_i, start_j =
  let res = ref (0, 0) in
  for i = 0 to n - 1 do
    for j = 0 to m - 1 do
      if Char.equal data.(i).(j) '^' then res := i, j
    done
  done;
  !res
;;

type direction =
  | Up
  | Down
  | Right
  | Left

let next_direction = function
  | Up -> Right
  | Right -> Down
  | Down -> Left
  | Left -> Up
;;

let move (i, j) dir =
  match dir with
  | Up -> i - 1, j
  | Right -> i, j + 1
  | Down -> i + 1, j
  | Left -> i, j - 1
;;

let get (i, j) = data.(i).(j)

(* Not using Core's Set or Hash_set because of preprocessors dependency *)
module PointSet = Stdlib.Set.Make (struct
    type t = int * int

    let compare (x1, y1) (x2, y2) =
      match Int.compare x1 x2 with
      | 0 -> Int.compare y1 y2
      | c -> c
    ;;
  end)

let within_bounds (i, j) = 0 <= i && i < n && 0 <= j && j < m

let task1, all_visited_coords =
  let visited = ref PointSet.empty in
  let add_to_visited point = visited := PointSet.add point !visited in
  let current_position = ref (start_i, start_j) in
  let current_direction = ref Up in
  let running = ref true in
  add_to_visited !current_position;
  while !running do
    let next_position = move !current_position !current_direction in
    if not (within_bounds next_position)
    then running := false
    else if Char.equal (get next_position) '#'
    then current_direction := next_direction !current_direction
    else (
      current_position := next_position;
      add_to_visited !current_position)
  done;
  PointSet.cardinal !visited, !visited
;;

Stdio.printf "Task 1: %d\n" task1

module PointWithDirectionSet = Stdlib.Set.Make (struct
    type t = (int * int) * direction

    let compare ((i1, j1), d1) ((i2, j2), d2) =
      let dir_to_int = function
        | Up -> 1
        | Down -> 2
        | Right -> 3
        | Left -> 4
      in
      match Int.compare i1 i2 with
      | 0 ->
        (match Int.compare j1 j2 with
         | 0 -> compare (dir_to_int d1) (dir_to_int d2)
         | c -> c)
      | c -> c
    ;;
  end)

let task2 =
  let can_place_obstacle position =
    let original_i, original_j = position in
    let result = ref false in
    let visited = ref PointWithDirectionSet.empty in
    let add_to_visited p d = visited := PointWithDirectionSet.add (p, d) !visited in
    let has_already_seen p d = PointWithDirectionSet.mem (p, d) !visited in
    let current_position = ref (start_i, start_j) in
    let current_direction = ref Up in
    let running = ref true in
    data.(original_i).(original_j) <- '#';
    add_to_visited !current_position !current_direction;
    while !running do
      let next_position = move !current_position !current_direction in
      if not (within_bounds next_position)
      then running := false
      else if Char.equal (get next_position) '#'
      then current_direction := next_direction !current_direction
      else (
        current_position := next_position;
        if has_already_seen !current_position !current_direction
        then (
          result := true;
          running := false);
        add_to_visited !current_position !current_direction)
    done;
    data.(original_i).(original_j) <- '.';
    !result
  in
  all_visited_coords
  |> PointSet.to_list
  |> List.filter ~f:can_place_obstacle
  |> List.length
;;

Stdio.printf "Task 2: %d\n" task2
