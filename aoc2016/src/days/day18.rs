pub fn exec() {
    let input = "^..^^.^^^..^^.^...^^^^^....^.^..^^^.^.^.^^...^.^.^.^.^^.....^.^^.^.^.^.^.^.^^..^^^^^...^.....^....^.";

    // true == safe
    let start = input.chars().map(|x| x == '.').collect::<Vec<_>>();

    fn sum(input: &Vec<bool>) -> i32 {
        input.iter().filter(|x| **x).count() as i32
    }

    fn calculate(input: Vec<bool>) -> Vec<bool> {
        let mut ret = Vec::with_capacity(input.len());

        let prev = |i: i32| -> bool {
            if i < 0 || i >= input.len() as i32 {
                true
            } else {
                input[i as usize]
            }
        };
        for i in 0..input.len() as i32 {
            let trap = prev(i - 1) ^ prev(i + 1);
            ret.push(!trap);
        }
        ret
    }

    fn iterate(mut prev: Vec<bool>, rows: i32) -> i32 {
        let mut ret = sum(&prev);

        for _x in 1..rows {
            let current = calculate(prev);
            ret += sum(&current);
            prev = current;
        }
        ret
    }

    println!("Part1: {}", iterate(start.clone(), 40));
    println!("Part2: {}", iterate(start, 400000));
}
