def read_input(fname)
    res = []
    IO.foreach fname do |line|
      res.push(line.strip().split("").map(&:to_i))
    end
    res
  end
  
  
  def to_hashmap(forest)
    res = Hash.new
    n = forest.length
    for i in 0...n
      for j in 0...n
        if i == 0 then
          res[[i-1, j]] = -1e18
        end
        if j == 0 then
          res[[i, j - 1]] = -1e18
        end
        if i == n - 1 then
          res[[i + 1, j]] = -1e18
        end
        if j == n - 1 then
          res[[i, j + 1]] = -1e18
        end
  
        res[[i, j]] = forest[i][j]
      end
    end
    res
  end
  
  
  def build_highest_trees_cache(forest, n)
    cache = Hash.new
  
    for i in 0...n
      for j in 0...n
        if i == 0 then
          cache[["up", i - 1, j]] = [i - 1, j]
        end
        if j == 0 then
          cache[["left", i, j - 1]] = [i, j - 1]
        end
  
        if forest[cache[["left", i, j - 1]]] > forest[[i, j]] then
          cache[["left", i, j]] = cache[["left", i, j - 1]]
        else
          cache[["left", i, j]] = [i, j]
        end
  
        if forest[cache[["up", i - 1, j]]] > forest[[i, j]] then
          cache[["up", i, j]] = cache[["up", i - 1, j]]
        else
          cache[["up", i, j]] = [i, j]
        end
      end
    end
  
    for i in (0...n).reverse_each
      for j in (0...n).reverse_each
        if i == n - 1 then
          cache[["down", i + 1, j]] = [i + 1, j]
        end
        if j == n - 1 then
          cache[["right", i, j + 1]] = [i, j + 1]
        end
        
        if forest[cache[["right", i, j + 1]]] > forest[[i, j]] then
          cache[["right", i, j]] = cache[["right", i, j + 1]]
        else
          cache[["right", i, j]] = [i, j]
        end
  
        if forest[cache[["down", i + 1, j]]] > forest[[i, j]] then
          cache[["down", i, j]] = cache[["down", i + 1, j]]
        else
          cache[["down", i, j]] = [i, j]
        end
      end
    end
  
    cache
  end
  
  
  def task1(forest, n)
    cache = build_highest_trees_cache(forest, n)
    res = 0
  
    for i in 0...n
      for j in 0...n
        height = forest[[i, j]]
  
        if (
          height > forest[cache[["left", i, j - 1]]] or 
          height > forest[cache[["up", i - 1, j]]] or 
          height > forest[cache[["right", i, j + 1]]] or 
          height > forest[cache[["down", i + 1, j]]]
        ) then
          res += 1
        end
  
      end
    end
  
    res
  end
  
  
  def task2(forest, n)
    max_scenic_score = 0
  
    for i in 1...n - 1
      for j in 1...n - 1
        height = forest[[i, j]]
  
        left_visible_trees = 0
        ii = i
        jj = j - 1
        while jj >= 0
          left_visible_trees += 1
          if forest[[ii, jj]] >= height
            break
          end
          jj -= 1
        end
  
        up_visible_trees = 0
        ii = i - 1
        jj = j
        while ii >= 0
          up_visible_trees += 1
          if forest[[ii, jj]] >= height
            break
          end
          ii -= 1
        end
  
        down_visible_trees = 0
        ii = i + 1
        jj = j
        while ii < n
          down_visible_trees += 1
          if forest[[ii, jj]] >= height
            break
          end
          ii += 1
        end
  
        right_visible_trees = 0
        ii = i
        jj = j + 1
        while jj < n
          right_visible_trees += 1
          if forest[[ii, jj]] >= height
            break
          end
          jj += 1
        end
  
        tree_scenic_score = up_visible_trees * right_visible_trees * down_visible_trees * left_visible_trees
  
        max_scenic_score = [max_scenic_score, tree_scenic_score].max
      end
    end
  
    max_scenic_score
  end
  
  
  raw_forest = read_input("input.txt")
  n = raw_forest.length
  forest = to_hashmap(raw_forest)
  
  puts "Task 1: %d" % [task1(forest, n)]
  puts "Task 2: %d" % [task2(forest, n)]
  