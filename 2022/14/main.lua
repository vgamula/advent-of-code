function sign(x)
  if x < 0 then
    return -1
  elseif x == 0 then
    return 0
  elseif x > 0 then
    return 1
  end
end


function coordinate(x, y)
  return tostring(x) .. '_' .. tostring(y)
end


function get(cave, x, y)
  coord = coordinate(x, y)
  if cave[coord] ~= nil then
    return cave[coord]
  else
    return '.'
  end
end


function set(cave, x, y, value)
  coord = coordinate(x, y)
  cave[coord] = value
end


function parse_line_coords(line)
  line_points = {}
  for token in string.gmatch(line, '\-?%d+,-%d+') do
    point = {}
    for x_or_y in string.gmatch(token, '\-?%d+') do
      table.insert(point, tonumber(x_or_y))
    end
    table.insert(line_points, point)
  end
  return line_points
end


function init_cave(fname, bottom_line)
  all_points = {}
  for line in io.lines(fname) do
    table.insert(all_points, parse_line_coords(line))
  end
  if bottom_line ~= nil then
    table.insert(all_points, parse_line_coords(bottom_line))
  end

  cave = {}
  max_y = 0

  for _, line_points in pairs(all_points) do
    for i, next_point in ipairs(line_points) do
      if i > 1 then
        prev_point = line_points[i - 1]
        x1 = prev_point[1]
        y1 = prev_point[2]
        x2 = next_point[1]
        y2 = next_point[2]
        dx = sign(x2 - x1)
        dy = sign(y2 - y1)
        while x1 ~= x2 or y1 ~= y2 do
          set(cave, x1, y1, '#')
          x1 = x1 + dx
          y1 = y1 + dy
          if y1 > max_y then
            max_y = y1
          end
        end
        set(cave, x1, y1, '#')
      end
    end
  end

  return cave, max_y
end


function print_cave(cave, start_x, start_y, end_x, end_y)
  s = ''
  for y=start_y, end_y do
    for x=start_x, end_x do
      s = s .. get(cave, x, y)
    end
    s = s .. '\n'
  end
  print(s)
end


function pour_sand(cave, max_depth)
  x = 500
  y = 0
  while true do
    if y > max_depth then
      return 0
    end
    below_x = x
    below_y = y + 1
    if get(cave, x, y) == 'o' then
      return 0
    elseif get(cave, below_x, below_y) == '.' then
      y = y + 1
    elseif (
        get(cave, below_x, below_y) == '#' and
        get(cave, below_x - 1, below_y) == '#' and
        get(cave, below_x + 1, below_y) == '#'
    ) then
      set(cave, x, y, 'o')
      return 1
    elseif get(cave, below_x - 1, below_y) == '.' then
      x = x - 1
      y = y + 1
    elseif get(cave, below_x + 1, below_y) == '.' then
      x = x + 1
      y = y + 1
    else
      set(cave, x, y, 'o')
      return 1
    end
  end
end


function max_units_of_sand(cave, max_depth)
  res = 0
  while true do
    r = pour_sand(cave, max_depth)
    res = res + r
    if r == 0 then
      break
    end
  end
  return res
end


fname = 'input.txt'

cave, max_depth = init_cave(fname)
print('Task 1:', max_units_of_sand(cave, max_depth))

bottom_depth = max_depth + 2
bottom_line = (
  '-999,' .. tostring(bottom_depth) ..
  ' -> ' ..
  '999,' .. tostring(bottom_depth)
)
cave, max_depth = init_cave(fname, bottom_line)
print('Task 2:', max_units_of_sand(cave, max_depth))
