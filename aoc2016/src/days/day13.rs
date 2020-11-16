use std::cmp::max;
use std::collections::BTreeSet;

use std::collections::vec_deque::VecDeque;

pub fn exec() {
    fn wall(i: (i32, i32)) -> bool {
        let x = i.0;
        let y = i.1;
        let fav = 1362;
        let mut mn = x * x + 3 * x + 2 * x * y + y + y * y + fav;
        let mut res = false;

        while mn > 0 {
            res = res ^ (mn & 1 == 1);
            mn = mn >> 1
        }

        res
    }

    let mut visited: BTreeSet<(i32, i32)> = BTreeSet::new();
    let mut queue: VecDeque<(i32, i32, i32)> = VecDeque::new();

    let mut part1 = 0;

    // x, y, steps taken
    queue.push_back((1, 1, 0));
    visited.insert((1, 1));

    while queue.len() > 0 {
        let e = queue.pop_front().unwrap();

        println!("{:?}", e);

        if e.0 == 31 && e.1 == 39 {
            part1 = e.2;
            break;
        }

        for d in [-1, 1].iter() {
            let dx = (max(0, e.0 + d), e.1);

            if !wall(dx) && !visited.contains(&dx) {
                queue.push_back((dx.0, dx.1, e.2 + 1));
                visited.insert(dx);
            }

            let dy = (e.0, max(0, e.1 + d));
            if !wall(dy) && !visited.contains(&dy) {
                queue.push_back((dy.0, dy.1, e.2 + 1));
                visited.insert(dy);
            }
        }
    }

    println!("Part1: {}", part1);

    queue.clear();
    visited.clear();

    // x, y, steps taken
    queue.push_back((1, 1, 0));
    visited.insert((1, 1));

    let mut part2 = 0;

    while queue.len() > 0 {
        let e = queue.pop_front().unwrap();

        part2 += 1;

        if e.2 != 50 {
            for d in [-1, 1].iter() {
                let dx = (max(0, e.0 + d), e.1);

                if !wall(dx) && !visited.contains(&dx) {
                    queue.push_back((dx.0, dx.1, e.2 + 1));
                    visited.insert(dx);
                }

                let dy = (e.0, max(0, e.1 + d));
                if !wall(dy) && !visited.contains(&dy) {
                    queue.push_back((dy.0, dy.1, e.2 + 1));
                    visited.insert(dy);
                }
            }
        }
    }

    println!("Part2: {}", part2);
}
