import re


class JackTokenizer:
    """
    Converts the Jack language file into a tokenized output.
    """

    def __init__(self, input_file):
        """
        Initializes the JackParser object.
        Parameters:
            input_file (str): the name of the file
        """

        self.input_file = input_file
        self.token_dict = {
            "keyword": [
                "class",
                "constructor",
                "function",
                "method",
                "field",
                "static",
                "var",
                "int",
                "char",
                "boolean",
                "void",
                "true",
                "false",
                "null",
                "this",
                "let",
                "do",
                "if",
                "else",
                "while",
                "return",
            ],
            "symbol": [
                "{",
                "}",
                "(",
                ")",
                "[",
                "]",
                ".",
                ",",
                ";",
                "+",
                "-",
                "*",
                "/",
                "&",
                "|",
                "<",
                ">",
                "=",
                "~",
            ],
            "integerConstant": range(0, 32768),
        }

    def clean_file(self, input_file):
        """
        Cleans the file by removing comments and whitespaces.
        Parameters:
            input_file (str): the name of the file
        """

        # remove comments and whitespaces
        single_line_comment = r"//.*"

        multi_line_comment = r"/\*\*?.*?\*/"

        text = re.sub(pattern=single_line_comment, repl="", string=input_file)
        text = re.sub(pattern=multi_line_comment, repl="", string=text, flags=re.DOTALL)
        lines = text.splitlines()
        for i, line in enumerate(lines):
            lines[i] = line.strip()
        lines = [line for line in lines if line]

        return lines

    def tokenizer(self, input_file):
        """
        Parses the file into the XML format.
        Parameters:
            input_file (str): the name of the file
        """

        tokenized_list = ["<tokens>"]
        for line in input_file:
            # current code token
            current_token = ""
            # check if string constant
            string_constant = False

            spec_symbols = {
                "<": "&lt;",
                ">": "&gt;",
                "&": "&amp;",
            }

            for char in line:
                if char == '"':
                    # check if string constant is already open or not
                    string_constant = not string_constant

                if char != " ":
                    if char in self.token_dict["symbol"]:
                        # check if token is a keyword
                        if current_token in self.token_dict["keyword"]:
                            tokenized_list.append(
                                f"<keyword> {current_token} </keyword>"
                            )
                        # check if token is an integer constant
                        elif (
                            current_token.isdigit()
                            and int(current_token) in self.token_dict["integerConstant"]
                        ):
                            tokenized_list.append(
                                f"<integerConstant> {current_token} </integerConstant>"
                            )
                        # check if token is a string constant and if both quotes are present
                        elif (
                            current_token
                            and current_token[-1] == '"'
                            and not string_constant
                        ):
                            tokenized_list.append(
                                "<stringConstant> "
                                + current_token.split('"')[1]
                                + " </stringConstant>"
                            )
                        elif current_token:
                            tokenized_list.append(
                                f"<identifier> {current_token} </identifier>"
                            )
                        # reset token if any of the above conditions are met
                        current_token = ""
                        # otherwise add the symbol to the tokenized list
                        if char in spec_symbols:
                            tokenized_list.append(
                                f"<symbol> {spec_symbols[char]} </symbol>"
                            )
                        else:
                            tokenized_list.append(f"<symbol> {char} </symbol>")
                    else:
                        current_token += char
                else:
                    # bug fix for space in string constant
                    if current_token and string_constant:
                        current_token += char
                        # move on to next character
                        continue
                    if current_token:
                        if current_token in self.token_dict["keyword"]:
                            tokenized_list.append(
                                f"<keyword> {current_token} </keyword>"
                            )
                        # check if token is an integer constant
                        elif (
                            current_token.isdigit()
                            and int(current_token) in self.token_dict["integerConstant"]
                        ):
                            tokenized_list.append(
                                f"<integerConstant> {current_token} </integerConstant>"
                            )
                            # check if token is a string constant and if both quotes are present
                        elif (
                            current_token
                            and current_token[-1] == '"'
                            and not string_constant
                        ):
                            tokenized_list.append(
                                "<stringConstant> "
                                + current_token.split('"')[1]
                                + " </stringConstant>"
                            )

                        elif current_token:
                            tokenized_list.append(
                                f"<identifier> {current_token} </identifier>"
                            )
                    # reset token if any of the above conditions are met
                    current_token = ""

        tokenized_list.append("</tokens>")
        return tokenized_list
