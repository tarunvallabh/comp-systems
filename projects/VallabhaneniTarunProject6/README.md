# Assembler for the Hack Computer- Project 6

This is a Python program for translating programs written in the Hack Assembly Language into machine code, the native language of the Hack computer.

## Prerequisites
Make sure you have Python 3.11.4 installed on your system. You can download Python from the official website.

## Instructions for Compiling and Running the Program

**1. Compiling the Code:**
- Compilation is not required as the code is written in Python
- The code has been tested with Python 3.11.4, and it should work with any compatible version.

**2. Running the Program:**

- Prepare an input file containing the Hack Assembly Language program that you want to assemble. Save it with a .asm file extension.

- Open your terminal or command prompt and navigate to the directory where the script (```assembler.py```) is located.

- Use the following command to execute the program:

    ```
    python assembler.py <input_file>
    ```
-  Replace `<input_file>` with the path to your input file. - If the input file is located in a different directory, be sure to provide the absolute path to the file. For example:
    ```
    python assembler.py input_file.in
    ```
- The assembler will generate an output file in the same directory as the input file. The output file will have the same name as the input file but with a .hack extension. This file contains the assembled machine code.

## What the Assembler Does

- **Pass 1:** The assembler reads the input file and removes comments and whitespace. 

- **Pass 2:** The program then identifies and processes labels, adding them to the symbol table. Labels are removed from the program text to avoid issues during translation.

- **Pass 3:** The program processes each line and translates it into machine code. A-instructions and C-instructions are translated into their binary machine code representation and written to the output file. 

- **Symbol Table**: The assembler maintains a symbol table containing predefined symbols for registers and memory locations. It also adds user-defined labels to the symbol table, ensuring that they are correctly referenced in the program.

## Testing
- There are no known errors in the code or limitations in functionality.
- The assembler has been tested with sample programs to ensure correct functionality. The programs used for testing were: 

    - ```add.asm```: Computes R0 = 2 + 3.

    - ```max.asm```: Finds the maximum value of R0 and R1, storing the result in R2.

    - ```Rect.asm```: Draws a rectangle in the top-left corner of the screen. The rectangle's height is determined by the value in R0.

    - ```Pong.asm```: Demonstrates the assembly capabilities by playing the game Pong.

    - ```mult.asm```: Multiplies the values in R0 and R1, saving the result in R2.

    - ```fill.asm```: Listens for keyboard input and takes action. When a key is pressed, the program blacks out the screen from the top, and it clears the screen in reverse when no key is pressed.

$~$

**Note**: Please ensure that you have Python 3.11.4 installed and that the input file is provided as a command-line argument when running the assembler. Otherwise, the assmbler will throw an error.











