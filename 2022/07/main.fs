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


let (|Prefix|_|) (p:string) (s:string) =
  if s.StartsWith p then
    Some (s.Substring p.Length)
  else
    None


let rec deepInsert (path: string array) dirEntry newEntryName newEntry =
  match dirEntry with
  | File(_) -> dirEntry
  | Directory(content) -> 
    if Array.length path = 0 then
      Directory (Map.add newEntryName newEntry content)
    else
      let head = Array.head path in
      let tail = Array.tail path in
      let innerDirToUpdate =
        match content |> Map.tryFind head with
          | Some(x) -> x
          | None -> emptyDir
      in
      let updatedDir = deepInsert tail innerDirToUpdate newEntryName newEntry in
      Directory (Map.add head updatedDir content)


let butlast a =
  let countToKeep =
    (Array.length a) - 1
  in
  Array.truncate countToKeep a


let rec restoreFileSystem root currentPath lines =
  match lines with
    | [] -> root
    | head::tail ->
      match head with
      | Prefix "$ cd .." _ ->
        restoreFileSystem root (butlast currentPath) tail
      | Prefix "$ cd " nextDir ->
        restoreFileSystem root (Array.append currentPath [|nextDir|]) tail
      | Prefix "$ ls" _ ->
        restoreFileSystem root currentPath tail
      | Prefix "dir " dirName ->
        restoreFileSystem (deepInsert currentPath root dirName emptyDir) currentPath tail
      | rest ->
        match rest.Split(' ') with
        | [| size; name |] ->
          let file = newFile (int size) in
          restoreFileSystem (deepInsert currentPath root name file) currentPath tail
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
    in
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
    let lines = File.ReadLines("input.txt") |> Seq.skip 1 |> Seq.toList in
    let restoredFS = restoreFileSystem emptyDir Array.empty lines in

    let allDirs = restoredFS |> allFSEntries |> Seq.filter isDir in
    let dirSizes = allDirs |> Seq.map fsEntrySize in

    let fsSize = 70000000 in
    let totalUsedSpace = Seq.max dirSizes in
    let totalFreeSpace = fsSize - totalUsedSpace in
    let totalSpaceNeeded = 30000000 - totalFreeSpace in

    dbg (dirSizes |> Seq.filter (fun x -> x <= 100000) |> Seq.sum)
    dbg (dirSizes |> Seq.filter (fun x -> x >= totalSpaceNeeded ) |> Seq.min)

    0
