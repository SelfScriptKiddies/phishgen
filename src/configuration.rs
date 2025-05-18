use clap::{Parser, Subcommand};


#[derive(Parser, Debug)]
#[command(version, about, long_about = None, subcommand_help_heading = "Available Subcommands", disable_help_subcommand = true)]
pub struct Configuration {
    #[arg(short, long)]
    pub verbose: bool,

    #[arg(short='l', long="logging-level", help="Logging level (trace|debug|info|warn|error)", help_heading = "Logging", default_value = "info")]
    pub logging_level: String,

    #[command(subcommand)]
    pub command: Commands,
}

#[derive(Subcommand, Debug)]
pub enum Commands {
    Inject(InjectArgs),
    Macro(MacroArgs),
    Create(CreateArgs),
}

#[derive(Parser, Debug)]
pub struct InjectArgs {
    #[arg(value_parser)]
    pub input_docx_file: String,

    // TODO: inject macro to document, implement not remote injection technique
    #[arg(value_parser)]
    pub macro_path: String,

    #[arg(short, long, default_value = "patched_document.docx")]
    pub output_docx_file: String,
}

#[derive(Parser, Debug)]
pub struct MacroArgs {
    #[arg(short='f', long="file", required_unless_present="source_code")]
    pub input_file: Option<String>,

    #[arg(short='s', long, required_unless_present="input_file")]
    pub source_code: Option<String>,
}

#[derive(Parser, Debug)]
pub struct CreateArgs {
    #[command(subcommand)]
    pub command: CreateCommands,
}

#[derive(Subcommand, Debug)]
pub enum CreateCommands {
    Empty {
        #[arg(short='d', long, default_value = ".")]
        output_directory: String,
    },

    Full {
        #[arg(short='d', long, default_value = ".")]
        output_directory: String
    },

    #[command(name="fulldoc")]
    FullDoc {
        #[arg(short='d', long, default_value = ".")]
        output_directory: String
    },
}

