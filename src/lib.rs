use configuration::{Configuration, Commands, InjectArgs, MacroArgs, CreateArgs};
use log::{debug, error, info};
pub mod configuration;

pub fn run(config: Configuration) {
    debug!("Running with config: {:?}", config);
    let result = match config.command {
        Commands::Inject(args) => inject(args),
        Commands::Macro(args) => generate_macro(args),
        Commands::Create(args) => create(args)
    };
    if let Err(e) = result {
        error!("{}", e);
    }
}

fn inject(args: InjectArgs) -> Result<(), std::io::Error> {
    info!("Injecting macro to document");
    Ok(())
}

fn generate_macro(args: MacroArgs) -> Result<(), std::io::Error> {
    info!("Generating macro");
    Ok(())
}

fn create(args: CreateArgs) -> Result<(), std::io::Error> {
    info!("Creating document");
    Ok(())
}