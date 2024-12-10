open Core
open Common

let data =
  read_lines_from_stdin ()
  |> List.hd_exn
  |> String.to_array
  |> Array.map ~f:(fun c -> Char.to_string c |> Int.of_string)
;;

assert (Array.length data mod 2 = 1)

let task1 data =
  let data = Array.copy data in
  let idx = ref 0 in
  let file_idx = ref (Array.length data - 1) in
  (* Precompute the total number of memory blocks to allocate *)
  let total_memory = Array.fold data ~init:0 ~f:( + ) in
  let memory = Array.create ~len:total_memory 0 in
  let mem_idx = ref 0 in
  while !idx <= !file_idx do
    if !idx mod 2 = 0
    then (
      (* Write blocks for file_id from idx *)
      let file_id = !idx / 2 in
      for _ = 1 to data.(!idx) do
        memory.(!mem_idx) <- file_id;
        incr mem_idx
      done;
      incr idx)
    else if !idx mod 2 = 1 && data.(!idx) = 0
    then incr idx
    else if !idx mod 2 = 1 && data.(!file_idx) = 0
    then file_idx := !file_idx - 2
    else if !idx mod 2 = 1 && data.(!idx) > 0
    then (
      let file_id = !file_idx / 2 in
      let movable_count = Int.min data.(!idx) data.(!file_idx) in
      for _ = 1 to movable_count do
        memory.(!mem_idx) <- file_id;
        incr mem_idx
      done;
      data.(!idx) <- data.(!idx) - movable_count;
      data.(!file_idx) <- data.(!file_idx) - movable_count)
  done;
  (* Calculate the checksum *)
  Array.foldi memory ~f:(fun i acc file_id -> acc + (file_id * i)) ~init:0
;;

Stdio.printf "Task 1: %d\n" (task1 data);;
Out_channel.flush Out_channel.stdout

(* Task 2 is implemented only in Python (day09.py) because
   OCaml version was quite slow due to lots of memory allocations. (immutable lists)
   And the code is very messy if I try to optimize it by using 2d arrays.:shrug: *)
