use std;
use std::cmp::Ordering;
use std::collections::HashMap;
use std::iter;
use std::iter::FromIterator;

use crate::common;

pub fn exec() {
    let input = common::lines_from_file("input07.txt");

    let mut part1 = 0;
    let mut part2 = 0;

    fn p1test(buffer: &[char; 4], pos: i32) -> bool {
        let a1 = (pos - 3) as usize % 4;
        let b1 = (pos - 2) as usize % 4;
        let b2 = (pos - 1) as usize % 4;
        let a2 = (pos - 0) as usize % 4;

        return buffer[a1] != '-'
            && buffer[a1] == buffer[a2]
            && buffer[b1] == buffer[b2]
            && buffer[a1] != buffer[b1];
    };

    fn p2test(buffer: &[char; 3], pos: i32) -> (bool, String, String) {
        let a1 = (pos - 2) as usize % 3;
        let b1 = (pos - 1) as usize % 3;
        let a2 = (pos - 0) as usize % 3;

        let b = buffer[a1] != '-'
            && buffer[b1] != '-'
            && buffer[a1] == buffer[a2]
            && buffer[a1] != buffer[b1];

        let mut aba = String::new();
        let mut bab = String::new();
        if b {
            aba.push(buffer[a1]);
            aba.push(buffer[b1]);
            bab.push(buffer[b1]);
            bab.push(buffer[a1]);
        }

        return (b, aba, bab);
    }

    for line in input {
        {
            let mut buffer = ['-', '-', '-', '-'];

            let mut hypernet = false;

            let mut abba = false;
            let mut abbah = false;

            for i in 0..line.len() as i32 {
                let c = line.chars().nth(i as usize).unwrap();
                match c {
                    '[' => {
                        hypernet = true;
                        buffer = ['-', '-', '-', '-'];
                    }
                    ']' => {
                        hypernet = false;
                        buffer = ['-', '-', '-', '-'];
                    }
                    _ => buffer[i as usize % 4] = c,
                }
                if hypernet {
                    abbah = p1test(&buffer, i);
                } else {
                    abba = abba || p1test(&buffer, i);
                }
                if abbah {
                    break;
                }
            }
            if abba && (!abbah) {
                part1 += 1;
            }
        }
        {
            let mut buffer = ['-', '-', '-'];

            let mut hypernet = false;

            let mut aba = HashMap::new();
            let mut bab = HashMap::new();

            for i in 0..line.len() as i32 {
                let c = line.chars().nth(i as usize).unwrap();
                match c {
                    '[' => {
                        hypernet = true;
                        buffer = ['-', '-', '-'];
                    }
                    ']' => {
                        hypernet = false;
                        buffer = ['-', '-', '-'];
                    }
                    _ => buffer[i as usize % 3] = c,
                }

                let (test, v1, v2) = p2test(&buffer, i);

                if test {
                    if hypernet {
                        bab.insert(v2, true);
                    } else {
                        aba.insert(v1, true);
                    }
                }
            }
            if (aba.iter().filter(|e| bab.contains_key(e.0)).count()) > 0 {
                part2 += 1;
            }
        }
    }

    println!("Part1: {}", part1);
    println!("Part2: {}", part2);
}
