use clap::Parser;
use phishgen::configuration::Configuration;

fn main() {
    colog::init();
    let options = Configuration::parse();
    phishgen::run(options);
}
