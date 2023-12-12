class JackCompiler:
    """
    Compiles the tokenized input into a parsed list.
    """

    def __init__(self, token_input):
        self.token_input = token_input
        # list of tokens
        self.token_list = []
        self.parsed_list = []
        self.index = 0
        # indentation
        self.indent = 0

    def read_and_compile(self):
        """
        Reads the tokenized input and compiles it into a parsed list.
        """
        with open(self.token_input, mode="r") as f:
            lines = f.readlines()

            # Exclude the first and last lines
            for line in lines[1:-1]:
                self.token_list.append(line)

        self.compile_class(self.indent)
        return self.parsed_list

    def add_to_list(self, indent):
        """
        Adds the current token to the parsed list.
        Parameters:
            indent: indentation level
        """
        # make sure the index is not out of range
        if self.index < len(self.token_list):
            # add the current token to the parsed list. Make sure to add the correct indentation
            # indentation is 2 spaces per level
            self.parsed_list.append(" " * (indent + 2) + self.token_list[self.index])
            self.index += 1

    def token_only(self):
        """
        Returns the current token without the tag.
        """
        # need only the token, not the tag
        return self.token_list[self.index].split(" ")[1].strip()

    def compile_class(self, indent):
        """
        Compiles the class.
        Parameters:
            indent: indentation level
        """
        # add class tag
        self.parsed_list.append(" " * indent + "<class>")
        # add "class" keyword
        self.add_to_list(indent)
        # add class name
        self.add_to_list(indent)
        # add "{" symbol
        self.add_to_list(indent)

        # compile class var dec
        while self.index < len(self.token_list) and self.token_only().strip() in (
            "static",
            "field",
        ):
            self.compile_class_var_dec(indent + 2)

        # compile subroutine
        while self.index < len(self.token_list) and self.token_only().strip() in (
            "constructor",
            "function",
            "method",
        ):
            self.compile_subroutine(indent + 2)

        # add "}" symbol
        self.add_to_list(indent)
        # add class tag
        self.parsed_list.append(" " * indent + "</class>")

    def compile_class_var_dec(self, indent):
        """
        Compiles the class variable declaration.
        Parameters:
            indent: indentation level
        """
        # add class var dec tag
        self.parsed_list.append(" " * indent + "<classVarDec>")
        # add "static" or "field" keyword
        self.add_to_list(indent)
        # add type. Keep adding until a ";" is found
        while self.index < len(self.token_list) and ";" not in self.token_only():
            self.add_to_list(indent)
        # add ";" symbol
        self.add_to_list(indent)
        # add class var dec tag
        self.parsed_list.append(" " * indent + "</classVarDec>")

    def compile_subroutine(self, indent):
        """
        Compiles the subroutine.
        Parameters:
            indent: indentation level
        """
        # add subroutine
        self.parsed_list.append(" " * indent + "<subroutineDec>")
        # add "constructor", "function", or "method" keyword
        self.add_to_list(indent)
        # add return type
        self.add_to_list(indent)
        # add subroutine name
        self.add_to_list(indent)
        # add "(" symbol
        self.add_to_list(indent)
        # add parameter list
        self.compile_parameter_list(indent + 2)
        # add ")" symbol
        self.add_to_list(indent)
        # add subroutine body
        self.compile_subroutine_body(indent + 2)
        # add subroutine
        self.parsed_list.append(" " * indent + "</subroutineDec>")

    def compile_parameter_list(self, indent):
        """
        Compiles the parameter list.
        Parameters:
            indent: indentation level
        """
        # add parameter list tag
        self.parsed_list.append(" " * indent + "<parameterList>")
        while self.index < len(self.token_list) and ")" not in self.token_only():
            # get variable type
            self.add_to_list(indent)
            # get variable name
            self.add_to_list(indent)
            # add "," symbol
            if self.index < len(self.token_list) and "," in self.token_only():
                self.add_to_list(indent)
        # add parameter list tag
        self.parsed_list.append(" " * indent + "</parameterList>")

    def compile_subroutine_body(self, indent):
        """
        Compiles the subroutine body.
        Parameters:
            indent: indentation level
        """
        # add subroutine body tag
        self.parsed_list.append(" " * indent + "<subroutineBody>")
        # add "{" symbol
        self.add_to_list(indent)
        # add var dec (not class var dec)
        while self.index < len(self.token_list) and self.token_only() not in [
            "let",
            "do",
            "if",
            "while",
            "return",
        ]:
            self.compile_var_dec(indent + 2)
        # add statements
        if self.index < len(self.token_list) and self.token_only() in [
            "let",
            "do",
            "if",
            "while",
            "return",
        ]:
            self.compile_statements(indent + 2)

        # add "}" symbol
        self.add_to_list(indent)
        # add subroutine body tag
        self.parsed_list.append(" " * indent + "</subroutineBody>")

    def compile_var_dec(self, indent):
        """
        Compiles the variable declaration.
        Parameters:
            indent: indentation level
        """
        # add var dec tag
        self.parsed_list.append(" " * indent + "<varDec>")
        # add "var" keyword
        self.add_to_list(indent)
        # add type
        self.add_to_list(indent)
        # add var name
        self.add_to_list(indent)
        # add "," symbol
        while self.index < len(self.token_list) and ";" not in self.token_only():
            self.add_to_list(indent)
            self.add_to_list(indent)
        # add ";" symbol
        self.add_to_list(indent)
        # add var dec tag
        self.parsed_list.append(" " * indent + "</varDec>")

    def compile_statements(self, indent):
        """
        Compiles the statements.
        Parameters:
            indent: indentation level
        """
        # add statements tag
        self.parsed_list.append(" " * indent + "<statements>")
        # while loop to add statements
        while self.index < len(self.token_list) and "}" not in self.token_only():
            if self.index < len(self.token_list) and self.token_only() == "let":
                self.compile_let(indent + 2)
            elif self.index < len(self.token_list) and self.token_only() == "if":
                self.compile_if(indent + 2)
            elif self.index < len(self.token_list) and self.token_only() == "while":
                self.compile_while(indent + 2)
            elif self.index < len(self.token_list) and self.token_only() == "do":
                self.compile_do(indent + 2)
            elif self.index < len(self.token_list) and self.token_only() == "return":
                self.compile_return(indent + 2)

        # add statements tag
        self.parsed_list.append(" " * indent + "</statements>")

    def compile_let(self, indent):
        """
        Compiles the let statement.
        Parameters:
            indent: indentation level
        """
        # add let tag
        self.parsed_list.append(" " * indent + "<letStatement>")
        # add "let" keyword
        self.add_to_list(indent)
        # add var name
        self.add_to_list(indent)
        # add expression with array if there is one (add check for cursor position)
        if self.index < len(self.token_list) and "[" in self.token_only():
            # add "[" symbol
            self.add_to_list(indent)
            # add expression (indented)
            self.compile_expression(indent + 2)
            # add "]" symbol
            self.add_to_list(indent)
        # add "=" symbol
        self.add_to_list(indent)
        # add expression (indented)
        self.compile_expression(indent + 2)
        # add ";" symbol
        self.add_to_list(indent)
        # add let tag
        self.parsed_list.append(" " * indent + "</letStatement>")

    def compile_if(self, indent):
        """
        Compiles the if statement.
        Parameters:
            indent: indentation level
        """
        # add if tag
        self.parsed_list.append(" " * indent + "<ifStatement>")
        # add "if" keyword
        self.add_to_list(indent)
        # add "(" symbol
        self.add_to_list(indent)
        # add expression
        self.compile_expression(indent + 2)
        # add ")" symbol
        self.add_to_list(indent)
        # add "{" symbol
        self.add_to_list(indent)
        # add statements
        self.compile_statements(indent + 2)
        # add "}" symbol
        self.add_to_list(indent)
        # add "else" keyword if there is one
        if self.index < len(self.token_list) and self.token_only() == "else":
            self.add_to_list(indent)
            # add "{" symbol
            self.add_to_list(indent)
            # add statements
            self.compile_statements(indent + 2)
            # add "}" symbol
            self.add_to_list(indent)
        # add if tag
        self.parsed_list.append(" " * indent + "</ifStatement>")

    def compile_while(self, indent):
        """
        Compiles the while statement.
        Parameters:
            indent: indentation level
        """
        # add while tag
        self.parsed_list.append(" " * indent + "<whileStatement>")
        # add "while" keyword
        self.add_to_list(indent)
        # add "(" symbol
        self.add_to_list(indent)
        # add expression
        self.compile_expression(indent + 2)
        # add ")" symbol
        self.add_to_list(indent)
        # add "{" symbol
        self.add_to_list(indent)
        # add statements
        self.compile_statements(indent + 2)
        # add "}" symbol
        self.add_to_list(indent)
        # add while tag
        self.parsed_list.append(" " * indent + "</whileStatement>")

    def compile_do(self, indent):
        """
        Compiles the do statement.
        Parameters:
            indent: indentation level
        """
        # add do tag
        self.parsed_list.append(" " * indent + "<doStatement>")
        # add "do" keyword
        self.add_to_list(indent)
        # add subroutine call
        self.compile_subroutine_call(indent)
        # add ";" symbol
        self.add_to_list(indent)
        # add do tag
        self.parsed_list.append(" " * indent + "</doStatement>")

    def compile_return(self, indent):
        """
        Compiles the return statement.
        Parameters:
            indent: indentation level
        """
        # add return tag
        self.parsed_list.append(" " * indent + "<returnStatement>")
        # add "return" keyword
        self.add_to_list(indent)
        # add expression if there is one
        if self.index < len(self.token_list) and ";" not in self.token_only():
            self.compile_expression(indent + 2)
        # add ";" symbol
        self.add_to_list(indent)
        # add return tag
        self.parsed_list.append(" " * indent + "</returnStatement>")

    def compile_expression(self, indent):
        """
        Compiles the expression.
        Parameters:
            indent: indentation level
        """
        # add expression tag
        self.parsed_list.append(" " * indent + "<expression>")
        # add term (indented)
        self.compile_term(indent + 2)
        # add operator if there is one
        while self.index < len(self.token_list) and self.token_only() in (
            "+",
            "-",
            "*",
            "/",
            "&amp;",
            "|",
            "&lt;",
            "&gt;",
            "=",
        ):
            self.add_to_list(indent)
            # add term (indented)
            self.compile_term(indent + 2)
        # add expression tag
        self.parsed_list.append(" " * indent + "</expression>")

    def compile_subroutine_call(self, indent):
        """
        Compiles the subroutine call.
        Parameters:
            indent: indentation level
        """
        # must check the next token to see if it is a "." or "("
        if (self.index + 1) < len(self.token_list) and "." in self.token_list[
            self.index + 1
        ].split(" ")[1].strip():
            # add class name or variable name
            self.add_to_list(indent)
            # add "." symbol
            self.add_to_list(indent)

        # add subroutine name
        self.add_to_list(indent)
        # add "(" symbol
        self.add_to_list(indent)
        # add expression list
        self.compile_expression_list(indent + 2)
        # add ")" symbol
        self.add_to_list(indent)

    def compile_expression_list(self, indent):
        """
        Compiles the expression list.
        Parameters:
            indent: indentation level
        """
        # add expression list tag
        self.parsed_list.append(" " * indent + "<expressionList>")
        # add expression if there is one
        while self.index < len(self.token_list) and ")" not in self.token_only():
            self.compile_expression(indent + 2)
            # add "," symbol and expression
            while self.index < len(self.token_list) and "," in self.token_only():
                # add "," symbol
                self.add_to_list(indent)
                # add expression
                self.compile_expression(indent + 2)

        # add expression list tag
        self.parsed_list.append(" " * indent + "</expressionList>")

    def compile_term(self, indent):
        """
        Compiles the term.
        Parameters:
            indent: indentation level
        """
        # add term tag
        self.parsed_list.append(" " * indent + "<term>")
        # check if the next token is a square bracket
        if (self.index + 1) < len(self.token_list) and "[" in self.token_list[
            self.index + 1
        ].split(" ")[1].strip():
            # add var name
            self.add_to_list(indent)
            # add "[" symbol
            self.add_to_list(indent)
            # add expression
            self.compile_expression(indent + 2)
            # add "]" symbol
            self.add_to_list(indent)
        # check if the term is a unary operator
        elif self.index < len(self.token_list) and self.token_only() in ("-", "~"):
            # add unary operator
            self.add_to_list(indent)
            # add term
            self.compile_term(indent + 2)
        # check if the expression and term are in parentheses
        elif self.index < len(self.token_list) and "(" in self.token_only():
            # add "(" symbol
            self.add_to_list(indent)
            # add expression
            self.compile_expression(indent + 2)
            # add ")" symbol
            self.add_to_list(indent)
        # check if the term is a subroutine call
        elif (self.index + 1) < len(self.token_list) and self.token_list[
            self.index + 1
        ].split(" ")[1].strip() in ("(", "."):
            # add subroutine call
            self.compile_subroutine_call(indent)

        # if none of the above, add the term
        else:
            self.add_to_list(indent)
        # add term tag
        self.parsed_list.append(" " * indent + "</term>")
