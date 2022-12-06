DIM tmp AS STRING

FUNCTION are_all_characters_different(a AS STRING) AS BOOLEAN
  DIM freqs(1 TO 26) AS SINGLE
  DIM letter_number AS INTEGER

  FOR i AS INTEGER = 1 to LEN(a)
    letter_number = ASC(MID(a, i, 1)) - ASC("a") + 1
    freqs(letter_number) = freqs(letter_number) + 1
  NEXT

  FOR i AS INTEGER = 1 to 26
    IF freqs(i) >= 2 THEN
      RETURN FALSE
    END IF
  NEXT

  RETURN TRUE
END FUNCTION

FUNCTION start_of_packet(a AS STRING, len_to_check AS INTEGER) AS INTEGER
  FOR i AS INTEGER = len_to_check TO LEN(A)
    IF are_all_characters_different(MID(A, i - len_to_check + 1, len_to_check)) THEN
      RETURN i
    END IF
  NEXT

  RETURN -1
END FUNCTION

OPEN "input.txt" FOR INPUT AS #1
DO UNTIL EOF(1)
  INPUT #1, tmp
  PRINT "Task 1:", start_of_packet(tmp, 4)
  PRINT "Task 2:", start_of_packet(tmp, 14)
LOOP
