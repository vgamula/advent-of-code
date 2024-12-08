open Core
open Common

let data = read_lines_from_stdin () |> List.to_array |> Array.map ~f:String.to_array
let n = Array.length data
let m = Array.length data.(0)
let antennas = Hashtbl.create (module Char)

module Point = struct
  type t = int * int

  let compare (x1, y1) (x2, y2) =
    match Int.compare x1 x2 with
    | 0 -> Int.compare y1 y2
    | c -> c
  ;;
end

let track_antenna_position (c : char) (position : Point.t) =
  Hashtbl.update antennas c ~f:(function
    | None -> [ position ]
    | Some positions -> position :: positions)
;;

for i = 0 to n - 1 do
  for j = 0 to m - 1 do
    if not (Char.equal data.(i).(j) '.') then track_antenna_position data.(i).(j) (i, j)
  done
done

let move (x, y) (dx, dy) = x + dx, y + dy
let within_bounds (x, y) = 0 <= x && x < n && 0 <= y && y < m

let task1 =
  let antenna_types = Hashtbl.keys antennas in
  List.map antenna_types ~f:(fun antenna_type ->
    let positions = Hashtbl.find_exn antennas antenna_type |> List.to_array in
    Array.sort positions ~compare:Point.compare;
    let count = Array.length positions in
    let visited = ref [] in
    let check_antinode current_position diff_vector =
      let next_position = move current_position diff_vector in
      if within_bounds next_position then [ next_position ] else []
    in
    for i = 0 to count - 2 do
      let a = positions.(i) in
      for j = i + 1 to count - 1 do
        let b = positions.(j) in
        let di, dj = fst b - fst a, snd b - snd a in
        visited := !visited @ check_antinode a (-di, -dj) @ check_antinode b (di, dj)
      done
    done;
    !visited)
  |> List.concat
  |> List.dedup_and_sort ~compare:Point.compare
  |> List.length
;;

Stdio.printf "Task 1: %d\n" task1

let task2 =
  let antenna_types = Hashtbl.keys antennas in
  List.map antenna_types ~f:(fun antenna_type ->
    let positions = Hashtbl.find_exn antennas antenna_type |> List.to_array in
    Array.sort positions ~compare:Point.compare;
    let count = Array.length positions in
    let visited = ref [] in
    let rec find_all_antinodes current_position diff_vector =
      let next_position = move current_position diff_vector in
      if within_bounds next_position
      then next_position :: find_all_antinodes next_position diff_vector
      else []
    in
    for i = 0 to count - 2 do
      let a = positions.(i) in
      for j = i + 1 to count - 1 do
        let b = positions.(j) in
        let di, dj = fst b - fst a, snd b - snd a in
        visited
        := !visited
           @ find_all_antinodes a (-di, -dj)
           @ find_all_antinodes a (di, dj)
           @ find_all_antinodes b (-di, -dj)
           @ find_all_antinodes b (di, dj)
      done
    done;
    !visited)
  |> List.concat
  |> List.dedup_and_sort ~compare:Point.compare
  |> List.length
;;

Stdio.printf "Task 2: %d\n" task2
