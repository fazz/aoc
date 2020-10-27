use regex::Regex;

use crate::common;

pub fn exec() {
    let input = common::lines_from_file("input08.txt");

    let rerect = Regex::new(r"rect (\d{1,})x(\d{1,})").unwrap();
    let rerotate = Regex::new(r"rotate (row y|column x)=(\d{1,}) by (\d{1,})").unwrap();

    let mut display = [[0i32; 50]; 6];

    let mut part1 = 0;

    for line in input.iter() {
        let capsrect = rerect.captures(line);
        let capsrotate = rerotate.captures(line);

        if capsrect.is_some() {
            let c = capsrect.unwrap();
            let x = c.get(1).unwrap().as_str().parse::<usize>().unwrap();
            let y = c.get(2).unwrap().as_str().parse::<usize>().unwrap();
            for yy in 0..y {
                for xx in 0..x {
                    if display[yy][xx] == 0 {
                        part1 += 1;
                    }
                    display[yy][xx] = 1;
                }
            }
        } else {
            let c = capsrotate.unwrap();

            let direction = c.get(1).unwrap().as_str();
            let amt = c.get(3).unwrap().as_str().parse::<usize>().unwrap();

            if direction == "row y" {
                let row = c.get(2).unwrap().as_str().parse::<usize>().unwrap();

                let mut buffer: Vec<i32> = Vec::with_capacity(amt);

                buffer.extend_from_slice(&display[row][0..amt]);
                for x in 0..50 as usize {
                    let tmp2 = display[row][(x + amt) % 50];

                    display[row][(x + amt) % 50] = buffer[x % amt];

                    buffer[x % amt] = tmp2;
                }
            } else {
                let col = c.get(2).unwrap().as_str().parse::<usize>().unwrap();

                let mut buffer: Vec<i32> = Vec::with_capacity(amt);

                buffer.extend(display[0..amt].iter().map(|&i| i[col]));
                for y in 0..6 as usize {
                    let tmp2 = display[(y + amt) % 6][col];
                    display[(y + amt) % 6][col] = buffer[y % amt];
                    buffer[y % amt] = tmp2;
                }
            }
        }
    }

    println!("Part1: {:?}", part1);
    println!("Part2:");
    println!("");

    for y in 0..6 {
        let r: String = display[y]
            .iter()
            .map(|x| ((*x as u8) + 48) as char)
            .map(|x| {
                if x == '1' {
                    return "#";
                } else {
                    return " ";
                }
            })
            .collect();

        println!("{}", r);
    }
}
