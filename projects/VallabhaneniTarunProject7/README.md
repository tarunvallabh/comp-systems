# Virtual Machine (VM) Translator

The VM Translator is a Python program designed to translate programs written in the Hack Virtual Machine (VM) language into assembly code, which is the native language of the Hack computer.

## Prerequisites
Ensure Python 3.11.4 or a compatible version is installed on your system. You can download Python from the official website.

## Compiling and Running the Program

**1. Compiling the Code:**
- No compilation is necessary since the code is written in Python.
- The code has been tested with Python 3.11.4 and is expected to work with other compatible versions.

**2. Running the Program:**

- Prepare an input file containing the VM code that you wish to translate. Save it with a .vm file extension.
- Open your terminal or command prompt and navigate to the directory where the `main.py` script is located.

- Execute the program using the following command:

    ```
    python main.py <input_file>
    ```
- Replace `<input_file>` with the path to your input file. If the file is located in a different directory, provide the absolute path. For example:
    ```
    python main.py input_file.vm
    ```
- The translator will generate an output file in the same directory as the input file. The output file will have the same name as the input file but with a .asm extension, containing the translated assembly code.

## Translation Process

- **Parsing and Cleaning:** The program first reads the input file, removes comments, and eliminates whitespace to create a structured set of commands.

- **Processing and Translation:** The VM code is parsed and processed according to its operation type. Operations such as arithmetic commands and memory access instructions are converted to their corresponding assembly code.

## Testing

- The code has been rigorously tested to ensure accuracy and reliability.
- A variety of VM programs were used for testing, ensuring the translator functions correctly with various command types.
- There are no known flaws in the program. All output .asm files were tested succesfully on the provided CPU emulator. 

## Limitations

- Due to errors in processing the following expression : "AM = M-1" by the CPU Emulator provided, the line was split into two lines of code: "M = M-1" followed by "A = M". Though this makes the code slighlty more inefficient by adding a tiktok, it was necessary to allow the CPU emulator to read the output assembly files for testing. 

**Note:** Python 3.11.4 should be installed, and the input file must be provided as a command-line argument for the translator to run successfully.
