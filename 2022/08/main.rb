def is_valid(i, j, n)
  0 <= i and i < n and 0 <= j and j < n
end

def is_visible_from_direction(forest, i, j, di, dj)
  height = forest[i][j]
  i += di
  j += dj
  while is_valid(i, j, forest.length)
    return false if forest[i][j] >= height

    i += di
    j += dj
  end
  true
end

def task1(forest)
  res = 0
  (0...forest.length).each do |i|
    (0...forest.length).each do |j|
      next unless is_visible_from_direction(forest, i, j, -1, 0) ||
                  is_visible_from_direction(forest, i, j, 0, -1) ||
                  is_visible_from_direction(forest, i, j, 1, 0) ||
                  is_visible_from_direction(forest, i, j, 0, 1)

      res += 1
    end
  end
  res
end

def visible_trees(forest, i, j, di, dj)
  height = forest[i][j]
  visible = 0
  i += di
  j += dj
  while is_valid(i, j, forest.length)
    visible += 1
    break if forest[i][j] >= height

    i += di
    j += dj
  end
  visible
end

def task2(forest)
  max_scenic_score = 0

  (1...forest.length - 1).each do |i|
    (1...forest.length - 1).each do |j|
      tree_scenic_score = (
        visible_trees(forest, i, j, 0, -1) *
        visible_trees(forest, i, j, -1, 0) *
        visible_trees(forest, i, j, 1, 0) *
        visible_trees(forest, i, j, 0, 1)
      )
      max_scenic_score = [max_scenic_score, tree_scenic_score].max
    end
  end

  max_scenic_score
end

forest = []
IO.foreach 'input.txt' do |line|
  forest.push(line.strip.split('').map(&:to_i))
end
n = forest.length

puts format('Task 1: %d', task1(forest))
puts format('Task 2: %d', task2(forest))
