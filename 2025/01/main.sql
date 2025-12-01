-- duckdb -f main.sql
with recursive
  commands as materialized (
    select
      command,
      cast(substring(command, 2) as int) as _num,
      if (command[1] = 'L', -1, 1) * (_num % 100) as ticks,
      _num // 100 as full_rotations,
      idx
    from
      -- read_text('input01.txt'),
      read_text('example01.txt'),
      unnest(split(content, e'\n'))
    with
      ordinality as t (command, idx)
    where
      command <> ''
  ),
  result (idx) as (
    select
      0 as idx,
      50 as dial_position,
      0 as number_of_times_dial_pointed_at_zero
    union all
    select
      cmd.idx,
      (100 + prev.dial_position + cmd.ticks) % 100 as dial_position,
      cmd.full_rotations + if (prev.dial_position + cmd.ticks > 99, 1, 0) + if (
        0 < prev.dial_position
        and prev.dial_position + cmd.ticks <= 0,
        1,
        0
      ) as number_of_times_dial_pointed_at_zero
    from
      commands cmd
      join result prev on cmd.idx = prev.idx + 1
  )
select
  count_if(dial_position = 0) as task1,
  sum(number_of_times_dial_pointed_at_zero) as task2
from
  result
