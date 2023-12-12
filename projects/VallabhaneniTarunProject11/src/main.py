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
    output_name = os.path.join(output_directory, file_name.replace(".jack", ".vm"))

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
        input_path = sys.argv[1]

        # Check if the input path is a directory or a single file
        if os.path.isdir(input_path):
            # Process all .jack files in the directory
            for file_name in os.listdir(input_path):
                if file_name.endswith(".jack"):
                    process_file(os.path.join(input_path, file_name))
        elif input_path.endswith(".jack"):
            # Process a single file
            process_file(input_path)
        else:
            print(
                "Invalid input. Please provide a Jack file or a directory containing Jack files."
            )
    else:
        print("Usage: python your_script.py [input_file.jack or directory]")


def process_file(input_file):
    """
    Process a single Jack file.
    Parameters:
        input_file (str): the name of the file
    """
    tokenizer = JackTokenizer(input_file)
    with open(input_file, "r") as f:
        input_lines = f.readlines()
    cleaned_lines = tokenizer.clean_file("".join(input_lines))

    output_directory = os.path.dirname(input_file)

    tokenized_output = tokenizer.tokenizer(cleaned_lines)
    output_file = write_file_tokenized(
        tokenized_output, output_directory, os.path.basename(input_file)
    )
    print(f"Tokenized file saved at {output_file}")

    compiler = JackCompiler(output_file)
    compiled_output = compiler.read_and_compile()
    output_compiled_file = write_file_compiled(
        compiled_output, output_directory, os.path.basename(input_file)
    )
    print(f"Compiled file saved at {output_compiled_file}")


if __name__ == "__main__":
    main()
