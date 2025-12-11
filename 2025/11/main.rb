class Solver
  T2_REQUIRED_VISITS = %w[dac fft].freeze

  def initialize(fname)
    @graph = Hash.new { |h, k| h[k] = Set.new }
    File.open(fname, 'r') do |f|
      f.each_line do |line|
        parts = line.scan(/\w+/)
        parts[1..].each { |dest| @graph[parts.first] << dest }
      end
    end
  end

  private def search(memo, current, dest)
    return memo[current] if memo[current]

    memo[current] =
      if current == dest then 1
      else
        @graph[current].sum { |n| search(memo, n, dest) } end
  end

  def task1
    search({}, 'you', 'out')
  end

  private def search2(memo, current, dest, required_visits)
    key = [current, required_visits]
    return memo[key] if memo[key]

    memo[key] = if current == dest
                  required_visits.zero? ? 1 : 0
                else
                  @graph[current].sum do |n|
                    search2(memo, n, dest, required_visits - (T2_REQUIRED_VISITS.include?(current) ? 1 : 0))
                  end
                end
  end

  def task2
    search2({}, 'svr', 'out', 2)
  end

  def task2_alternative
    [
      search({}, 'svr', 'dac') * search({}, 'dac', 'fft') * search({}, 'fft', 'out'),
      search({}, 'svr', 'fft') * search({}, 'fft', 'dac') * search({}, 'dac', 'out')
    ].max
  end
end

solver = Solver.new('input.txt')
puts "Task 1: #{solver.task1}"
puts "Task 2: #{solver.task2}"
puts "Task 2(alt): #{solver.task2_alternative}"
