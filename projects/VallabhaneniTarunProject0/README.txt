-----------------------------------------
Comment and Whitespace Remover - Project 0
-----------------------------------------

**Instructions for Compiling and Running the Program:**

1. Compiling the Code:
   - Compilation is not required as the code is written in Python
   - Make sure you have Python 3.11.4 installed on your system. You can download Python from the official website. 
   - The code has been tested with Python 3.11.4, and it should work with any compatible version.

2. Running the Program:
   - Open your terminal or command prompt.
   - Navigate to the directory where the script (comment_remover.py) is located.

   I) To Remove Comments and Whitespace from a File:
   - Use the following command to execute the program and remove comments and whitespace from an input file:

     ```
     python comment_remover.py <input_file>
     ```

 - Replace `<input_file>` with the path to your input file. - If the input file is located in a different directory, be sure to provide the absolute path to the file. For example:

     ```
     python comment_remover.py input_file.in
     ```

- This will generate an output file with the same name as the input file but with the ".out" extension in the same directory as the input file.

** What Works and What Doesn't:**

- Works:
  - The program successfully removes both single-line (indicated by //) and multi-line (indicated by /* and */) comments from the input file.
  - It removes leading and trailing whitespace from lines.
  - It removes blank lines that may result from comment removal.
  - The output file is saved in the same directory as the input file, as specified.

- Doesn't Work:
  - No known errors in the code. 

Please make sure Python 3.11.4 is already installed on your computer, and that the input file is provided as a command-line argument. Otherwise, the script will throw an error. 