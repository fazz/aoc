
use crate::common;

pub fn exec() {
    let input = common::lines_from_file("input09.txt");

    //let input = vec!["(27x12)(20x12)(13x14)(7x10)(1x12)A"];

    let mut part1 = 0;
    let mut part2 = 0;

    fn calc(chars: &[char], expand: bool) -> u64 {
        let mut inprefix = false;
        let mut charcount = true;

        let mut output = 0;

        let mut cc: usize = 0;
        let mut rc: u64 = 0;

        let mut i = 0;

        while i < chars.len() {
            // -> extraskip, outputcount
            let (es, oc) = match (chars[i], inprefix, charcount) {
                ('(', false, _) => {
                    inprefix = true;
                    charcount = true;
                    cc = 0;
                    rc = 0;
                    (0, 0)
                }

                ('0'..='9', true, true) => {
                    cc = cc * 10 + (chars[i] as usize - '0' as usize);
                    (0, 0)
                }

                ('x', true, true) => {
                    charcount = false;
                    (0, 0)
                }

                ('0'..='9', true, false) => {
                    rc = rc * 10 + (chars[i] as u64 - '0' as u64);
                    (0, 0)
                }

                (')', true, false) => {
                    inprefix = false;

                    let ocr: u64;
                    if !expand {
                        ocr = cc as u64 * rc;
                    } else {
                        // part2
                        //ocr = cc as u32 * rc;
                        ocr = calc(&chars[i + 1..i + 1 + cc], true) * rc;
                    }

                    (cc, ocr)
                }

                (_, false, _) => (0, 1),

                _ => panic!("WTF!"),
            };

            output += oc;
            i += es + 1;
        }
        output
    }

    for line in input {
        let chars: Vec<char> = line.chars().collect();

        println!("{}", chars.len());

        part1 = calc(&chars, false);
        part2 = calc(&chars, true);
    }

    println!("Part1: {:?}", part1);
    println!("Part2: {:?}", part2);
}
