use std::fs;

#[derive(Debug, Clone)]
struct Point {
    x: u32,
    y: u32,
}

impl Point {
    fn new(x: u32, y: u32) -> Self {
        Point { x, y }
    }
}

#[derive(Debug)]
struct Line<'a> {
    start: &'a Point,
    end: &'a Point,
}

fn area(a: &Point, b: &Point) -> u64 {
    u64::from(a.x.abs_diff(b.x) + 1) * u64::from(a.y.abs_diff(b.y) + 1)
}

fn task1(points: &[Point]) -> u64 {
    let mut result = 0;

    for (i, p1) in points.iter().enumerate() {
        for p2 in &points[i + 1..] {
            result = result.max(area(p1, p2));
        }
    }

    result
}

fn is_line_overlapping_rectangle(line: &Line, top_left: &Point, bottom_right: &Point) -> bool {
    let line_min_x = line.start.x.min(line.end.x);
    let line_max_x = line.start.x.max(line.end.x);
    let line_min_y = line.start.y.min(line.end.y);
    let line_max_y = line.start.y.max(line.end.y);

    if line_max_x <= top_left.x
        || bottom_right.x <= line_min_x
        || line_max_y <= top_left.y
        || bottom_right.y <= line_min_y
    {
        false
    } else {
        true
    }
}

fn is_rectangle_intersected_by_any_line(
    top_left: &Point,
    bottom_right: &Point,
    lines: &[Line],
) -> bool {
    lines
        .iter()
        .any(|line| is_line_overlapping_rectangle(line, top_left, bottom_right))
}

fn task2(points: &[Point], lines: &[Line]) -> u64 {
    let mut result = 0;

    for (i, a) in points.iter().enumerate() {
        for b in &points[i + 1..] {
            let potential_area = area(a, b);
            if potential_area <= result {
                continue;
            }

            let top_left = Point::new(a.x.min(b.x), a.y.min(b.y));
            let bottom_right = Point::new(a.x.max(b.x), a.y.max(b.y));

            if !is_rectangle_intersected_by_any_line(&top_left, &bottom_right, lines) {
                result = potential_area;
            }
        }
    }

    result
}

fn main() {
    let fname = "example.txt";
    let points = {
        let mut points: Vec<Point> = fs::read_to_string(fname)
            .unwrap()
            .trim()
            .split("\n")
            .map(|s| {
                let (x, y) = s.split_once(",").unwrap();
                Point::new(x.parse().unwrap(), y.parse().unwrap())
            })
            .collect();
        points.push(points[0].clone());
        points
    };

    let lines: Vec<Line> = points
        .windows(2)
        .map(|w| Line {
            start: &w[0],
            end: &w[1],
        })
        .collect();

    println!("Task 1: {}", task1(&points));
    println!("Task 2: {}", task2(&points, &lines));
}
