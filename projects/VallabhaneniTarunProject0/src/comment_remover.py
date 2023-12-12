import sys
import os
import re


def remove_comments_and_whitespace(input_file):
    """
    Removes single line and multi line comments and whitespace from a given input file
    and creates an output file in the same directory.

    Parameter input_file: the input file to be processed
    Return: None
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

        # remove leading and trailing whitespace from lines
        lines = text.splitlines()
        for i, line in enumerate(lines):
            lines[i] = line.strip()

        # Modified after testing: remove blank lines after comments are removed
        lines = [line for line in lines if line]

        # create an output file
        output_file = os.path.join(
            input_directory, input_filename.replace(".in", ".out")
        )

        # Write the output file with the content
        with open(output_file, "w") as outfile:
            outfile.write("\n".join(lines))

        # success message indicating that the outfile was created
        print(f"Output file '{output_file}' created.")

    except FileNotFoundError:
        # add an error message if there are issues reading the file
        print(f"Error: Input file '{input_file}' not found.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Please retry as follows: python comment_remover.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    remove_comments_and_whitespace(input_file)
