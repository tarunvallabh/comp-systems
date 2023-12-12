from lookupdict import LookupDicts
from vmparser import VMParser
import os
import sys


def translate_vm_directory(input_directory, output_file):
    """
    Opens the input directory and appends the output file with the assembly code of all .vm files.
    Parameters:
        input_directory (str): the name of the input directory
        output_file (str): the name of the output file
    """
    try:
        lookup = LookupDicts()
        output_path = os.path.join(
            input_directory, output_file
        )  # File path with input_directory

        # check the number of vm files in the directory
        vm_files = [
            file for file in os.listdir(input_directory) if file.endswith(".vm")
        ]

        # keep the file open and append to it
        with open(output_path, "a") as outfile:
            # Bug fix: Only if there are multiple vm files, add the bootstrap code
            if len(vm_files) > 1:
                # Adding bootstrap code to the output file
                set_pointer = lookup.bootstrap_code()
                call_code = lookup.write_call("Sys.init", 0, 1)

                # Convert the list to strings and write to the output file
                outfile.write("\n".join(set_pointer + call_code) + "\n")

            # iterate through all files in the directory, parse them and write to output files
            for file in os.listdir(input_directory):
                if file.endswith(".vm"):
                    input_file = os.path.join(input_directory, file)
                    with open(input_file, "r") as infile:
                        doc = infile.read()

                    # parse the file and write to output file
                    parser = VMParser()
                    cleaned_file = parser.clean_file(doc)
                    parsed_file = parser.parsed_command(
                        cleaned_file, file.replace(".vm", "")
                    )

                    for elem in parsed_file:
                        outfile.write(elem + "\n")

            # Adding infinite loop to the output file
            for elem in ["(END)", "@END", "0;JMP"]:
                outfile.write(elem + "\n")

        print(f"Output file '{output_file}' created.")

    except FileNotFoundError:
        print(f"Error: Input directory '{input_directory}' not found.")


def translate_vm_file(input_file, output_file):
    """
    Opens the input file and creates the output file with the assembly code.
    Parameters:
        input_file (str): the name of the file
        output_file (str): the name of the output file
    """
    try:
        input_file = os.path.abspath(input_file)
        # make sure directory is the same
        input_directory, input_filename = os.path.split(input_file)

        with open(input_file, "r") as infile:
            doc = infile.read()

        parsefile_name = input_filename.replace(".vm", "")
        parser = VMParser()
        cleaned_file = parser.clean_file(doc)
        parsed_file = parser.parsed_command(cleaned_file, parsefile_name)

        with open(output_file, "a") as outfile:
            for elem in parsed_file:
                outfile.write(elem + "\n")

            # Write the infinite loop (required after testing)
            for elem in ["(END)", "@END", "0;JMP"]:
                outfile.write(elem + "\n")

        print(f"Output file '{output_file}' created.")

    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")


def main():
    """
    Main function that takes in the input file and calls the open_file function.
    """
    if len(sys.argv) != 2:
        print("Please retry as follows: python main.py <input_file>")
        sys.exit(1)

    file_to_open = sys.argv[1]
    file_directory, file_name = os.path.split(file_to_open)

    if os.path.isdir(file_to_open):
        # make sure the output file is inside the input directory
        output_file = os.path.join(
            file_to_open, f"{os.path.basename(file_to_open)}.asm"
        )
        # remove the output file if it already exists
        if os.path.exists(output_file):
            os.remove(output_file)

        translate_vm_directory(file_to_open, output_file)

    # if the input is an individual file
    else:
        # make sure the output file is in the same directory as the input file
        output_file = os.path.join(file_directory, file_name.replace(".vm", ".asm"))
        # remove the output file if it already exists
        if os.path.exists(output_file):
            os.remove(output_file)

        translate_vm_file(file_to_open, output_file)


if __name__ == "__main__":
    main()
