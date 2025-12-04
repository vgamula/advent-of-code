let is_valid_coord grid i j =
  0 <= i && i < Array.length grid && 0 <= j && j < Array.length grid.(0)
;;

let neighbour_papers grid i j =
  let coords =
    [ i - 1, j - 1
    ; i - 1, j
    ; i - 1, j + 1
    ; i, j - 1
    ; i, j + 1
    ; i + 1, j - 1
    ; i + 1, j
    ; i + 1, j + 1
    ]
  in
  coords
  |> List.filter (fun (i, j) -> is_valid_coord grid i j)
  |> List.filter (fun (i, j) -> grid.(i).(j) == '@')
;;

let removable_paper_positions grid =
  let all_positions =
    List.init
      (Array.length grid * Array.length grid.(0))
      (fun i -> i / Array.length grid.(0), i mod Array.length grid.(0))
  in
  all_positions
  |> List.filter (fun (i, j) ->
       grid.(i).(j) == '@' && List.length @@ neighbour_papers grid i j < 4)
;;

let part1 grid = List.length @@ removable_paper_positions grid

let part2 original_grid =
  let grid_copy = Array.map Array.copy original_grid in
  let rec loop grid =
    match removable_paper_positions grid with
    | [] -> 0
    | r ->
      r |> List.iter (fun (i, j) -> grid.(i).(j) <- '.');
      List.length r + loop grid
  in
  loop grid_copy
;;

let () =
  let lines =
    "example01.txt"
    |> In_channel.open_text
    |> In_channel.input_all
    |> String.trim
    |> String.split_on_char '\n'
  in
  let grid =
    lines |> List.map (fun x -> String.to_seq x |> Array.of_seq) |> Array.of_list
  in
  let res1 = part1 grid
  and res2 = part2 grid in
  Printf.printf "Part 1: %d\n" res1;
  Printf.printf "Part 2: %d\n" res2
;;
