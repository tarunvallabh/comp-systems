class LookupDicts:
    """
    Contains all the lookup dictionaries for the VM commands and operations.
    """

    def __init__(self):
        """
        Initialize the symbol table and the lookup dictionaries.
        """

        self.add_list = ["@SP", "M=M-1", "A=M", "D=M", "A=A-1", "M=D+M"]
        self.sub_list = ["@SP", "M=M-1", "A=M", "D=M", "A=A-1", "M=M-D"]
        self.and_list = ["@SP", "M=M-1", "A=M", "D=M", "A=A-1", "M=D&M"]
        self.or_list = ["@SP", "M=M-1", "A=M", "D=M", "A=A-1", "M=D|M"]
        self.not_list = ["@SP", "A=M-1", "M=!M"]
        self.neg_list = ["@SP", "A=M-1", "M=-M"]
        self.cond_list = ["@SP", "M=M-1", "A=M", "D=M", "A=A-1", "D=M-D"]

    def eq_list(self, line_num):
        """
        Returns the assembly code for the equals to command.
        Parameters:
            line_num (int): the line number of the command
        """
        return self.cond_list + [
            "@EQ" + str(line_num),
            "D;JEQ",
            "@SP",
            "A=M-1",
            "M=0",
            "@END" + str(line_num),
            "0;JMP",
            "(EQ" + str(line_num) + ")",
            "@SP",
            "A=M-1",
            "M=-1",
            "(END" + str(line_num) + ")",
        ]

    def gt_list(self, line_num):
        """
        Returns the assembly code for the greater than command.
        Parameters:
            line_num (int): the line number of the command
        """
        return self.cond_list + [
            "@GT" + str(line_num),
            "D;JGT",
            "@SP",
            "A=M-1",
            "M=0",
            "@END" + str(line_num),
            "0;JMP",
            "(GT" + str(line_num) + ")",
            "@SP",
            "A=M-1",
            "M=-1",
            "(END" + str(line_num) + ")",
        ]

    def lt_list(self, line_num):
        """
        Returns the assembly code for the less than command.
        Parameters:
            line_num (int): the line number of the command
        """
        return self.cond_list + [
            "@LT" + str(line_num),
            "D;JLT",
            "@SP",
            "A=M-1",
            "M=0",
            "@END" + str(line_num),
            "0;JMP",
            "(LT" + str(line_num) + ")",
            "@SP",
            "A=M-1",
            "M=-1",
            "(END" + str(line_num) + ")",
        ]

    def push_constant(self, index):
        """
        Returns the assembly code for the push command for the constant segment.
        Parameters:
            index (int): the offset from the base address of the corresponding segment
        """
        return ["@" + str(index), "D=A", "@SP", "A=M", "M=D", "@SP", "M=M+1"]

    def push_segment_map(self, segment, index):
        """
        Returns the assembly code for the push command for the local,
        argument, this, and that segments.
        Parameters:
            segment (str): the segment to be accessed
            index (int): the offset from the base address of the corresponding segment
        """
        segment_dict = {
            "local": "@LCL",
            "argument": "@ARG",
            "this": "@THIS",
            "that": "@THAT",
        }
        return [
            segment_dict[segment],
            "D=M",
            "@" + str(index),
            "D=D+A",
            "A=D",
            "D=M",
            "@SP",
            "A=M",
            "M=D",
            "@SP",
            "M=M+1",
        ]

    def push_temp(self, index):
        """
        Returns the assembly code for the push command for the temp segment.
        Parameters:
            index (int): the offset from the base address of the corresponding segment
        """
        return [
            "@5",
            "D=A",
            "@" + str(index),
            "D=D+A",
            "A=D",
            "D=M",
            "@SP",
            "A=M",
            "M=D",
            "@SP",
            "M=M+1",
        ]

    def push_pointer(self, index):
        """
        Returns the assembly code for the push command for the pointer segment.
        Parameters:
            index (int): the offset from the base address of the corresponding segment
        """
        return [
            "@3",
            "D=A",
            "@" + str(index),
            "D=D+A",
            "A=D",
            "D=M",
            "@SP",
            "A=M",
            "M=D",
            "@SP",
            "M=M+1",
        ]

    def push_static(self, index, filename):
        """
        Returns the assembly code for the push command for the static segment.
        Parameters:
            index (int): the offset from the base address of the corresponding segment
            filename (str): the name of the file
        """
        return [
            "@" + filename + "." + str(index),
            "D=M",
            "@SP",
            "A=M",
            "M=D",
            "@SP",
            "M=M+1",
        ]

    def pop_segment_map(self, segment, index):
        """
        Returns the assembly code for the pop command for the local,
        argument, this, and that segments.
        Parameters:
            segment (str): the segment to be accessed
            index (int): the offset from the base address of the corresponding segment
        """
        segment_dict = {
            "local": "@LCL",
            "argument": "@ARG",
            "this": "@THIS",
            "that": "@THAT",
        }

        return [
            segment_dict[segment],
            "D=M",
            "@" + str(index),
            "D=D+A",
            "@R13",
            "M=D",
            "@SP",
            "M=M-1",
            "A=M",
            "D=M",
            "@R13",
            "A=M",
            "M=D",
        ]

    def pop_temp(self, index):
        """
        Returns the assembly code for the pop command for the temp segment.
        Parameters:
            index (int): the offset from the base address of the corresponding segment
        """
        return [
            "@5",
            "D=A",
            "@" + str(index),
            "D=D+A",
            "@R13",
            "M=D",
            "@SP",
            "M=M-1",
            "A=M",
            "D=M",
            "@R13",
            "A=M",
            "M=D",
        ]

    def pop_static(self, index, filename):
        """
        Returns the assembly code for the pop command for the static segment.
        Parameters:
            index (int): the offset from the base address of the corresponding segment
            filename (str): the name of the file
        """
        return [
            "@SP",
            "M=M-1",
            "A=M",
            "D=M",
            "@" + filename + "." + str(index),
            "M=D",
        ]

    def pop_pointer(self, index):
        """
        Returns the assembly code for the pop command for the pointer segment.
        Parameters:
            index (int): the offset from the base address of the corresponding segment
        """
        return [
            "@3",
            "D=A",
            "@" + str(index),
            "D=D+A",
            "@R13",
            "M=D",
            "@SP",
            "M=M-1",
            "A=M",
            "D=M",
            "@R13",
            "A=M",
            "M=D",
        ]

    def write_label(self, label):
        """
        Writes the assembly code for the label command.
        Parameters:
            label (str): the label to be written
        """
        return ["(" + label + ")"]

    def write_goto(self, label):
        """
        Writes the assembly code for the goto command.
        Parameters:
            label (str): the label to be written
        """
        return ["@" + label, "0;JMP"]

    def write_ifgoto(self, label):
        """
        Writes the assembly code for the if-goto command.
        Parameters:
            label (str): the label to be written
        """
        return ["@SP", "M=M-1", "A=M", "D=M", "@" + label, "D;JNE"]

    def write_function(self, func, local_vars):
        """
        Writes the assembly code for the function command.
        """

        a = ["(" + func + ")"]
        for _ in range(int(local_vars)):
            a.extend(["@SP", "A=M", "M=0", "@SP", "M=M+1"])
        return a

    def push_segment_only(self, segment):
        """
        Writes the assembly code for the push command for the local,
        argument, this, and that segments.
        Parameters:
            segment (str): the segment to be accessed
        """
        segment_dict = {
            "local": "@LCL",
            "argument": "@ARG",
            "this": "@THIS",
            "that": "@THAT",
        }
        return [
            segment_dict[segment],
            "D=M",
            "@SP",
            "M=M+1",
            "A=M",
            "A=A-1",
            "M=D",
        ]

    def push_return_address(self, func, line_num):
        """
        Writes the assembly code for the push command for the return address.
        Parameters:
            func (str): the function name
            filename (str): the name of the file
        """
        ret = func + str(line_num)
        # push return address
        return [
            "@" + ret,
            "D=A",
            "@SP",
            "M=M+1",
            "A=M",
            "A=A-1",
            "M=D",
        ]

    def write_call(self, func, num_args, line_num):
        """
        Writes the assembly code for the call command.
        """
        out = []
        ret = func + str(line_num)
        # push return address
        out.extend(self.push_return_address(func, line_num))
        # push LCL
        out.extend(self.push_segment_only("local"))
        # push ARG
        out.extend(self.push_segment_only("argument"))
        # push THIS
        out.extend(self.push_segment_only("this"))
        # push THAT
        out.extend(self.push_segment_only("that"))
        # ARG = SP - (n + 5)
        out.extend(
            [
                "@SP",
                "D=M",
                "@" + str(int(num_args) + 5),
                "D=D-A",
                "@ARG",
                "M=D",
            ]
        )
        # LCL = SP
        out.extend(["@SP", "D=M", "@LCL", "M=D"])
        # goto f
        out.extend(self.write_goto(func))
        # (return-address)
        out.extend(["(" + ret + ")"])

        return out

    def write_return(self):
        """
        Writes the assembly code for the return command.
        """
        out = []
        # FRAME = LCL
        out.extend(
            [
                "@LCL",
                "D=M",
                "@" + "FRAME",
                "M=D",
            ]
        )
        # RET = *(FRAME-5)
        out.extend(
            [
                "@5",
                "A=D-A",
                "D=M",
                "@" + "RET",
                "M=D",
            ]
        )
        # *ARG = pop()
        out.extend(["@SP", "M=M-1", "A=M", "D=M", "@ARG", "A=M", "M=D"])
        # SP = ARG + 1
        out.extend(["@ARG", "D=M+1", "@SP", "M=D"])
        # THAT = *(FRAME-1)
        out.extend(
            [
                "@FRAME",
                "M=M-1",
                "A=M",
                "D=M",
                "@THAT",
                "M=D",
            ]
        )
        # THIS = *(FRAME-2)
        out.extend(
            [
                "@FRAME",
                "M=M-1",
                "A=M",
                "D=M",
                "@THIS",
                "M=D",
            ]
        )
        # ARG = *(FRAME-3)
        out.extend(
            [
                "@FRAME",
                "M=M-1",
                "A=M",
                "D=M",
                "@ARG",
                "M=D",
            ]
        )
        # LCL = *(FRAME-4)
        out.extend(
            [
                "@FRAME",
                "M=M-1",
                "A=M",
                "D=M",
                "@LCL",
                "M=D",
            ]
        )
        # goto RET
        out.extend(["@RET", "A=M", "0;JMP"])
        return out

    def bootstrap_code(self):
        """
        Sets the stack pointer to 256.
        """
        return [
            "// BOOTSTRAP CODE",
            "@256",
            "D=A",
            "@SP",
            "M=D",
        ]
