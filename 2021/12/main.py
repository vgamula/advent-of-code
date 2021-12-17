from collections import defaultdict
import fileinput

graph = defaultdict(set)

for line in fileinput.input():
    f, t = line.strip().split("-")
    graph[f].add(t)
    graph[t].add(f)


def task1(graph):
    all_paths = []

    def traverse(all_paths, current_node, current_path, visited):
        if current_node == "end":
            all_paths.append(",".join(current_path))
            return

        for edge in graph[current_node]:
            if edge in visited:
                continue
            current_path.append(edge)
            if edge.islower():
                visited.add(edge)
            traverse(all_paths, edge, current_path, visited)
            if edge.islower():
                visited.remove(edge)
            current_path.pop()

    traverse(all_paths, "start", ["start"], set(["start"]))

    return len(all_paths)


def task2(graph):
    all_paths = []

    visits = defaultdict(int)

    def can_visit(edge):
        if edge == "start":
            return False

        if edge == "end":
            return True

        if edge.isupper():
            return True

        if edge.islower():
            small_cave_visits = len([1 for x in visits.values() if x == 2])
            if small_cave_visits < 1 or small_cave_visits == 1 and visits[edge] == 0:
                return True

        return False

    def traverse(all_paths, current_node, current_path):

        if current_node == "end":
            all_paths.append(",".join(current_path))
            return

        for edge in graph[current_node]:
            if not can_visit(edge):
                continue
            if edge.islower():
                visits[edge] += 1
            current_path.append(edge)
            traverse(all_paths, edge, current_path)
            if edge.islower():
                visits[edge] -= 1
            current_path.pop()

    traverse(all_paths, "start", ["start"])

    return len(all_paths)


print(task1(graph))
print(task2(graph))
