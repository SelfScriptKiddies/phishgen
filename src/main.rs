use clap::Parser;
use log::LevelFilter;
use phishgen::configuration::Configuration;


fn init_logger(config: &Configuration) {
    let mut builder = colog::default_builder();
    let level = match config.logging_level.as_str() {
        "trace" => LevelFilter::Trace,
        "debug" => LevelFilter::Debug,
        "info" => LevelFilter::Info,
        "warn" => LevelFilter::Warn,
        "error" => LevelFilter::Error,
        _ => LevelFilter::Info,
    };
    builder.filter(None, level);
    builder.init();
}

fn main() {
    let options = Configuration::parse();
    init_logger(&options);
    phishgen::run(options);
}
