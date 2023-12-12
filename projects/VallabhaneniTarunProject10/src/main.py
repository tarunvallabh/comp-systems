import sys
import os
from JackTokenizer import JackTokenizer
from JackCompiler import JackCompiler


def write_file_tokenized(input_list, output_directory, file_name):
    """
    Writes the tokenized output to a file.
    Parameters:
        input_list (list): the tokenized output
        output_directory (str): the directory to write the file to
        file_name (str): the name of the file
    """
    output_name = os.path.join(output_directory, file_name.replace(".jack", "T.xml"))

    with open(output_name, "w") as f:
        for line in input_list:
            f.write(line + "\n")

    return output_name


def write_file_compiled(input_list, output_directory, file_name):
    """
    Writes the compiled output to a file.
    Parameters:
        input_list (list): the compiled output
        output_directory (str): the directory to write the file to
        file_name (str): the name of the file
    """
    output_name = os.path.join(output_directory, file_name.replace(".jack", ".xml"))

    with open(output_name, "w") as f:
        for line in input_list:
            if line.endswith("\n"):
                f.write(line)
            else:
                f.write(line + "\n")

    return output_name


def main():
    """
    Main function to run the tokenizer and compiler.
    """
    if len(sys.argv) == 2:
        input_file = sys.argv[1]

        # Check if the input file is a Jack file
        if input_file.endswith(".jack"):
            # Create an instance of JackTokenizer
            tokenizer = JackTokenizer(input_file)

            # Read and clean the input file
            with open(input_file, "r") as f:
                input_lines = f.readlines()

            cleaned_lines = tokenizer.clean_file("".join(input_lines))

            # Determine the output directory within the same folder as the input file
            output_directory = os.path.dirname(input_file) + "/output"

            # Create the output directory if it doesn't exist
            if not os.path.exists(output_directory):
                os.makedirs(output_directory)

            # Parse the cleaned input and get tokenized output
            tokenized_output = tokenizer.tokenizer(cleaned_lines)

            # Write the tokenized output to an T.XML file in the same directory
            output_file = write_file_tokenized(
                tokenized_output, output_directory, os.path.basename(input_file)
            )
            print(f"Tokenized file saved at {output_file}")

            # compile the tokenized output
            compiler = JackCompiler(output_file)
            compiled_output = compiler.read_and_compile()

            # Write the compiled output to an XML file in the same directory
            output_compiled_file = write_file_compiled(
                compiled_output, output_directory, os.path.basename(input_file)
            )

            print(f"Compiled file saved at {output_compiled_file}")
        else:
            print("Invalid input file. Please provide a Jack file.")
    else:
        print("Usage: python your_script.py input_file.jack")


if __name__ == "__main__":
    main()
