
use std;
use std::cmp::{min, max};

pub fn exec() {

    let input = "L2, L5, L5, R5, L2, L4, R1, R1, L4, R2, R1, L1, L4, R1, L4, L4, R5, R3, R1, L1, R1, L5, L1, R5, L4, R2, L5, L3, L3, R3, L3, R4, R4, L2, L5, R1, R2, L2, L1, R3, R4, L193, R3, L5, R45, L1, R4, R79, L5, L5, R5, R1, L4, R3, R3, L4, R185, L5, L3, L1, R5, L2, R1, R3, R2, L3, L4, L2, R2, L3, L2, L2, L3, L5, R3, R4, L5, R1, R2, L2, R4, R3, L4, L3, L1, R3, R2, R1, R1, L3, R4, L5, R2, R1, R3, L3, L2, L2, R2, R1, R2, R3, L3, L3, R4, L4, R4, R4, R4, L3, L1, L2, R5, R2, R2, R2, L4, L3, L4, R4, L5, L4, R2, L4, L4, R4, R1, R5, L2, L4, L5, L3, L2, L4, L4, R3, L3, L4, R1, L2, R3, L2, R1, R2, R5, L4, L2, L1, L3, R2, R3, L2, L1, L5, L2, L1, R4,";

    let mut x = 0;
    let mut y = 0;

    let mut dx = 0;
    let mut dy = 1;
    let mut d = 0;

    let mut xp2 = None;
    let mut yp2 = None;
    let mut p2found = false;

    const SIZE: usize = 400;
    const OFFSET: i32 = 200;

    let mut state = [[0u8; SIZE]; SIZE];

    fn os(c: i32) -> usize {
        (c + OFFSET) as usize
    }

    for c in input.chars() { 
        match c {
            'L' => {let tmp = dx; dx = -dy; dy = tmp},
            'R' => {let tmp = dx; dx = dy; dy = -tmp},
            ',' => {

                if !p2found {
                    for i in min(0, d*dx)..max(0, d*dx)+1 {
                        for j in min(0, d*dy)..max(0, d*dy)+1 {
                            if (i != 0 || j != 0) && state[os(x+i)][os(y+j)] != 0 {
                                p2found = true;
                                xp2 = Some(x + i);
                                yp2 = Some(y + j);
                            }
                            state[os(x+i)][os(y+j)] = 1;
                        }
                    }
                }

                x = x+d*dx;
                y = y+d*dy;
                d = 0
            },
            ' ' => (),
            _ => match c.to_string().parse::<i32>() {
                Ok(n) => {d = d*10+n},
                Err(_) => ()
            }
        };
    };

    println!("Part1: {:?}", x.abs() + y.abs());
    match (xp2, yp2) {
        (Some(x), Some(y)) => println!("Part2: {:?}", x.abs() + y.abs()),
        _ => panic!("No P2")
    }
    
}

