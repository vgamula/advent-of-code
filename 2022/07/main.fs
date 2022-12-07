open System
open System.IO


let dbg x = printfn "%A" x


type FileRecord = 
  { Name: string;
    SizeInBytes: int }


type DirRecord<'a> = 
  { Name: string;
    Content: Map<string, 'a> }


type CustomFileSystemEntry =
  | CustomFile of FileRecord
  | CustomDir of DirRecord<CustomFileSystemEntry>


let newFile fileName size =
  CustomFile ({
    Name = fileName
    SizeInBytes = size
  })


let newEmptyDir dirName =
  CustomDir ({
    Name = dirName
    Content = Map.empty
  })


let (|Prefix|_|) (p:string) (s:string) =
    if s.StartsWith(p) then
        Some(s.Substring(p.Length))
    else
        None


let rec deepInsert (path: string array) dirEntry newEntryName newEntry =
  match dirEntry with
  | CustomFile(_) -> dirEntry
  | CustomDir({Name = name; Content = content}) -> 
    if Array.length path = 0 then
      CustomDir({
        Name = name;
        Content = Map.add newEntryName newEntry content
      })
    else
      let head = Array.head path in
      let tail = Array.tail path in
      let innerDirToUpdate =
        match content |> Map.tryFind head with
          | Some(x) -> x
          | None -> (newEmptyDir head)
      in
      let updatedDir = deepInsert tail innerDirToUpdate newEntryName newEntry in
      CustomDir({
        Name = name;
        Content = Map.add head updatedDir content
      })


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
      | Prefix "$ cd " nextFolder ->
        restoreFileSystem root (Array.append currentPath [|nextFolder|]) tail
      | Prefix "$ ls" _ ->
        restoreFileSystem root currentPath tail
      | Prefix "dir " dirName ->
        let dir = (newEmptyDir dirName) in
        restoreFileSystem (deepInsert currentPath root dirName dir) currentPath tail
      | rest ->
        match rest.Split(' ') with
        | [| size; name |] ->
          let file = newFile name (int size) in
          restoreFileSystem (deepInsert currentPath root name file) currentPath tail
        | _ ->
          root


type BoxedMutableValue = {
  mutable Value: int seq
}

  
let rec fsEntrySize fsEntry (boxedDirSizes: BoxedMutableValue) =
  match fsEntry with
  | CustomFile({Name = _; SizeInBytes = size}) ->
    size
  | CustomDir({Name = name; Content = content}) ->
    let folderSize =
      content
      |> Map.map (fun _ entry -> fsEntrySize entry boxedDirSizes)
      |> Map.toSeq
      |> Seq.map snd
      |> Seq.sum
    in
    boxedDirSizes.Value <- Seq.append boxedDirSizes.Value (Seq.singleton folderSize)
    folderSize

  
[<EntryPoint>]
let main argv =
    let lines = File.ReadLines("input.txt") |> Seq.skip 1 |> Seq.toList in
    let emptyFS = newEmptyDir "/" in
    let restoredFS = restoreFileSystem emptyFS Array.empty lines in
    let dirSizes = { Value = Seq.empty }
    let fsSize = 70000000 in
    let totalUsedSpace = fsEntrySize restoredFS dirSizes in
    let totalFreeSpace = fsSize - totalUsedSpace in
    let totalSpaceNeeded = 30000000 - totalFreeSpace in
    dbg (dirSizes.Value |> Seq.filter (fun x -> x <= 100000) |> Seq.sum)
    dbg (dirSizes.Value |> Seq.filter (fun x -> x >= totalSpaceNeeded ) |> Seq.min)
    0
