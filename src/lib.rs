use configuration::*;
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

struct Document {
    path: String,
    content: Vec<u8>,
}

fn create(args: CreateArgs) -> Result<(), std::io::Error> {    
    let document: Document = match args.command {
        CreateCommands::Empty { output_directory } => Document {
            path: format!("{}/harmless_pattern.dotx", output_directory),
            content: include_bytes!("../resources/examples/harmless_pattern.dotx").to_vec(),
        },
        CreateCommands::Full { output_directory } => Document {
            path: format!("{}/full_resume_pattern.dotx", output_directory),
            content: include_bytes!("../resources/examples/full_resume_pattern.dotx").to_vec(),
        },
        CreateCommands::FullDoc { output_directory } => Document {
            path: format!("{}/resume_document.docx", output_directory),
            content: include_bytes!("../resources/examples/resume_document.docx").to_vec(),
        },
    };

    info!("Creating document {}", document.path);

    std::fs::write(document.path, document.content)?;

    info!("Document created successfully");
    
    Ok(())
}