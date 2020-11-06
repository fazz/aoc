use std::collections::HashMap;

use regex::Regex;

pub fn exec() {

    let input = vec![
        "cpy 1 a", "cpy 1 b", "cpy 26 d", "jnz c 2", "jnz 1 5", "cpy 7 c", "inc d", "dec c",
        "jnz c -2", "cpy a c", "inc a", "dec b", "jnz b -2", "cpy c b", "dec d", "jnz d -6",
        "cpy 17 c", "cpy 18 d", "inc a", "dec d", "jnz d -2", "dec c", "jnz c -5",
    ];

    fn calc<'a>(input: & Vec<&'a str>, mut registers: HashMap<&'a str, i32>) -> i32 {
        let re = Regex::new(r"(cpy|inc|dec|jnz) ([^ ]{1,})[ ]{0,1}([^ ]{0,})").unwrap();

        let mut pc: i32 = 0;

        loop {
            let i = input.get(pc as usize);

            if i.is_none() {
                break;
            }
            let i = i.unwrap();

            let caps = re.captures(i).unwrap();

            let inst = caps.get(1).unwrap().as_str();
            let op1 = caps.get(2).unwrap().as_str();
            let op2 = caps.get(3);

            match (inst, op1, op2) {
                ("cpy", _, Some(op2)) => {
                    let ii = op1.parse::<i32>();
                    if let Ok(result) = ii {
                        registers.insert(op2.as_str(), result);
                    } else {
                        registers.insert(op2.as_str(), *registers.get(op1).unwrap());
                    }
                    pc = pc + 1
                }
                ("inc", _, _) => {
                    registers.insert(op1, registers.get(op1).unwrap() + 1);
                    pc = pc + 1;
                }
                ("dec", _, _) => {
                    registers.insert(op1, registers.get(op1).unwrap() - 1);
                    pc = pc + 1;
                }

                ("jnz", _, Some(op2)) => {
                    let flag = match op1.parse::<i32>() {
                        Ok(value) => value,
                        _ => *registers.get(op1).unwrap(),
                    };

                    if flag == 0 {
                        pc = pc + 1;
                    } else {
                        pc = pc + op2.as_str().parse::<i32>().unwrap();
                    }
                }

                _ => panic!("WTF!"),
            }
        }
        *registers.get("a").unwrap()
    }

    let mut registers: HashMap<&str, i32> = HashMap::new();

    registers.insert("a", 0);
    registers.insert("b", 0);
    registers.insert("c", 0);
    registers.insert("d", 0);

    println!("Part1: {}", calc(&input, registers));

    let mut registers: HashMap<&str, i32> = HashMap::new();

    registers.insert("a", 0);
    registers.insert("b", 0);
    registers.insert("c", 1);
    registers.insert("d", 0);

    println!("Part2: {}", calc(&input, registers));
}
