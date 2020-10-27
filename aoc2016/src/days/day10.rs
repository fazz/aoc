use std::collections::HashMap;

use regex::Regex;

use crate::common;

#[derive(PartialEq, Eq, Hash, Debug)]
struct Dst<'a> {
    dst_id: &'a str,
    first: bool,
    output: bool,
}

pub fn exec() {
    #[derive(PartialEq, Eq, Hash, Debug)]
    enum SrcType {
        BotHigh,
        BotLow,
        Input,
    }

    #[derive(PartialEq, Eq, Hash, Debug)]
    struct Src<'a> {
        src_id: &'a str,
        src_type: &'a SrcType,
        value: Option<i32>,
    }

    #[derive(Clone, Debug)]
    struct Bot {
        one: Option<i32>,
        two: Option<i32>,
    }

    impl Bot {
        fn high(&self) -> Option<i32> {
            if self.one.is_some() && self.two.is_some() {
                if self.one > self.two {
                    return self.one;
                } else {
                    return self.two;
                }
            } else {
                return None;
            }
        }
        fn low(&self) -> Option<i32> {
            if self.one.is_some() && self.two.is_some() {
                if self.one < self.two {
                    return self.one;
                } else {
                    return self.two;
                }
            } else {
                return None;
            }
        }
        fn set(&mut self, value: i32) {
            if self.one.is_none() {
                self.one = Some(value)
            } else if self.two.is_none() {
                self.two = Some(value)
            } else {
                panic!("WTF!")
            }
        }
    }

    type BotMap<'a> = HashMap<&'a str, Bot>;
    let mut bots: BotMap = HashMap::new();

    fn setinput<'a, 'b>(bot_id: &'a str, value: i32, rules: &'b mut HashMap<Dst<'a>, Src>) {
        let first = !rules.contains_key(&Dst {
            dst_id: bot_id,
            first: true,
            output: false,
        });

        rules.insert(
            Dst {
                dst_id: &bot_id,
                first: first,
                output: false,
            },
            Src {
                src_id: "input",
                src_type: &SrcType::Input,
                value: Some(value),
            },
        );
    }

    fn split<'a, 'b>(
        src_id: &'a str,
        high_id: &'a str,
        h_output: bool,
        low_id: &'a str,
        l_output: bool,
        rules: &'b mut HashMap<Dst<'a>, Src<'a>>,
    ) {
        let first = h_output
            || !rules.contains_key(&Dst {
                dst_id: high_id,
                first: true,
                output: false,
            });

        rules.insert(
            Dst {
                dst_id: high_id,
                first: first,
                output: h_output,
            },
            Src {
                src_id: src_id,
                src_type: &SrcType::BotHigh,
                value: None,
            },
        );

        let first = l_output
            || !rules.contains_key(&Dst {
                dst_id: low_id,
                first: true,
                output: false,
            });

        rules.insert(
            Dst {
                dst_id: low_id,
                first: first,
                output: l_output,
            },
            Src {
                src_id: src_id,
                src_type: &SrcType::BotLow,
                value: None,
            },
        );
    }

    let mut rules: HashMap<Dst, Src> = HashMap::new();

    // Load

    let input = common::lines_from_file("input10.txt");

    let reinput = Regex::new(r"value (\d{1,}) goes to bot (\d{1,})").unwrap();
    let resplit = Regex::new(
        r"bot (\d{1,}) gives low to (output|bot) (\d{1,}) and high to (output|bot) (\d{1,})",
    )
    .unwrap();

    for line in input.iter() {
        let capsinput = reinput.captures(line);
        let capssplit = resplit.captures(line);

        if let Some(i) = capsinput {
            setinput(
                i.get(2).unwrap().as_str(),
                i.get(1).unwrap().as_str().parse::<i32>().unwrap(),
                &mut rules,
            );
        } else if let Some(s) = capssplit {
            let high = s.get(5).unwrap().as_str();
            let low = s.get(3).unwrap().as_str();

            let h_output = s.get(4).unwrap().as_str() == "output";
            let l_output = s.get(2).unwrap().as_str() == "output";

            split(
                s.get(1).unwrap().as_str(),
                high,
                h_output,
                low,
                l_output,
                &mut rules,
            );
        } else {
            panic!("WTF!");
        }
    }

    // Drop mutability
    let rules = rules;

    fn calculate<'a, 'b>(
        dst_id: &'a str,
        output: bool,
        bots: &mut BotMap<'a>,
        rules: &'a HashMap<Dst<'a>, Src<'a>>,
    ) -> (Option<&'a str>, i32, i32) {
        // part1, high, low

        if !output {
            if let Some(b) = bots.get(dst_id) {
                return (None, b.high().unwrap(), b.low().unwrap());
            }
        }

        let find_src = |dst_id: &str, output: bool, first: bool| {
            let r = rules
                .get(&Dst {
                    dst_id: dst_id,
                    first: first || output,
                    output: output,
                })
                .unwrap();

            (r.src_type, r.src_id, r.value)
        };

        let one = find_src(dst_id, output, true);
        let two = find_src(dst_id, output, false);

        let mut newbot = Bot {
            one: None,
            two: None,
        };

        for source in [one, two].iter() {
            let (src_type, src_id, dir_value) = source;

            let (solution, value) = match src_type {
                SrcType::Input => (None, dir_value.unwrap()),
                SrcType::BotHigh | SrcType::BotLow => {
                    let (solution, src_high, src_low) = calculate(src_id, false, bots, rules);
                    match src_type {
                        SrcType::BotHigh => (solution, src_high),
                        SrcType::BotLow => (solution, src_low),
                        _ => panic!("WTF"),
                    }
                }
            };
            if output {
                return (None, value, 0);
            }

            newbot.set(value);

            if let Some(_s) = solution {
                return (solution, 0, 0);
            }
        }

        match (newbot.high(), newbot.low()) {
            (Some(h), Some(l)) => {
                bots.insert(dst_id, newbot);
                match (h, l) {
                    (61, 17) => (Some(dst_id), h, l),
                    _ => (None, h, l),
                }
            }
            _ => panic!("WTF"),
        }
    };

    let mut part1 = "NOT FOUND";

    let botlist: Vec<&str> = rules.keys().map(|x| x.dst_id).collect();

    for k in botlist {
        let (result, _high, _low) = calculate(k, false, &mut bots, &rules);

        if let Some(r) = result {
            part1 = r;
            break;
        }
    }

    println!("Part1: {}", part1);

    let (_result, h0, _low) = calculate("0", true, &mut bots, &rules);
    let (_result, h1, _low) = calculate("1", true, &mut bots, &rules);
    let (_result, h2, _low) = calculate("2", true, &mut bots, &rules);

    println!("Part2: {}", h0 * h1 * h2);
}
