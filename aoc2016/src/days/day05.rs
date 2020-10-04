use md5;

pub fn exec() {
    let input = String::from("ojvtpuvg");

    fn part1(input: &String) -> String {
        let mut index = 0;

        let mut password = String::new();

        while password.len() < 8 {
            let mut hash_input = input.to_owned();
            hash_input.push_str(&index.to_string());

            let digest = md5::compute(hash_input.as_bytes());

            let x = digest.0;

            let r = match (x[0], x[1], x[2] & 0xf0) {
                (0, 0, 0) => Some(x[2]),
                _ => None,
            };
            match r {
                Some(x) => {
                    let f = format!("{:x}", x);
                    password.push_str(&f);
                }
                _ => {}
            }
            index += 1;
        }
        return password;
    }

    println!("Part1: {}", part1(&input));

    fn part2(input: &String) -> String {
        let mut index = 0;

        let mut password = ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'];
        let mut passwordfull = 0;

        while passwordfull < 8 {
            let mut hash_input = input.to_owned();
            hash_input.push_str(&index.to_string());

            let digest = md5::compute(hash_input.as_bytes());

            let x = digest.0;

            let r = match (x[0], x[1], x[2] & 0xf0) {
                (0, 0, 0) => Some(x[2]),
                _ => None,
            };
            match r {
                Some(pos) => {
                    let value = format!("{:x}", x[3] >> 4);
                    if pos <= 7 && password[pos as usize] == 'x' {
                        password[pos as usize] = value.chars().next().unwrap();
                        passwordfull += 1;
                    }
                }
                _ => {}
            }
            index += 1;
        }
        let mut result = String::new();
        password.iter().fold(&mut result, |acc, c| {
            acc.push(*c);
            return acc;
        });
        return result;
    }

    println!("Part2: {}", part2(&input));
}
