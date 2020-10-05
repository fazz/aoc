use std;
use std::cmp::Ordering;
use std::collections::HashMap;
use std::iter;
use std::iter::FromIterator;

use crate::common;

pub fn exec() {
    let input = common::lines_from_file("input06.txt");

    // pos -> char
    let mut char_counts: Vec<HashMap<char, i32>> =
        iter::repeat_with(|| HashMap::new()).take(8).collect();

    let mut linelen: Option<usize> = None;

    for line in input {
        if let None = linelen {
            linelen = Some(line.len());
        }
        for i in 0..linelen.unwrap() {
            let ccp = char_counts.iter_mut().nth(i).unwrap();

            let cc = ccp.entry(line.chars().nth(i).unwrap()).or_insert(0);

            *cc += 1;
        }
    }

    let mut part1 = vec!['0'; linelen.unwrap()];
    let mut part2 = vec!['0'; linelen.unwrap()];

    for i in 0..linelen.unwrap() {

        let hm = char_counts.get(i).unwrap();
        let mut counts: Vec<(&char, &i32)> = hm.iter().map(|x| x).collect();

        counts.sort_by(|a, b| {
            if a.1 < b.1 {
                return Ordering::Greater;
            } else if a.1 == b.1 {
                return Ordering::Equal;
            }
            return Ordering::Less;
        });
        part1[i] = *counts[0].0;

        counts.reverse();
        part2[i] = *counts[0].0;
    }

    println!("Part1: {}", String::from_iter(part1));
    println!("Part2: {}", String::from_iter(part2));
}