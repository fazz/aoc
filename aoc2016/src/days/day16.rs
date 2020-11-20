pub fn exec() {
    fn calc(input: &str, size: i32) -> String {
        let mut stream = vec![false; size as usize];

        for i in 0..input.len() {
            stream[i] = input.as_bytes()[i] as char == '1';
        }

        let mut filled: i32 = input.len() as i32;
        let mut i: i32 = filled - 1;

        let mut count = 0;

        while i < size {
            let mut target = 2 * filled - i;
            while i >= 0 && target < size {
                if i == 0 {
                    count += 1;
                }
                stream[target as usize] = !stream[i as usize];
                i -= 1;
                target = 2 * filled - i;
            }
            filled = 2 * filled + 1;
            i = filled - 1;
        }
        println!("count: {}", count);

        let mut clustersize = 2;
        let mut s = size / 2;
        while s % 2 == 0 {
            clustersize *= 2;
            s /= 2;
        }

        let mut i = 0;
        let mut out = vec![];
        while i < size {
            let mut v = stream[i as usize];
            for j in 1..clustersize {
                v ^= stream[(i + j) as usize];
            }
            out.push(!v);
            i += clustersize;
        }

        out.iter()
            .map(|v| if *v { '1' } else { '0' })
            .collect::<_>()
    }

    let input = "00101000101111010";

    println!("Part1: {}", calc(input, 272));
    println!("Part2: {}", calc(input, 35651584));
}
