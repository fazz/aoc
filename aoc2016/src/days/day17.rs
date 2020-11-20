use md52::{Digest, Md5};

use std::collections::vec_deque::VecDeque;

fn get_input() -> (&'static str, i32, i32) {
    ("lpvhkcbi", 4, 4)
}

#[derive(Debug)]
struct State {
    x: i32,
    y: i32,
    path: String,
    digest: Md5,
}

impl State {
    // up, down, left, right
    fn calc(&self) -> (bool, bool, bool, bool) {
        let digest = format!("{:02x}", self.digest.clone().finalize());
        let digest = digest.as_bytes();

        fn pass(x: i32, y: i32, xd: i32, yd: i32, c: char) -> bool {
            let (_input, w, h) = get_input();

            let open = match c {
                'b' | 'c' | 'd' | 'e' | 'f' => true,
                _ => false,
            };

            open && x + xd >= 0 && y + yd >= 0 && x + xd < w && y + yd < h
        }

        (
            pass(self.x, self.y, 0, -1, digest[0] as char),
            pass(self.x, self.y, 0, 1, digest[1] as char),
            pass(self.x, self.y, -1, 0, digest[2] as char),
            pass(self.x, self.y, 1, 0, digest[3] as char),
        )
    }

    fn derive(&self, xd: i32, yd: i32) -> State {
        let c = match (xd, yd) {
            (0, -1) => "U",
            (0, 1) => "D",
            (-1, 0) => "L",
            (1, 0) => "R",
            _ => {panic!("WTF")}
        };

        let mut digest = self.digest.clone();
        digest.update(c.as_bytes());

        State {
            x: self.x + xd,
            y: self.y + yd,
            path: self.path.clone() + c,
            digest: digest,
        }
    }
}

pub fn exec() {
    let (input, w, h) = get_input();

    let mut queue = VecDeque::new();

    let mut digest = Md5::new();
    digest.update(input.as_bytes());

    queue.push_back(State {
        x: 0,
        y: 0,
        path: String::from(""),
        digest: digest,
    });

    let mut part1 = None;
    let mut part2 = 0;

    loop {
        let e = queue.pop_front();

        if e.is_none() {
            break;
        }

        let e = e.unwrap();

        if e.x == w - 1 && e.y == h - 1 {
            if part1.is_none() {
                part1 = Some(e.path.clone());
            }
            if e.path.len() > part2 {
                part2 = e.path.len();
            }
            continue;
        }

        let (u, d, l, r) = e.calc();
        if u {
            queue.push_back(e.derive(0, -1));
        }
        if d {
            queue.push_back(e.derive(0, 1));
        }
        if l {
            queue.push_back(e.derive(-1, 0));
        }
        if r {
            queue.push_back(e.derive(1, 0));
        }
    }

    println!("Part1: {}", part1.unwrap());

    println!("Part2: {}", part2);
}
