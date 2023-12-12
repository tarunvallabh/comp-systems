import re
import os
import sys

symbol_table = {
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
    "R0": 0,
    "R1": 1,
    "R2": 2,
    "R3": 3,
    "R4": 4,
    "R5": 5,
    "R6": 6,
    "R7": 7,
    "R8": 8,
    "R9": 9,
    "R10": 10,
    "R11": 11,
    "R12": 12,
    "R13": 13,
    "R14": 14,
    "R15": 15,
    "SCREEN": 16384,
    "KBD": 24576,
}

dest_table = {
    "null": "000",
    "M": "001",
    "D": "010",
    "MD": "011",
    "A": "100",
    "AM": "101",
    "AD": "110",
    "AMD": "111",
}

jump_table = {
    "null": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111",
}

comp_table = {
    "0": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000",
    "!D": "0001101",
    "!A": "0110001",
    "-D": "0001111",
    "-A": "0110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "D|A": "0010101",
    "M": "1110000",
    "!M": "1110001",
    "-M": "1110011",
    "M+1": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "D|M": "1010101",
}


def make_binary(num):
    """
    Makes a 16-bit binary number from a decimal number
    Parameter num: the decimal number to be converted
    """
    binary = ""
    while num > 0:
        binary = str(num % 2) + binary
        num = num // 2
    while len(binary) < 16:
        # makes sure the binary number is 16 bits long
        binary = "0" + binary
    return binary


def dest(string):
    """
    Returns the dest mnemonic from the line inputted
    Parameter string: the c-instruction
    """
    if string.__contains__("="):
        # splits string at the = and returns the first part
        return string.split("=")[0].strip()
    else:
        return "null"


def comp(string):
    """
    Returns the comp mnemonic from the line inputted
    Parameter string: the c-instruction
    """
    if string.__contains__("="):
        # splits string at the = and returns the second part
        return string.split("=")[1].strip()
    elif string.__contains__(";"):
        # splits string at the ; and returns the first part
        return string.split(";")[0].strip()
    else:
        return "null"


def jump(string):
    """
    Returns the jump mnemonic from the line inputted
    Parameter string: the c-instruction
    """
    if string.__contains__(";"):
        # splits string at the ; and returns the second part
        return string.split(";")[1].strip()
    else:
        return "null"


def check_at_sign(string):
    """
    Returns the string after the @
    Parameter string: the a-instruction
    """
    if string.__contains__("@"):
        # splits string at the @ and returns the second part
        return string.split("@")[1].strip()


def convert_jump(string):
    """
    Converts the jump mnemonic to binary
    Parameter string: the jump mnemonic
    """
    return jump_table[jump(string)]


def convert_dest(string):
    """
    Converts the dest mnemonic to binary
    Parameter string: the dest mnemonic
    """
    return dest_table[dest(string)]


def convert_comp(string):
    """
    Converts the comp mnemonic to binary
    Parameter string: the comp mnemonic
    """
    return comp_table[comp(string)]


def convert_at_sign_numeric(string):
    """
    Converts the at sign to binary
    Parameter string: the a-instruction
    """
    a = check_at_sign(string)
    if a.isnumeric():
        return make_binary(int(a))


def convert_c_instruction(string):
    """
    Converts the c-instruction to binary
    Parameter string: the c-instruction
    """
    return "111" + convert_comp(string) + convert_dest(string) + convert_jump(string)


def assembler(input_file):
    """
    Assembles the input file in the asm language to a binary file in the hack language
    Parameter input_file: the input file to be processed
    """
    try:
        # in case executable is not in same directory
        # reference: https://docs.python.org/3/library/os.path.html#module-os.path
        input_file = os.path.abspath(input_file)
        # make sure directory is the same
        # reference: https://docs.python.org/3/library/os.path.html#module-os.path
        input_directory, input_filename = os.path.split(input_file)

        # open input file
        with open(input_file, "r") as infile:
            doc = infile.read()

        # Pass 1: remove comments and whitespace

        # define regex for single-line and multi-line comments
        # reference: https://www.programiz.com/python-programming/regex
        # reference: https://docs.python.org/3/library/re.html
        single_line_comment = r"//.*"
        multi_line_comment = r"/\*.*?\*/"

        # remove single-line comments
        # reference: https://www.pythontutorial.net/python-regex/python-regex-sub/
        text = re.sub(pattern=single_line_comment, repl="", string=doc)

        # remove multi-line comments. Include the flag in order to account for new line spaces in the multi line comment
        # when removing them
        # reference: https://www.pythontutorial.net/python-regex/python-regex-sub/
        text = re.sub(pattern=multi_line_comment, repl="", string=text, flags=re.DOTALL)

        # remove whitespace
        text = text.replace(" ", "")

        # remove leading and trailing whitespace from lines
        lines = text.splitlines()
        for i, line in enumerate(lines):
            lines[i] = line.strip()

        # Modified after testing: remove blank lines after comments are removed
        lines = [line for line in lines if line]

        # Pass 2: add labels to the symbol table and remove them from the program

        # have a new list of lines without labels to avoid skipping lines
        lines_without_labels = []

        for line in lines:
            if "(" in line:
                # Extract the label
                symb = line[1:-1]
                # Add the symbol to the symbol table with the adjusted index of the line
                symbol_table[symb] = len(lines_without_labels)
            else:
                # For lines that are not labels, add them to the new list
                lines_without_labels.append(line)

        # Pass 3: go through the program and translate each line to binary

        output_list = []
        # counter to keep track of memory location for new symbols
        counter = 0
        for line in lines_without_labels:
            # if the line is a c-instruction
            if line.__contains__("=") or line.__contains__(";"):
                output_list.append(convert_c_instruction(line))
            # if line is an a-instruction and a symbol in the symbol table
            elif check_at_sign(line) in symbol_table.keys():
                output_list.append(make_binary(symbol_table[check_at_sign(line)]))
            # if line is an a-instruction and a numeric value.
            # Modified after testing: make sure the value is not None
            elif check_at_sign(line) is not None and check_at_sign(line).isnumeric():
                output_list.append(convert_at_sign_numeric(line))
            # if line is an a-instruction and a new symbol
            elif check_at_sign(line) not in symbol_table.keys():
                counter += 1
                # add the symbol to the symbol table to the register after R15
                symbol_table[check_at_sign(line)] = 15 + counter
                # convert the symbol to binary
                output_list.append(make_binary(symbol_table[check_at_sign(line)]))

        # create an output file
        output_file = os.path.join(
            input_directory, input_filename.replace(".asm", ".hack")
        )

        # Write the output file with the content
        with open(output_file, "w") as outfile:
            outfile.write("\n".join(output_list))

        # success message indicating that the outfile was created
        print(f"Output file '{output_file}' created.")

    except FileNotFoundError:
        # add an error message if there are issues reading the file
        print(f"Error: Input file '{input_file}' not found.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Please retry as follows: python assembler.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    assembler(input_file)
