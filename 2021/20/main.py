import fileinput

lines = [line.strip() for line in fileinput.input()]

algorithm = lines[0]
image = {}
for y, line in enumerate(lines[2:]):
    for x, c in enumerate(line):
        if c == "#":
            image[(y, x)] = c

y1 = 0
y2 = len(lines) - 2

x1 = 0
x2 = len(lines[2])


def print_image(image, x1, x2, y1, y2):
    for i in range(y1 - 1, y2 + 2):
        tmp = ""
        for j in range(x1 - 1, x2 + 2):
            tmp += image.get((i, j), ".")
        print(tmp)


def get_algorith_key(img, y, x) -> int:
    tmp = ""
    for i in range(-1, 2):
        for j in range(-1, 2):
            tmp += img.get((y + i, x + j), ".")
    return int(tmp.replace(".", "0").replace("#", "1"), 2)


def enhance(input_image, x1, x2, y1, y2, outer_value):
    output_image = {}

    x1 -= 1
    x2 += 1

    y1 -= 1
    y2 += 1

    for y in range(y1, y2 + 1):
        for x in range(x1, x2 + 1):
            algorithm_key = 0
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    is_out_of_bounds = not (y1 < y + dy < y2) or not (x1 < x + dx < x2)
                    algorithm_key <<= 1
                    algorithm_key |= (y + dy, x + dx) in input_image or (
                        is_out_of_bounds and outer_value == "#"
                    )

            if algorithm[algorithm_key] == "#":
                output_image[(y, x)] = "#"

    next_outer_value = algorithm[-1 if outer_value == "#" else 0]
    return output_image, x1, x2, y1, y2, next_outer_value


def enhance_n_times(image, x1, x2, y1, y2, n):
    outer_value = "."
    for _i in range(n):
        image, x1, x2, y1, y2, outer_value = enhance(image, x1, x2, y1, y2, outer_value)
    return image, x1, x2, y1, y2


def lit_pixels(image):
    return sum(pixel == "#" for pixel in image.values())


image_1, *_ = enhance_n_times(image, x1, x2, y1, y2, 2)
print("Task 1:", lit_pixels(image_1))

image_2, *_ = enhance_n_times(image, x1, x2, y1, y2, 50)
print("Task 2:", lit_pixels(image_2))
