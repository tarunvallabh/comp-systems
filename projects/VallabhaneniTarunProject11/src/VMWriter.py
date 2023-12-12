class VMWriter:
    """
    Class that emits VM commands into a file, using the VM command syntax.
    """

    def __init__(self):
        """
        Initializes the VMWriter object.
        """
        self.segment_dict = {
            "static": "static",
            "field": "this",
            "arg": "argument",
            "var": "local",
        }

    def write_push(self, segment, index):
        """
        Writes a VM push command.
        Parameters:
            segment (str): the segment to push to
            index (int): the index to push to
        """
        if segment in self.segment_dict:
            segment = self.segment_dict[segment]

        return [f"push {segment} {index}"]

    def write_pop(self, segment, index):
        """
        Writes a VM pop command.
        Parameters:
            segment (str): the segment to pop from
            index (int): the index to pop from
        """
        if segment in self.segment_dict:
            segment = self.segment_dict[segment]

        return [f"pop {segment} {index}"]

    def write_if(self, label):
        """
        Writes a VM if-goto command.
        Parameters:
            label (str): the label to jump to
        """
        return [f"if-goto {label}"]

    def write_goto(self, label):
        """
        Writes a VM goto command.
        Parameters:
            label (str): the label to jump to
        """
        return [f"goto {label}"]

    def write_label(self, label):
        """
        Writes a VM label command.
        Parameters:
            label (str): the label to write
        """
        return [f"label {label}"]

    def write_function(self, subroutine):
        """
        Writes a VM function command.
        Parameters:
            subroutine (Subroutine): the subroutine to write
        """
        return [
            f"function {subroutine.class_name}.{subroutine.subroutine_name} {subroutine.n_local_symbols}"
        ]

    def write_return(self):
        """
        Writes a VM return command.
        """
        return ["return"]

    def write_call(self, class_name, func_name, num_arg_symbols):
        """
        Writes a VM call command.
        Parameters:
            class_name (str): the class name to call
            func_name (str): the function name to call
            num_arg_symbols (int): the number of argument symbols to call
        """
        return [f"call {class_name}.{func_name} {num_arg_symbols}"]

    def write_constant(self, constant):
        """
        Writes a VM push constant command.
        Parameters:
            constant (int): the constant to push
        """
        return [f"push constant {constant}"]

    def write_string(self, string):
        """
        Writes a VM push string command.
        Parameters:
            string (str): the string to push
        """
        string_out = []
        string_out.extend(self.write_constant(len(string)))
        string_out.append("call String.new 1")
        for char in string:
            string_out.extend(self.write_constant(ord(char)))
            string_out.append("call String.appendChar 2")
        return string_out

    def write_arithmetic(self, operator):
        """
        Writes a VM arithmetic command.
        Parameters:
            operator (str): the operator to use
        """

        op_dict = {
            "+": "add",
            "-": "sub",
            "*": "call Math.multiply 2",
            "/": "call Math.divide 2",
            "&amp;": "and",
            "|": "or",
            "&lt;": "lt",
            "&gt;": "gt",
            "=": "eq",
        }
        return [op_dict[operator]]
