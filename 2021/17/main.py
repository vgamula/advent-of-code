from collections import defaultdict

x_min, x_max, y_min, y_max = list(
    map(
        int,
        input()
        .replace("target area: x=", "")
        .replace(", y=", " ")
        .replace("..", " ")
        .split(" "),
    )
)


def simulate_probe_shot(vx, vy, steps):
    grid = defaultdict(lambda: ".")

    grid[(0, 0)] = "S"

    t_positions = set()
    for y in range(y_min, y_max + 1):
        for x in range(x_min, x_max + 1):
            grid[(y, x)] = "T"
            t_positions.add((y, x))

    sx, sy = 0, 0

    for _ in range(steps):
        sx += vx
        sy += vy
        grid[(sy, sx)] = "#"
        vx = max(0, vx - 1)
        vy -= 1

    for y in range(10, -25, -1):
        tmp = ""
        for x in range(0, 70):
            tmp += grid[(y, x)]
        print(tmp)


# simulate_probe_shot(6, 3, 10)


global_max_y = 0
for yv in range(-100, 100):
    found = False
    y = 0
    local_max_y = 0
    while True:
        if y < y_min:
            break

        y += yv
        yv -= 1
        local_max_y = max(local_max_y, y)

        if y_min <= y <= y_max:
            found = True
            break
    if found:
        global_max_y = max(global_max_y, local_max_y)
print("Task 1:", global_max_y)

count = 0
for _xv in range(400):
    for _yv in range(-100, 100):
        xv = _xv
        yv = _yv
        good = False
        x, y = 0, 0
        while True:
            if y < y_min or x > x_max:
                break

            x += xv
            xv = max(0, xv - 1)

            y += yv
            yv -= 1

            if x_min <= x <= x_max and y_min <= y <= y_max:
                good = True
                break
        if good:
            count += 1
print("Task 2:", count)
