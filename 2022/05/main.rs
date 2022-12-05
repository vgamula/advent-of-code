use std::cell::RefCell;
use std::collections::{HashMap, VecDeque};
use std::fs;

const FNAME: &str = "input.txt";

fn initial_stacks(rows: &Vec<&str>) -> HashMap<char, RefCell<VecDeque<char>>> {
    let mut map = HashMap::new();
    let numbers_row_idx: usize = rows
        .iter()
        .enumerate()
        .find(|&r| r.1.to_string() == "".to_string())
        .expect("must find empty row")
        .0
        - 1;
    for number_char in '1'..='9' {
        let mut queue = VecDeque::new();
        match rows[numbers_row_idx].find(number_char) {
            None => break,
            Some(number_char_idx) => {
                for i in (0..numbers_row_idx).rev() {
                    let current_box = rows[i].chars().nth(number_char_idx).expect("");
                    if current_box == ' ' {
                        break;
                    }
                    queue.push_back(current_box);
                }
            }
        }
        map.insert(number_char, RefCell::new(queue));
    }
    map
}

fn operations(rows: &Vec<&str>) -> Vec<(char, char, u32)> {
    let empty_row_idx: usize = rows
        .iter()
        .enumerate()
        .find(|&r| r.1.to_string() == "".to_string())
        .expect("must find empty row")
        .0;
    let mut ops = vec![];
    for row_idx in (empty_row_idx + 1)..rows.len() {
        let parts = rows[row_idx].split(" ").collect::<Vec<&str>>();
        let from = parts[3].to_string().chars().nth(0).expect("");
        let to = parts[5].to_string().chars().nth(0).expect("");
        let n: u32 = parts[1].parse().expect("");
        ops.push((from, to, n))
    }
    ops
}

fn task1(stacks: HashMap<char, RefCell<VecDeque<char>>>, ops: &Vec<(char, char, u32)>) -> String {
    let mut res: Vec<String> = vec![];
    for (from, to, n) in ops {
        let mut from_stack = stacks[&from].borrow_mut();
        let mut to_stack = stacks[&to].borrow_mut();
        for _ in 0..*n {
            to_stack.push_back(from_stack.pop_back().expect(""));
        }
    }
    for c in '1'..='9' {
        if !stacks.contains_key(&c) {
            break;
        }
        let top_box = stacks[&c]
            .borrow()
            .iter()
            .last()
            .unwrap_or(&'\0')
            .to_string();
        res.push(top_box);
    }
    String::from_iter(res)
}

fn task2(stacks: HashMap<char, RefCell<VecDeque<char>>>, ops: &Vec<(char, char, u32)>) -> String {
    let mut res: Vec<String> = vec![];
    for (from, to, n) in ops {
        let mut from_stack = stacks[&from].borrow_mut();
        let mut tmp_stack = VecDeque::new();
        for _ in 0..*n {
            tmp_stack.push_front(from_stack.pop_back().expect(""));
        }
        let mut to_stack = stacks[&to].borrow_mut();
        for _ in 0..*n {
            to_stack.push_back(tmp_stack.pop_front().expect(""));
        }
    }
    for c in '1'..='9' {
        if !stacks.contains_key(&c) {
            break;
        }
        let top_box = stacks[&c]
            .borrow()
            .iter()
            .last()
            .unwrap_or(&' ')
            .to_string();
        res.push(top_box);
    }
    String::from_iter(res)
}

fn main() {
    let file_content = fs::read_to_string(FNAME).expect("Error when reading the file");
    let rows = file_content.split("\n").collect::<Vec<&str>>();
    let stacks = initial_stacks(&rows);
    let ops = operations(&rows);
    println!("Task 1: {:?}", task1(stacks.clone(), &ops));
    println!("Task 2: {:?}", task2(stacks.clone(), &ops));
}
