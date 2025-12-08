import Foundation

let fname = "example.txt"
let toProcess = 10

// let fname = "input.txt"
// let toProcess = 1000

struct JunctionBox {
    let id: Int
    let x: Int
    let y: Int
    let z: Int

    func distance(_ other: JunctionBox) -> Decimal {
        pow(Decimal(x - other.x), 2) + pow(Decimal(y - other.y), 2) + pow(Decimal(z - other.z), 2)
    }
}

struct UnionFind {
    private var parent: [Int]

    init(size: Int) {
        parent = [Int](0..<size)
    }

    mutating func find(_ x: Int) -> Int {
        if parent[x] != x {
            parent[x] = find(parent[x])
        }
        return parent[x]
    }

    mutating func union(_ a: Int, _ b: Int) {
        let aRoot = find(a)
        let bRoot = find(b)

        if aRoot != bRoot {
            parent[aRoot] = bRoot
        }
    }
}

let boxes = try String(contentsOfFile: fname, encoding: .utf8)
    .split(separator: "\n")
    .enumerated()
    .map({
        id, line -> JunctionBox in
        let xyz = line.split(separator: ",").map({ Int($0)! })
        return JunctionBox(id: id, x: xyz[0], y: xyz[1], z: xyz[2])
    })
assert(boxes.count > 0)

var pairs = [(distance: Decimal, a: JunctionBox, b: JunctionBox)]()
for (i, a) in boxes.enumerated() {
    for b in boxes[(i + 1)...] {
        let distance = a.distance(b)
        pairs.append((distance, a, b))
    }
}
pairs.sort(by: { $0.distance < $1.distance })

func task1(toProcess: Int) -> Int {
    var uf = UnionFind(size: boxes.count)

    for (_, a, b) in pairs.prefix(toProcess) {
        if uf.find(a.id) != uf.find(b.id) {
            uf.union(a.id, b.id)
        }
    }

    var counter = [Int: Int]()
    for box in boxes {
        counter[uf.find(box.id), default: 0] += 1
    }

    return counter.values.sorted().suffix(3).reduce(1, *)
}

func task2() -> Int {
    var uf = UnionFind(size: boxes.count)
    var result = 0

    for (_, a, b) in pairs {
        if uf.find(a.id) != uf.find(b.id) {
            uf.union(a.id, b.id)
            result = a.x * b.x
        }
    }

    return result
}

print("Task 1:", task1(toProcess: toProcess))
print("Task 2:", task2())
