// sh -c swiftc -o main main.swift Heap.swift
import Foundation

let file = "input.txt"

func readInput(filename: String) -> String {
  let url = URL(fileURLWithPath: filename)
  let contents = try! String(contentsOf: url, encoding: .utf8)
  return contents
}

let heights = readInput(filename: file).components(separatedBy: "\n").map({ Array($0) })

let n = heights.count
let m = heights[0].count

struct State {
  var cost: Int
  var node: (Int, Int)
}

func positionToCode(pos: (Int, Int)) -> Int {
  return pos.0 * m + pos.1
}

func neighbors(node: (Int, Int)) -> Array<(Int, Int)> {
  var res: Array<(Int, Int)> = []
  for (di, dj) in zip([-1, 1, 0, 0], [0, 0, 1, -1]) {
    let i = node.0 + di
    let j = node.1 + dj
    if (0 <= i && i < n && 0 <= j && j < m) {
      let a = getAsciiCode(s: heights[node.0][node.1])
      let b = getAsciiCode(s: heights[i][j])
      if (b - a <= 1) {
        res.append((i, j))  
      }
    }
  }
  return res
}

func getAsciiCode(s: String.Element) -> Int {
  if (s == "S") {
    return Int(Character("a").asciiValue!)
  } else if (s == "E") {
    return Int(Character("z").asciiValue!)
  } else {
    return Int(s.asciiValue!)
  }
}

func findShortestPathFromStart(startNode: (Int, Int)) -> Int {
  var dist = Array(repeating: Int.max, count: n * m)
  var heap = Heap<State>(sort: { $0.cost < $1.cost})
  heap.insert(State(cost: 0, node: startNode))
  dist[positionToCode(pos: startNode)] = 0

  while let state = heap.remove(at: 0) {
    if heights[state.node.0][state.node.1] == "E" {
      return state.cost
    }

    guard state.cost <= dist[positionToCode(pos: state.node)] else {
      continue
    }

    for edge in neighbors(node: state.node) {
      let next = State(cost: state.cost + 1, node: edge)

      if next.cost < dist[positionToCode(pos: next.node)] {
        dist[positionToCode(pos: next.node)] = next.cost
        heap.insert(next)
      }
    }
  }
  return -1
}

func fewestStepsFromStart() -> Int {
  for i in 0..<n {
    for j in 0..<m {
      if heights[i][j] == "S" {
        let startNode = (i, j)
        return findShortestPathFromStart(startNode: startNode)
      }
    }
  }
  return -1
}

func fewestStepsFromA() -> Int {
  var minDistance = 9999999
  for i in 0..<n {
    for j in 0..<m {
      if heights[i][j] == "S" || heights[i][j] == "a" {
        let startNode = (i, j)
        let shortestPath = findShortestPathFromStart(startNode: startNode)
        if (shortestPath != -1 ) {
          minDistance = min(minDistance, shortestPath)
        }
      }
    }
  }
  return minDistance
}

print("Task 1: ", fewestStepsFromStart())
print("Task 2: ", fewestStepsFromA())
