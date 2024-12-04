open Core
open Common

let lines = read_lines_from_stdin () |> List.to_array |> Array.map ~f:String.to_array
let n = Array.length lines
let m = Array.length lines.(0)

let task1 =
  let directions = [ -1, -1; -1, 0; -1, 1; 0, -1; 0, 1; 1, -1; 1, 0; 1, 1 ] in
  let rec go direction i j k =
    if not (Char.equal lines.(i).(j) (String.get "XMAS" k))
    then 0
    else if k = String.length "XMAS" - 1
    then 1
    else (
      let di, dj = direction in
      let ni, nj = i + di, j + dj in
      if 0 <= ni && ni < n && 0 <= nj && nj < m then go direction ni nj (k + 1) else 0)
  in
  let res = ref 0 in
  for i = 0 to n - 1 do
    for j = 0 to m - 1 do
      let tmp : int =
        List.map directions ~f:(fun direction -> go direction i j 0)
        |> List.fold ~f:( + ) ~init:0
      in
      res := !res + tmp
    done
  done;
  !res
;;

Stdio.printf "Task 1: %d\n" task1

let task2 : int =
  let find_x_mas_num a =
    let res = ref 0 in
    for i = 0 to Array.length a - 3 do
      for j = 0 to Array.length a.(0) - 3 do
        if Char.equal a.(i).(j) 'M'
           && Char.equal a.(i).(j + 2) 'S'
           && Char.equal a.(i + 1).(j + 1) 'A'
           && Char.equal a.(i + 2).(j) 'M'
           && Char.equal a.(i + 2).(j + 2) 'S'
        then res := !res + 1
      done
    done;
    !res
  in
  let rotate a =
    let rows = Array.length a in
    let cols = Array.length a.(0) in
    let rotated = Array.make_matrix ~dimx:cols ~dimy:rows '_' in
    for i = 0 to rows - 1 do
      for j = 0 to cols - 1 do
        rotated.(j).(rows - 1 - i) <- a.(i).(j)
      done
    done;
    rotated
  in
  find_x_mas_num lines
  + (find_x_mas_num @@ rotate lines)
  + (find_x_mas_num @@ rotate @@ rotate lines)
  + (find_x_mas_num @@ rotate @@ rotate @@ rotate lines)
;;

Stdio.printf "Task 2: %d\n" task2
