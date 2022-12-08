open System.IO


let dbg x = printfn "%A" x


type FileSystemEntry =
  | File of int
  | Directory of Map<string, FileSystemEntry>


let isDir a =
  match a with
  | Directory(_) -> true
  | _ -> false


let newFile size = File size


let emptyDir = Directory Map.empty


let rec deepInsert dirEntry (path: string array) newEntryName newEntry =
  match dirEntry with
  | File(_) -> dirEntry
  | Directory(content) -> 
    if Array.isEmpty path then
      Directory (Map.add newEntryName newEntry content)
    else
      let head = Array.head path
      let tail = Array.tail path
      let innerDirToUpdate =
        match Map.tryFind head content with
        | Some(x) -> x
        | None -> emptyDir
      let updatedDir = deepInsert innerDirToUpdate tail newEntryName newEntry
      Directory (Map.add head updatedDir content)


let butlast a =
  let countToKeep =
    (Array.length a) - 1
  Array.truncate countToKeep a


let rec restoreFileSystem root currentPath (lines: string list) =
  match lines with
  | [] -> root
  | head::tail ->
    match head.Split(" ") |> Array.toList with
    | ["$"; "cd"; ".."] ->
      restoreFileSystem root (butlast currentPath) tail
    | ["$"; "cd"; nextDir] ->
      restoreFileSystem root (Array.append currentPath [|nextDir|]) tail
    | ["$"; "ls"] ->
      restoreFileSystem root currentPath tail
    | ["dir"; dirName] ->
      restoreFileSystem (deepInsert root currentPath dirName emptyDir) currentPath tail
    | [size; name] ->
      let file = newFile (int size)
      restoreFileSystem (deepInsert root currentPath name file) currentPath tail
    | _ ->
      root


let rec fsEntrySize fsEntry =
  match fsEntry with
  | File(size) -> size
  | Directory(content) ->
    let dirSize =
      content
      |> Map.toSeq
      |> Seq.map snd
      |> Seq.map fsEntrySize
      |> Seq.sum
    dirSize


let rec allFSEntries fsEntry = seq {
  match fsEntry with
  | File(_) ->
    yield fsEntry
  | Directory(content) ->
    yield fsEntry
    yield! (
      content
      |> Map.toSeq
      |> Seq.map snd
      |> Seq.map allFSEntries
      |> Seq.concat
    )
}


[<EntryPoint>]
let main argv =
  let lines = File.ReadLines("input.txt") |> Seq.skip 1 |> Seq.toList
  let restoredFS = restoreFileSystem emptyDir Array.empty lines

  let allDirs = restoredFS |> allFSEntries |> Seq.filter isDir
  let dirSizes = allDirs |> Seq.map fsEntrySize

  let fsSize = 70000000
  let totalUsedSpace = Seq.max dirSizes
  let totalFreeSpace = fsSize - totalUsedSpace
  let totalSpaceNeeded = 30000000 - totalFreeSpace

  printfn "Task 1: %d" (dirSizes |> Seq.filter (fun x -> x <= 100000) |> Seq.sum)
  printfn "Task 2: %d" (dirSizes |> Seq.filter (fun x -> x >= totalSpaceNeeded) |> Seq.min)

  0
