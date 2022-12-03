program AOC_2022_03;
uses crt;

type
  SetOfChar = set of char;

var
  tmp: string;
  input: array[0..300] of string;
  inputLen: integer;


function StrToSet(s: string): SetOfChar;
var
  tmp: SetOfChar = [];
  c: char;
begin
  for c in s do
    tmp := tmp + [c];
  StrToSet := tmp;
end;


function priority(c: char): integer;
begin
  if c = UpCase(c) then
    priority := Ord(c) - Ord('A') + 27
  else
    priority := Ord(c) - Ord('a') + 1;
end;


function checkRucksack(input: string): integer;
var
  commonItems: SetOfChar = [];
  c: char;
begin
  checkRucksack := 0;

  commonItems := (
    StrToSet(Copy(input, 1, Trunc(Length(input) / 2))) *
    StrToSet(Copy(input, Trunc(Length(input) / 2) + 1, Length(input)))
  );

  for c in commonItems do
    checkRucksack := checkRucksack + priority(c);
end;


function task1(input: array of string; inputLen: integer): integer;
var
  i: integer;
begin
  task1 := 0;

  for i := 0 to inputLen do
    task1 := task1 + checkRucksack(input[i]);
end;


function task2(input: array of string; inputLen: integer): integer;
var
  i: integer;
  commonBadges: SetOfChar;
  c: char;
begin
  task2 := 0;

  for i := 0 to Trunc(inputLen / 3) do begin
    commonBadges := (
      StrToSet(input[i * 3]) *
      StrToSet(input[i * 3 + 1]) *
      StrToSet(input[i * 3 + 2])
    );
    for c in commonBadges do
      task2 := task2 + priority(c);
  end;
end;


begin
  ClrScr;

  inputLen := 0;
  while True do begin
    ReadLn(tmp);
    if tmp = '' then break;
    input[inputLen] := tmp;
    inputLen := inputLen + 1;
  end;

  WriteLn('Task 1: ', task1(input, inputLen));
  WriteLn('Task 2: ', task2(input, inputLen));
end.
