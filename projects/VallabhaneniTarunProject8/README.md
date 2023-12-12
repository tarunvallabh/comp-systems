# Virtual Machine (VM) Translator (Full-Scale) - Part 2

The VM Translator is a Python program designed to translate programs written in the Hack Virtual Machine (VM) language into assembly code, which is the native language of the Hack computer. This is an updated version of the previous Virtual Machine Translator that now handles program flow and function calls. 

## Prerequisites
Ensure Python 3.11.4 or a compatible version is installed on your system. You can download Python from the official website.

## Compiling and Running the Program

### Compiling the Code:
- No compilation is necessary since the code is written in Python.
- The code has been tested with Python 3.11.4 and is expected to work with other compatible versions.

### Running the Program:

**1. Prepare the Input Files:**

- For a single file: Save the VM code in a file with a .vm file extension.
- For multiple files in a directory: Create a directory containing the .vm files.

**2. Executing the Program**
- Open your terminal or command prompt and navigate to the directory containing the main.py script.

- Execute the program using the following command:

    ```
    python main.py <input_file_or_directory>
    ```
- Replace `<input_file_or_directory>` with the path to your input file. If the file is located in a different directory, provide the absolute path. For example:
    ```
    python main.py /path/to/your/input_file_or_directory
    ```
- The translator will generate an output file within the specified directory (if the input is a directory) or the same directory as the input file (if the input is a file). The output file will have the same name as the input file but with a .asm extension, containing the translated assembly code.

## Translation Process
1. **Translation from a Directory:**

- If the provided input is a directory containing a Sys.vm file, the translator appends the assembly code of all .vm files into a single output file. It adds a Bootstrap code and a call to the "Sys.init" function at the beginning of the file. After processing all .vm files, it writes an infinite loop at the end of the output file. The output file is the placed within the input directory. 
- If the provided input is a directory without a Sys.vm file, the bootstrap code is not added to the output file. After processing the .vm file, it again writes an infinite loop at the end of the output file. The output file is the placed within the input directory. 

2. **Translation from a File:**

- For a single .vm file, it reads the input file, processes it, and writes the assembly code to a single output file. The output file is stored in the same directory as the input file. 
- Similar to translation from a directory, it adds an infinite loop at the end of the output file.

## Testing

- The code has been rigorously tested to ensure accuracy and reliability.
- A variety of VM programs contained in input directories were used for testing, ensuring the translator functions correctly with various command types.
- There are no known flaws in the program. All output .asm files were tested succesfully on the provided CPU emulator. 

## Limitations

- Due to errors in processing the following expressions, "AM = M-1" and "AM = M+1" by the CPU Emulator provided, the lines were split into two lines of code: "M = M-1" followed by "A = M", and "M = M+1" followed by "A = M" respectively. Though this makes the code slighlty more inefficient by adding a tiktok, it was necessary to allow the CPU emulator to read the output assembly files for testing. 

**Note:** Python 3.11.4 should be installed, and the input file must be provided as a command-line argument for the translator to run successfully.
