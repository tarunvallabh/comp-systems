from VMWriter import VMWriter
from SymbolTable import ClassSymbolTable, SubroutineSymbolTable


class JackCompiler:
    """
    Compiles the tokenized input into a parsed list.
    """

    def __init__(self, token_input):
        """
        Initializes the JackCompiler object.
        Parameters:
            token_input (str): the name of the tokenized input file
        """
        self.token_input = token_input
        # list of tokens
        self.token_list = []
        self.parsed_list = []
        self.index = 0
        # indentation
        self.indent = 0
        # add the symbol tables
        self.jack_class = None
        self.jack_subroutine = None
        # add the VMWriter
        self.vm_writer = VMWriter()
        self.final_vm_code = []
        self.label_counter = 0

    def generate_label(self, label):
        """
        Generates a label for the VM code.
        Parameters:
            label: the label to be generated
        """
        self.label_counter += 1
        return f"{label}_{self.label_counter}"

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
        return self.final_vm_code

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

        # Extract the whole line at the current index
        line = self.token_list[self.index]

        # Check if the line contains a string constant
        if "<stringConstant>" in line:
            # Extract the string constant by removing the XML tags
            # Assumes that the string constant is properly enclosed in <stringConstant> tags
            string_constant = line.split("<stringConstant>")[1].split(
                "</stringConstant>"
            )[0]

            return string_constant.strip('"')
        else:
            # For other types of tokens, extract the token value
            return line.split(" ")[1].strip()

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
        class_name = self.token_only()
        self.jack_class = ClassSymbolTable(class_name)

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
        var_kind = self.token_only()
        self.add_to_list(indent)
        # Get variable type
        var_type = self.token_only()
        self.add_to_list(indent)
        # add type. Keep adding until a ";" is found
        while self.index < len(self.token_list) and ";" not in self.token_only():
            var_name = self.token_only()
            self.add_to_list(indent)
            if var_kind == "static":
                self.jack_class.add_static_var(var_name, var_type)
            elif var_kind == "field":
                self.jack_class.add_field_var(var_name, var_type)
            if self.index < len(self.token_list) and "," in self.token_only():
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
        subroutine_type = self.token_only()
        self.add_to_list(indent)
        # add return type
        subroutine_return = self.token_only()
        self.add_to_list(indent)
        # add subroutine name
        subroutine_name = self.token_only()
        self.add_to_list(indent)

        # add subroutine symbol table
        self.jack_subroutine = SubroutineSymbolTable(
            self.jack_class.class_name,
            subroutine_type,
            subroutine_return,
            subroutine_name,
        )
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
            var_type = self.token_only()
            self.add_to_list(indent)
            # get variable name
            var_name = self.token_only()
            self.add_to_list(indent)

            self.jack_subroutine.add_arg(var_name, var_type)
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

        # function f nVars (MUST HAVE AN OUTPUT LIST)
        self.final_vm_code.extend(self.vm_writer.write_function(self.jack_subroutine))
        if self.jack_subroutine.subroutine_type == "constructor":
            # get the number of fields
            n_fields = self.jack_class.n_field_symbols
            self.final_vm_code.extend(self.vm_writer.write_push("constant", n_fields))
            # allocate memory for the object
            self.final_vm_code.extend(self.vm_writer.write_call("Memory", "alloc", 1))
            # pop the address of the object into THIS
            self.final_vm_code.extend(self.vm_writer.write_pop("pointer", 0))

        elif self.jack_subroutine.subroutine_type == "method":
            # push the address of the object into THIS
            self.final_vm_code.extend(self.vm_writer.write_push("argument", 0))
            self.final_vm_code.extend(self.vm_writer.write_pop("pointer", 0))

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
        var_type = self.token_only()
        self.add_to_list(indent)
        # add var name
        var_name = self.token_only()
        self.jack_subroutine.add_var(var_name, var_type)
        self.add_to_list(indent)
        # add "," symbol
        while self.index < len(self.token_list) and ";" not in self.token_only():
            self.add_to_list(indent)
            var_name = self.token_only()
            self.jack_subroutine.add_var(var_name, var_type)
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
        var_name = self.token_only()
        symbol_info = self.jack_subroutine.get_symbol_info(
            var_name
        ) or self.jack_class.get_symbol_info(var_name)

        self.add_to_list(indent)

        # add expression with array if there is one (add check for cursor position)
        if self.index < len(self.token_list) and "[" in self.token_only():
            # add "[" symbol
            self.add_to_list(indent)
            # add expression (indented)
            self.compile_expression(indent + 2)
            # add "]" symbol
            self.add_to_list(indent)

            self.final_vm_code.extend(
                self.vm_writer.write_push(symbol_info["kind"], symbol_info["id"])
            )
            self.final_vm_code.append("add")
            # add "=" symbol
            self.add_to_list(indent)
            # add expression (indented)
            self.compile_expression(indent + 2)
            self.final_vm_code.extend(self.vm_writer.write_pop("temp", 0))
            self.final_vm_code.extend(self.vm_writer.write_pop("pointer", 1))
            self.final_vm_code.extend(self.vm_writer.write_push("temp", 0))
            self.final_vm_code.extend(self.vm_writer.write_pop("that", 0))
        else:
            # add "=" symbol
            self.add_to_list(indent)
            # add expression (indented)
            self.compile_expression(indent + 2)
            self.final_vm_code.extend(
                self.vm_writer.write_pop(symbol_info["kind"], symbol_info["id"])
            )

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

        label_if_true = self.generate_label("IF_TRUE")
        label_if_end = self.generate_label("IF_END")

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
        # add goto if true
        self.final_vm_code.extend(self.vm_writer.write_if(label_if_true))
        # Generate VM code for goto to end if condition is false
        label_if_false = self.generate_label("IF_FALSE")
        self.final_vm_code.extend(self.vm_writer.write_goto(label_if_false))

        # Generate VM code for if true
        self.final_vm_code.extend(self.vm_writer.write_label(label_if_true))

        # add "{" symbol
        self.add_to_list(indent)

        # add statements
        self.compile_statements(indent + 2)
        # add "}" symbol
        self.add_to_list(indent)
        # Generate VM code for goto to end of if-else construct
        self.final_vm_code.extend(self.vm_writer.write_goto(label_if_end))

        # add "else" keyword if there is one
        self.final_vm_code.extend(self.vm_writer.write_label(label_if_false))

        if self.index < len(self.token_list) and self.token_only() == "else":
            self.add_to_list(indent)
            # add "{" symbol
            self.add_to_list(indent)
            # add statements
            self.compile_statements(indent + 2)
            # add "}" symbol
            self.add_to_list(indent)

        # Generate VM code for end of if-else construct
        self.final_vm_code.extend(self.vm_writer.write_label(label_if_end))

        # add if tag
        self.parsed_list.append(" " * indent + "</ifStatement>")

    def compile_while(self, indent):
        """
        Compiles the while statement.
        Parameters:
            indent: indentation level
        """
        label_while_start = self.generate_label("WHILE_EXP")
        label_while_end = self.generate_label("WHILE_END")

        # VM code for while start (label for start of expression evaluation)
        self.final_vm_code.extend(self.vm_writer.write_label(label_while_start))

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

        # VM code for if the condition is false, jump to end of while loop
        self.final_vm_code.append("not")

        self.final_vm_code.extend(self.vm_writer.write_if(label_while_end))

        # add statements (body of the while loop)
        self.compile_statements(indent + 2)

        # VM code to go back to the start of the while loop (re-evaluate condition)
        self.final_vm_code.extend(self.vm_writer.write_goto(label_while_start))

        # add "}" symbol
        self.add_to_list(indent)

        # VM code for the end of the while loop (label for loop exit)
        self.final_vm_code.extend(self.vm_writer.write_label(label_while_end))

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
        # VM code for do
        self.final_vm_code.extend(self.vm_writer.write_pop("temp", 0))
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
        else:
            # if there is no expression, push 0
            self.final_vm_code.extend(self.vm_writer.write_push("constant", 0))

        self.final_vm_code.extend(self.vm_writer.write_return())

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
            # add operator
            operator = self.token_only()
            self.add_to_list(indent)
            # add term (indented)
            self.compile_term(indent + 2)
            # VM code for operator
            self.final_vm_code.extend(self.vm_writer.write_arithmetic(operator))
        # add expression tag
        self.parsed_list.append(" " * indent + "</expression>")

    def compile_subroutine_call(self, indent):
        """
        Compiles the subroutine call.
        Parameters:
            indent: indentation level
        """
        num_args = 0
        next_token = (
            self.token_list[self.index + 1]
            if (self.index + 1) < len(self.token_list)
            else ""
        )

        if (self.index + 1) < len(self.token_list) and "." in next_token:
            # add class name or variable name
            class_or_var_name = self.token_only()
            self.add_to_list(indent)
            # add "." symbol
            self.add_to_list(indent)
            symbol_info = self.jack_subroutine.get_symbol_info(
                class_or_var_name
            ) or self.jack_class.get_symbol_info(class_or_var_name)

            if symbol_info:
                class_name = symbol_info["type"]
                self.final_vm_code.extend(
                    self.vm_writer.write_push(symbol_info["kind"], symbol_info["id"])
                )
                num_args += 1  # Method call on an object
            else:
                class_name = class_or_var_name  # Function call

            # add subroutine name
            subroutine_name = self.token_only()
            self.add_to_list(indent)
        else:
            # Method call within the same class
            class_name = self.jack_class.class_name
            subroutine_name = self.token_only()
            self.add_to_list(indent)
            self.final_vm_code.extend(self.vm_writer.write_push("pointer", 0))
            num_args += 1

        # add "(" symbol
        self.add_to_list(indent)
        # add expression list
        num_args += self.compile_expression_list(indent + 2)
        # add ")" symbol
        self.add_to_list(indent)

        self.final_vm_code.extend(
            self.vm_writer.write_call(class_name, subroutine_name, num_args)
        )

    def compile_expression_list(self, indent):
        """
        Compiles the expression list.
        Parameters:
            indent: indentation level
        """
        num_expressions = 0
        # add expression list tag
        self.parsed_list.append(" " * indent + "<expressionList>")
        # add expression if there is one
        if self.index < len(self.token_list) and ")" not in self.token_only():
            self.compile_expression(indent + 2)
            num_expressions += 1
            # add "," symbol and expression
            while self.index < len(self.token_list) and "," in self.token_only():
                # add "," symbol
                self.add_to_list(indent)
                # add expression
                self.compile_expression(indent + 2)
                num_expressions += 1

        # add expression list tag
        self.parsed_list.append(" " * indent + "</expressionList>")
        return num_expressions

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
            var_name = self.token_only()
            self.add_to_list(indent)
            # add "[" symbol
            self.add_to_list(indent)
            # add expression
            self.compile_expression(indent + 2)
            # add "]" symbol
            self.add_to_list(indent)

            # Generate VM code for array indexing
            symbol_info = self.jack_subroutine.get_symbol_info(
                var_name
            ) or self.jack_class.get_symbol_info(var_name)
            if symbol_info:
                self.final_vm_code.extend(
                    self.vm_writer.write_push(symbol_info["kind"], symbol_info["id"])
                )
                self.final_vm_code.append("add")
                self.final_vm_code.extend(self.vm_writer.write_pop("pointer", 1))
                self.final_vm_code.extend(self.vm_writer.write_push("that", 0))

        # check if the term is a unary operator
        elif self.index < len(self.token_list) and self.token_only() in ("-", "~"):
            token_type = self.get_token_type()
            unary_operator = self.token_only()

            # add unary operator
            self.add_to_list(indent)
            # add term
            self.compile_term(indent + 2)

            # Generate VM code for unary operator
            if unary_operator == "-":
                self.final_vm_code.append("neg")
            elif unary_operator == "~":
                self.final_vm_code.append("not")

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
            token_type = self.get_token_type()
            token = self.token_only()
            if token_type == "integerConstant":
                self.final_vm_code.extend(self.vm_writer.write_constant(token))
                self.add_to_list(indent)
            elif token_type == "stringConstant":
                self.final_vm_code.extend(self.vm_writer.write_string(token))
                self.add_to_list(indent)
            elif token_type == "keyword":
                if self.token_only() == "true":
                    self.final_vm_code.extend(self.vm_writer.write_constant(0))
                    self.final_vm_code.append("not")
                    self.add_to_list(indent)
                elif self.token_only() in ("false", "null"):
                    self.final_vm_code.extend(self.vm_writer.write_constant(0))
                    self.add_to_list(indent)
                elif self.token_only() == "this":
                    self.final_vm_code.extend(self.vm_writer.write_push("pointer", 0))
                    self.add_to_list(indent)
            elif token_type == "identifier":
                symbol_info = self.jack_subroutine.get_symbol_info(
                    self.token_only()
                ) or self.jack_class.get_symbol_info(self.token_only())
                if symbol_info:
                    self.final_vm_code.extend(
                        self.vm_writer.write_push(
                            symbol_info["kind"], symbol_info["id"]
                        )
                    )
                self.add_to_list(indent)
        # add term tag
        self.parsed_list.append(" " * indent + "</term>")

    def get_token_type(self):
        """
        Determines the type of the current token.
        Returns:
            A string representing the token type ('keyword', 'symbol', 'integerConstant',
            'stringConstant', 'identifier').

        """

        # Get the whole line at the current index
        line = self.token_list[self.index]

        # Check for string constant first
        if "<stringConstant>" in line:
            return "stringConstant"

        current_token = self.token_only()  # Method to get the current token

        # Check if the token is a keyword
        if current_token in [
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
        ]:
            return "keyword"

        # Check if the token is a symbol
        elif current_token in [
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
        ]:
            return "symbol"
        # Check if the token is an integer constant
        elif current_token.isdigit():
            return "integerConstant"
        # If none of the above, the token is likely an identifier
        else:
            return "identifier"
