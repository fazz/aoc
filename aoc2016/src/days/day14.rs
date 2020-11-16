use std::collections::{BTreeSet, HashMap};

use md5;
use multimap::MultiMap;

struct State {
    // char to positions
    fives: MultiMap<char, i32>,
    // position to char
    threes: HashMap<i32, char>,
    hwm: i32,
    rounds: i32
}

impl Default for State {
    fn default() -> State {
        State {
            fives: MultiMap::new(),
            threes: HashMap::new(),
            hwm: -1,
            rounds: 1,
        }
    }
}

impl State {
    fn detect3(&self, input: &str) -> Option<char> {
        let input = input.as_bytes();
        for i in 0..input.len() - 2 {
            if input[i] == input[i + 1] && input[i + 1] == input[i + 2] {
                return Some(input[i] as char);
            }
        }
        None
    }

    fn detect5(&self, input: &str) -> BTreeSet<char> {
        let mut ret = BTreeSet::new();

        let input = input.as_bytes();
        for i in 0..input.len() - 4 {
            if input[i] == input[i + 1]
                && input[i + 1] == input[i + 2]
                && input[i + 2] == input[i + 3]
                && input[i + 3] == input[i + 4]
            {
                ret.insert(input[i] as char);
            }
        }
        ret
    }
    
    fn digest(&self, index: i32) -> String {
        let input = String::from("ahsbgdzn");
        //let input = String::from("abc");

        let mut digest_str = format!("{}{}", input, index);

        for _i in 1..=self.rounds {
            digest_str = format!("{:x}", md5::compute(digest_str.as_bytes()));
        }

        digest_str
    }

    fn update(&mut self, end_index: i32) {
        for i in self.hwm + 1..=end_index {
            let digest_str = self.digest(i);

            if let Some(c) = self.detect3(&digest_str) {
                self.threes.insert(i, c);
            }

            let f = self.detect5(&digest_str);
            for c in f {
                self.fives.insert(c, i)
            }
        }

        self.hwm = end_index;
    }

    fn check(&mut self, index: i32) -> bool {
        self.update(index + 1020);
        if let Some(c) = self.threes.get(&index) {
            let d = vec![];
            let v = self.fives.get_vec(c).unwrap_or(&d);
            for p in v {
                if *p <= index + 1000 && *p > index {
                    return true;
                }
            }
        }
        false
    }
}

pub fn exec() {
    let mut index = 0;
    let mut count = 0;

    let mut state = State::default();

    while count < 64 {
        if state.check(index) {
            count += 1;
        }
        index += 1;
    }

    println!("Part1: {}", index - 1);

    let mut index = 0;
    let mut count = 0;

    let mut state = State::default();
    state.rounds = 2017;

    while count < 64 {
        if state.check(index) {
            count += 1;
        }
        index += 1;
    }

    println!("Part2: {}", index - 1);
}
