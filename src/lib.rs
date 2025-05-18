use configuration::*;
use log::{debug, error, info};
pub mod configuration;

pub fn run(config: Configuration) {
    debug!("Running with config: {:?}", config);
    let result = match config.command {
        Commands::Inject(args) => Inject::inject(args),
        Commands::Macro(args) => Macro::generate_macro(args),
        Commands::Create(args) => Create::create(args)
    };
    if let Err(e) = result {
        error!("{}", e);
    }
}

#[allow(non_snake_case)]
mod Inject {
    use super::*;
    use tempfile::Builder;
    
    pub fn inject(args: InjectArgs) -> Result<(), std::io::Error> {
        info!("Mode inject");

        let temp_dir = Builder::new()
            .prefix("phishgen")
            .tempdir()?;
        debug!("Created temporary directory: {:?}", temp_dir.path());

        let input_path = std::path::Path::new(&args.input_docx_file);
        let temp_input_path = temp_dir.path().join(input_path.file_name().unwrap());
        
        debug!("Copying input file \"{}\" to temp directory", input_path.display());
        std::fs::copy(input_path, &temp_input_path)?;
        debug!("Input file copied to: {:?}", temp_input_path);

        Ok(())
    } 
}


#[allow(non_snake_case)]
mod Macro {
    use super::*;

    pub fn generate_macro(args: MacroArgs) -> Result<(), std::io::Error> {
        info!("Generating macro");
        Ok(())
    }
}

#[allow(non_snake_case)]
mod Create {
    use super::*;
    
    struct Document {
        path: String,
        content: Vec<u8>,
    }
    
    pub fn create(args: CreateArgs) -> Result<(), std::io::Error> {
        info!("Mode create");
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
}

