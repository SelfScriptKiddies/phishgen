use colog::init;
use log::info;
use clap::Parser;
pub mod configuration;

fn main() {
    init();
    let options = configuration::Configuration::parse();
    info!("Hello, world!");
}
