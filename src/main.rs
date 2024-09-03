use clap::{arg, command, Arg, Command};

use std::io::{self, stdin, Read};
use std::time::Duration;

struct FakeFrontmatter {
    title: String,
    author: String,
    categories: Vec<String>,
}

fn main() -> io::Result<()> {
    let cmd = command!()
        .subcommand_required(true)
        .subcommand(command!("create"))
        .subcommand(command!("sync"))
        .subcommand(command!("discard"))
        .subcommand(command!("abort"));

    let matches = cmd.get_matches();

    println!("Enter your input here: ");
    let input = read_line().unwrap();

    Ok(())
}

fn read_line() -> io::Result<String> {
    let mut buf = String::new();
    stdin().read_line(&mut buf)?;
    //Remove the trailing newline from the user submitting input
    buf = buf[0..buf.len() - 1].to_string();
    Ok(buf)
}
