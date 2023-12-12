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
        Tokenizes the input file.
        Parameters:
            input_file (str): the name of the file
        """
        tokenized_list = ["<tokens>"]
        string_constant = False  # Flag for string constant
        current_token = ""

        spec_symbols = {
            "<": "&lt;",
            ">": "&gt;",
            "&": "&amp;",
        }

        for line in input_file:
            for char in line:
                if char == '"' and not string_constant:
                    # Start of a string constant
                    string_constant = True
                    current_token = char
                elif char == '"' and string_constant:
                    # End of a string constant
                    current_token += char
                    tokenized_list.append(
                        f"<stringConstant> {current_token[1:-1]} </stringConstant>"
                    )
                    string_constant = False
                    current_token = ""
                elif string_constant:
                    # Inside a string constant
                    current_token += char
                else:
                    # Regular token processing
                    if char != " " and not string_constant:
                        if char in self.token_dict["symbol"]:
                            if current_token:
                                # Handle the token before the symbol
                                self.process_token(current_token, tokenized_list)
                                current_token = ""
                            # Add the symbol token
                            tokenized_symbol = spec_symbols.get(char, char)
                            tokenized_list.append(
                                f"<symbol> {tokenized_symbol} </symbol>"
                            )
                        else:
                            current_token += char
                    elif char == " " and current_token:
                        # Token ended by space
                        self.process_token(current_token, tokenized_list)
                        current_token = ""

        # Handle any remaining token
        if current_token:
            self.process_token(current_token, tokenized_list)

        tokenized_list.append("</tokens>")
        return tokenized_list

    def process_token(self, token, tokenized_list):
        """
        Processes and adds a token to the tokenized list.
        """
        if token in self.token_dict["keyword"]:
            tokenized_list.append(f"<keyword> {token} </keyword>")
        elif token.isdigit() and int(token) in self.token_dict["integerConstant"]:
            tokenized_list.append(f"<integerConstant> {token} </integerConstant>")
        elif token:
            tokenized_list.append(f"<identifier> {token} </identifier>")
