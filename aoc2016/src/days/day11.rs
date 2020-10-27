use std::collections::BTreeMap;
use std::collections::BTreeSet;
use std::collections::HashMap;
use std::{cmp::Ordering, collections::vec_deque::VecDeque};

pub fn exec() {
    let input_chip1: HashMap<i32, Vec<&str>> = [
        (1, vec!["Pr"]),
        (2, vec![]),
        (3, vec!["Co", "Cu", "Ru", "Pl"]),
        (4, vec![]),
    ]
    .iter()
    .cloned()
    .collect();

    let input_chip2: HashMap<i32, Vec<&str>> = [
        (1, vec!["Pr", "El", "Di"]),
        (2, vec![]),
        (3, vec!["Co", "Cu", "Ru", "Pl"]),
        (4, vec![]),
    ]
    .iter()
    .cloned()
    .collect();

    let input_generator1: HashMap<i32, Vec<&str>> = [
        (1, vec!["Pr"]),
        (2, vec!["Co", "Cu", "Ru", "Pl"]),
        (3, vec![]),
        (4, vec![]),
    ]
    .iter()
    .cloned()
    .collect();

    let input_generator2: HashMap<i32, Vec<&str>> = [
        (1, vec!["Pr", "El", "Di"]),
        (2, vec!["Co", "Cu", "Ru", "Pl"]),
        (3, vec![]),
        (4, vec![]),
    ]
    .iter()
    .cloned()
    .collect();

    #[derive(Clone)]
    struct Step<'a> {
        step: i32,
        state: &'a State<'a>,
    }

    #[derive(PartialEq, PartialOrd, Eq, Hash, Clone, Debug)]
    struct State<'a> {
        floor: i32,
        // (chip, generator)
        elements: BTreeMap<&'a str, (i32, i32)>,
    }

    impl<'a> Ord for State<'a> {
        fn cmp(&self, other: &Self) -> Ordering {
            if self.floor < other.floor {
                return Ordering::Less;
            }
            if self.floor > other.floor {
                return Ordering::Greater;
            }
            fn order(v: &State) -> Vec<(i32, i32)> {
                let mut values = vec![];
                for e in v.elements.values() {
                    values.push(*e);
                    values.sort_by(|a, b| a.cmp(b));
                }
                values
            }
            let so = order(self);
            let oo = order(other);

            so.cmp(&oo)
        }
    }

    impl<'a> State<'a> {
        fn move_chip(&mut self, element: &'a str, to_floor: &i32) {
            self.elements
                .entry(element)
                .and_modify(|v| *v = (*to_floor, v.1));
        }

        fn move_gen(&mut self, element: &'a str, to_floor: &i32) {
            self.elements
                .entry(element)
                .and_modify(|v| *v = (v.0, *to_floor));
        }

        fn validate(&self) -> Option<&State> {
            for (element, floors) in self.elements.iter() {
                if floors.0 == floors.1 {
                    continue;
                }
                for (element2, floors2) in self.elements.iter() {
                    if element != element2 {
                        if floors.0 == floors2.1 {
                            return None;
                        }
                    }
                }
            }
            Some(self)
        }

        fn isfinal(&self) -> bool {
            for e in self.elements.values() {
                if e.0 != 4 || e.1 != 4 {
                    return false;
                }
            }
            true
        }
    }

    struct Element<'a> {
        name: &'a str,
        empty: bool,
        chip: bool,
    }

    trait Movable<'a> {
        fn move_element(&self, tf: &i32, state: &mut State<'a>);
    }

    impl<'a> Movable<'a> for Element<'a> {
        fn move_element(&self, tf: &i32, state: &mut State<'a>) {
            if !self.empty {
                if self.chip {
                    state.move_chip(self.name, tf);
                } else {
                    state.move_gen(self.name, tf);
                }
            }
        }
    }

    fn calculate<'a>(mut queue: VecDeque<Step<'a>>, traversed: BTreeSet<State<'a>>) -> i32 {
        let step = queue.pop_front().unwrap();
        let state = step.state;

        // Drag their lifetime here
        let mut queue = queue;
        let mut traversed = traversed;

        let next_states = find_options(&state, &mut traversed);

        for newstate in next_states.iter() {
            if newstate.isfinal() {
                return step.step + 1;
            }

            traversed.insert(newstate.clone());

            queue.push_back(Step {
                step: step.step + 1,
                state: &newstate,
            });
        }

        calculate(queue, traversed)
    }

    fn moves<'a: 'b, 'b>(
        nextfloor: &i32,
        state: &'a State<'a>,
        options: &Vec<(&Box<dyn Movable<'a> + 'a>, &Box<dyn Movable<'a> + 'a>)>,
        traversed: &mut BTreeSet<State<'b>>,
    ) -> Vec<State<'b>> {
        let mut result = vec![];

        for option in options {
            let mut newstate = state.clone();

            option.0.move_element(&nextfloor, &mut newstate);
            option.1.move_element(&nextfloor, &mut newstate);

            newstate.floor = *nextfloor;

            if !traversed.contains(&newstate) {
                if let Some(_v) = newstate.validate() {
                    // Mark traversed as early as possible
                    traversed.insert(newstate.clone());
                    result.push(newstate);
                }
            }
        }

        result
    }

    fn find_options<'a>(
        state: &'a State<'a>,
        traversed: &mut BTreeSet<State<'a>>,
    ) -> Vec<State<'a>> {
        {
            let mut elements: Vec<Box<dyn Movable>> = vec![];

            for (name, floors) in state.elements.iter() {
                if floors.0 == state.floor {
                    elements.push(Box::new(Element {
                        name: name,
                        chip: true,
                        empty: false,
                    }));
                }
                if floors.1 == state.floor {
                    elements.push(Box::new(Element {
                        name: name,
                        chip: false,
                        empty: false,
                    }));
                }
            }

            elements.push(Box::new(Element {
                name: "empty",
                chip: false,
                empty: true,
            }));

            let l = elements.len();

            let elements = elements;

            let mut q: Vec<(&Box<dyn Movable>, &Box<dyn Movable>)> = vec![];

            for i in 0..l {
                let a = elements.get(i).unwrap();
                for j in i + 1..l {
                    let b = elements.get(j).unwrap();
                    q.push((a, b));
                }
            }

            let mut up = vec![];
            let mut down = vec![];
            if state.floor < 4 {
                up = moves(&(state.floor + 1), state, &q, traversed);
            }

            if state.floor > 1 {
                down = moves(&(state.floor - 1), state, &q, traversed);
            }

            up.append(&mut down);

            up
        }
    }

    fn calc(
        input_chip: HashMap<i32, std::vec::Vec<&str>>,
        input_generator: HashMap<i32, std::vec::Vec<&str>>,
    ) -> i32 {
        let mut queue: VecDeque<Step> = VecDeque::new();
        let mut traversed: BTreeSet<State> = BTreeSet::new();

        let mut state = State {
            floor: 1,
            elements: BTreeMap::new(),
        };

        for (floor, elements) in input_chip {
            for n in elements {
                state.elements.entry(n).or_insert((floor, -1));
            }
        }

        for (floor, elements) in input_generator {
            for n in elements {
                let e = *state.elements.get(n).unwrap();
                state.elements.insert(n, (e.0, floor));
            }
        }

        queue.push_back(Step {
            step: 0,
            state: &state,
        });

        traversed.insert(state.clone());

        calculate(queue, traversed)
    }

    println!("Part1: {}", calc(input_chip1, input_generator1));
    println!("Part2: {}", calc(input_chip2, input_generator2));
}
