class ClassSymbolTable:
    """
    Class representing the symbol table for a class.
    """

    def __init__(self, class_name):
        """
        Initializes the ClassSymbolTable object.
        """
        self.class_name = class_name
        self.class_symbol_table = {}
        self.n_static_symbols = 0
        self.n_field_symbols = 0

    def add_field_var(self, var_name, var_type):
        """
        Adds a field variable to the symbol table.
        """
        self.class_symbol_table[var_name] = {
            "type": var_type,
            "kind": "field",
            "id": self.n_field_symbols,
        }
        self.n_field_symbols += 1

    def add_static_var(self, var_name, var_type):
        """
        Adds a static variable to the symbol table.
        """
        self.class_symbol_table[var_name] = {
            "type": var_type,
            "kind": "static",
            "id": self.n_static_symbols,
        }
        self.n_static_symbols += 1

    def get_symbol_info(self, symbol_name):
        """
        Gets the symbol info for a given symbol name.
        """
        return self.class_symbol_table.get(symbol_name, None)


class SubroutineSymbolTable:
    """
    Class representing the symbol table for a subroutine.
    """

    def __init__(self, class_name, subroutine_type, return_type, subroutine_name):
        self.class_name = class_name
        self.subroutine_type = subroutine_type
        self.return_type = return_type
        self.subroutine_name = subroutine_name
        self.subroutine_symbol_table = {}
        self.n_local_symbols = 0
        self.n_arg_symbols = 0

        if self.subroutine_type == "method":
            self.add_arg("this", self.class_name)

    def add_var(self, var_name, var_type):
        """
        Adds a variable to the symbol table.
        """
        self.subroutine_symbol_table[var_name] = {
            "type": var_type,
            "kind": "var",
            "id": self.n_local_symbols,
        }
        self.n_local_symbols += 1

    def add_arg(self, arg_name, var_type):
        """
        Adds an argument to the symbol table.
        """
        self.subroutine_symbol_table[arg_name] = {
            "type": var_type,
            "kind": "arg",
            "id": self.n_arg_symbols,
        }
        self.n_arg_symbols += 1

    def get_symbol_info(self, symbol_name):
        """
        Gets the symbol info for a given symbol name.
        """
        return self.subroutine_symbol_table.get(symbol_name, None)
