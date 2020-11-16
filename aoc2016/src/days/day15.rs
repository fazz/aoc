
pub fn exec() {

    let input = vec![
        (1, 17, 5),
        (2, 19, 8),
        (3, 7, 1),
        (4, 13, 7),
        (5, 5, 1),
        (6, 3, 0),
    ];

    let input2 = vec![
        (1, 17, 5),
        (2, 19, 8),
        (3, 7, 1),
        (4, 13, 7),
        (5, 5, 1),
        (6, 3, 0),
        (7, 11, 0),
    ];

    fn calc(input: &Vec<(i32, i32, i32)>) -> i32 {
        let mut max = 0;
        let mut maxi = 0;
        for i in 0..input.len() {
            let v = input[i];
            if v.1 > max {
                max = v.1;
                maxi = i;
            }
        }

        let mut value = (-input[maxi].0 - input[maxi].2) % input[maxi].1;
        let step = input[maxi].1;

        loop {
            let mut found = true;
            for i in input {
                if (i.0 + i.2 + value) % i.1 != 0 {
                    found = false;
                    break;
                }
            }
            if found {
                break;
            }
            value += step;
        }
        value
    }

    println!("Part1: {}", calc(&input));
    println!("Part2: {}", calc(&input2));
}
