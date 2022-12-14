// sh -c swiftc -o main main.swift
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

func neighbors(node: (Int, Int), validator: (String.Element, String.Element) -> Bool) -> [(
  Int, Int
)] {
  var res: [(Int, Int)] = []
  for (di, dj) in zip([-1, 1, 0, 0], [0, 0, 1, -1]) {
    let i = node.0 + di
    let j = node.1 + dj
    if 0 <= i && i < n && 0 <= j && j < m {
      if validator(heights[node.0][node.1], heights[i][j]) {
        res.append((i, j))
      }
    }
  }
  return res
}

func getAsciiCode(s: String.Element) -> Int {
  if s == "S" {
    return Int(Character("a").asciiValue!)
  } else if s == "E" {
    return Int(Character("z").asciiValue!)
  } else {
    return Int(s.asciiValue!)
  }
}

func findShortestPath(
  startNode: (Int, Int), end: String.Element,
  neighborsValidator: (String.Element, String.Element) -> Bool
) -> Int {
  var minDistance = 9999999
  var dist = Array(repeating: Int.max, count: n * m)
  var queue = [State(cost: 0, node: startNode)]
  dist[positionToCode(pos: startNode)] = 0

  while queue.count > 0  {
    let state = queue.removeFirst()
    if heights[state.node.0][state.node.1] == end && state.cost < minDistance{
      minDistance = state.cost
    }

    guard state.cost <= dist[positionToCode(pos: state.node)] else {
      continue
    }

    for edge in neighbors(node: state.node, validator: neighborsValidator) {
      let next = State(cost: state.cost + 1, node: edge)

      if next.cost < dist[positionToCode(pos: next.node)] {
        dist[positionToCode(pos: next.node)] = next.cost
        queue.append(next)
      }
    }
  }
  return minDistance
}

func fewestStepsFromStart() -> Int {
  for i in 0..<n {
    for j in 0..<m {
      if heights[i][j] == "S" {
        let startNode = (i, j)
        return findShortestPath(
          startNode: startNode, end: "E",
          neighborsValidator: {
            getAsciiCode(s: $1) - getAsciiCode(s: $0) <= 1
          })
      }
    }
  }
  return -1
}

func fewestStepsFromA() -> Int {
  for i in 0..<n {
    for j in 0..<m {
      if heights[i][j] == "E" {
        let startNode = (i, j)
        return findShortestPath(
          startNode: startNode,
          end: "a",
          neighborsValidator: {
            getAsciiCode(s: $0) - getAsciiCode(s: $1) <= 1
          }
        )
      }
    }
  }
  return -1
}

print("Task 1:", fewestStepsFromStart())
print("Task 2:", fewestStepsFromA())
