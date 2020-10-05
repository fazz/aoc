
use clap::{Arg, App};

mod common;
mod days;

fn print_type_of<T>(_: &T) {
    println!("{}", std::any::type_name::<T>())
}

fn execute(day: i32) {
    match day {
        1 => days::day01::exec(),
        2 => days::day02::exec(),
        3 => days::day03::exec(),
        4 => days::day04::exec(),
        5 => days::day05::exec(),
        6 => days::day06::exec(),
        _ => ()
    }
}

fn main() {

    let matches = App::new("AoC 2016")
    .version("1")
//    .author("Hackerman Jones <hckrmnjones@hack.gov>")
    .about("Advent of Code 2016")
    .arg(Arg::with_name("day")
             .short("d")
             .long("day")
             .takes_value(true)
             .help("Day number"))
    .get_matches();


    let day_str = matches.value_of("day");
    match day_str {
        None => (),
        Some(s) => {
            match s.parse::<i32>() {
                Ok(n) => execute(n),
                Err(_) => (),
            }
        }
    };
    
}
