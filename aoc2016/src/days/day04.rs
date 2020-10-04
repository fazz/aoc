use regex::Regex;
use std;
use std::cmp::Ordering;
use std::cmp::{max, min};
use std::collections::HashMap;

use crate::common;

pub fn exec() {
    let input = common::lines_from_file("input04.txt");

    let re = Regex::new(r"(\D{1,})-(\d{1,})[\[](\D{1,})[\]]").unwrap();

    let mut part1 = 0;
    let mut part2 = 0;

    for line in input.iter() {
        let caps = re.captures(line).unwrap();

        let name = caps.get(1).unwrap().as_str();
        let sector_id = caps.get(2).unwrap().as_str().parse::<i32>().unwrap();
        let cc = caps.get(3).unwrap().as_str().to_string();

        let mut char_counts = HashMap::new();

        for c in name.chars() {
            match c {
                'a'..='z' => {
                    let cc = char_counts.entry(c).or_insert(0);
                    *cc += 1;
                }
                '-' => {}
                _ => panic!("WTF"),
            }
        }

        let mut counts: Vec<(&char, &i32)> = char_counts.iter().map(|x| x).collect();

        counts.sort_by(|a, b| {
            if a.1 < b.1 {
                return Ordering::Greater;
            } else if a.1 == b.1 {
                if a.0 < b.0 {
                    return Ordering::Less;
                }
                return Ordering::Greater;
            }
            return Ordering::Less;
        });

        let mut accumulator = String::from ("");
        let folded = counts.iter().fold(&mut accumulator, |acc, e| {
            if acc.len() >= 5 {
                return acc;
            }
            acc.push(*e.0);
            return acc;
        });

        if *folded == cc {
            part1 += sector_id;

            let realshift = (sector_id % 26) as i8;

            let mut accumulator = String::from ("");
            let x = name.chars().into_iter().map(
                |c| {
                    if c == '-' {
                        return ' ';
                    }
                    let mut ca = c as i8 - 'a' as i8;
                    ca += realshift;
                    return (ca % 26 + 'a' as i8) as u8 as char;
                }
            ).fold(&mut accumulator, |acc, v| {
                acc.push(v);
                return acc;
            }
            );

            if x == "northpole object storage" {
                part2 = sector_id;
            }
        };

    }

    println!("Part1: {:?}", part1);
    println!("Part2: {:?}", part2);
}
