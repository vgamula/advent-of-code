open Core

let read_lines_from_stdin () =
  In_channel.input_lines In_channel.stdin
  |> List.map ~f:String.strip
  |> List.filter ~f:(fun s -> not (String.is_empty s))
;;
