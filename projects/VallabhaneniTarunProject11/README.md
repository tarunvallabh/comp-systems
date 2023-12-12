# Jack Language Compiler - Part 2 (Code Generation)

This Python application translates and compiles programs written in the Jack language. It performs syntax analysis by tokenizing Jack language files into XML format and then compiling this tokenized output into Virtual Machine (VM) code.

## Prerequisites
Ensure you have Python 3.11.4 or a compatible version installed on your system.

## Structure and Usage

### Components
- JackTokenizer: Transforms Jack language files into a tokenized XML format.
- JackCompiler: Parses the tokenized input and compiles it into VM code.
- VMWriter: Generates VM commands from the compiled output.
- ClassSymbolTable and SubroutineSymbolTable: Manage symbol tables for classes and subroutines.
- Main Program: Coordinates the tokenization and compilation process, handling file input/output operations.


### Running the Program:

1. **Prepare the Input File:**
   - Save the Jack code in a file with a `.jack` extension.

2. **Executing the Program:**
   - Open the terminal or command prompt and navigate to the script's directory.
   - Run the program using the command:
     ```
     python main.py <input_path>
     ```
   - Replace <input_path> with the path to your Jack file or directory. 

3. **Output:**
   - The tokenizer and compiler will process each file and generate two output files in the same directory for each:
     - A tokenized version with a `T.xml` extension.
     - A compiled version with a `.vm` extension.

## Features
- **JackTokenizer:**
  - Removes comments and whitespace for clean processing.
  - Identifies and categorizes keywords, symbols, and constants.

- **JackCompiler:**
  - Handles class, subroutine, variable declarations, and statements.
  - Compiles expressions and terms accurately.

- **VMWriter**: 
    - Translates compiled code into VM commands.
    - Manages VM command syntax.

- **SymbolTable**: 
    - Track and manage variable and subroutine scopes.

- **Main Program:**
  - Supports individual .jack files and directories containing multiple .jack files.
  - Manages file writing operations for tokenized and compiled outputs.

## Testing and Limitations
- The code has undergone extensive testing for accuracy and reliability.
- A variety of Jack programs were used for testing, and all of the compiled code output files were tested on the VMEmulator tool provided by the nand2tetris course. 
- Handles a wide range of Jack language constructs.
- Outputs XML and VM file formats.
- There are no known limitations in the code. 

**Note:** Python 3.11.4 is required. The program accepts a Jack file or a directory containing Jack files as the command-line argument for successful execution.
