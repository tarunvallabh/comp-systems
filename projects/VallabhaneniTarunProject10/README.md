# Jack Language Compiler - Part 1 (Syntax Analysis)

This tool is a comprehensive Python application designed to translate and compile programs written in the Jack language. It first tokenizes the Jack language file into an XML format and then compiles this tokenized output into a parsed XML list.

## Prerequisites
Ensure you have Python 3.11.4 or a compatible version installed on your system.

## Structure and Usage

### Components
- `JackTokenizer`: Converts Jack language files into a tokenized output in XML format.
- `JackCompiler`: Compiles the tokenized input into a parsed XML list.
- `Main Program`: Orchestrates the process of tokenization and compilation, handling file input/output operations.

### Running the Program:

1. **Prepare the Input File:**
   - Save the Jack code in a file with a `.jack` extension.

2. **Executing the Program:**
   - Open the terminal or command prompt and navigate to the directory containing the script.
   - Run the program using the command:
     ```
     python main.py <input_file.jack>
     ```
   - Replace `<input_file.jack>` with the path to your Jack file.

3. **Output:**
   - The tokenizer and compiler will process the input file and generate two output files in the same directory:
     - A tokenized version with a `T.xml` extension.
     - A compiled version with a `.xml` extension.

## Features
- **JackTokenizer:**
  - Removes comments and whitespace for clean processing.
  - Identifies and categorizes keywords, symbols, and constants.

- **JackCompiler:**
  - Handles class, subroutine, variable declarations, and statements.
  - Compiles expressions and terms accurately.

- **Main Program:**
  - Validates input files and directories.
  - Manages file writing operations for tokenized and compiled outputs.

## Testing and Limitations
- The code has undergone extensive testing for accuracy and reliability.
- A variety of Jack programs were used for testing, and the output XML files were compared against the XML files provided by the nand2tetris course using the text comparator tool (also provided by the nand2tetris course).
- It correctly handles various Jack language constructs.
- The current implementation is tailored for `.jack` files and outputs XML files.
- There are no known limitations in the code. 

**Note:** Ensure Python 3.11.4 is installed and use a Jack file as the command-line argument for successful execution.
