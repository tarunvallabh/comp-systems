import re
from lookupdict import LookupDicts


class VMParser:
    """
    Parses a single .vm file and returns the assembly code that implements it.
    """

    def clean_file(self, input_file):
        """
        Cleans the file by removing comments and whitespaces.
         Parameters:
             input_file (str): the name of the file
        """

        # remove comments and whitespaces
        single_line_comment = r"//.*"
        multi_line_comment = r"/\*.*?\*/"

        text = re.sub(pattern=single_line_comment, repl="", string=input_file)
        text = re.sub(pattern=multi_line_comment, repl="", string=text, flags=re.DOTALL)
        lines = text.splitlines()
        for i, line in enumerate(lines):
            lines[i] = line.strip()
        lines = [line for line in lines if line]

        return lines

    def parsed_command(self, lines, filename):
        """
        Returns the assembly code for the cleaned vm file.
        Parameters:
            lines (list): the cleaned vm file
            filename (str): the name of the file
        """
        parsed_commands = []
        lookup = LookupDicts()

        # arithmetic operations
        firstword_lists = {
            "add": lookup.add_list,
            "sub": lookup.sub_list,
            "neg": lookup.neg_list,
            "eq": lookup.eq_list,
            "gt": lookup.gt_list,
            "lt": lookup.lt_list,
            "and": lookup.and_list,
            "or": lookup.or_list,
            "not": lookup.not_list,
        }

        # push operations
        push_lists = {
            "constant": lookup.push_constant,
            "temp": lookup.push_temp,
            "pointer": lookup.push_pointer,
            "static": lookup.push_static,
            "local": lookup.push_segment_map,
            "argument": lookup.push_segment_map,
            "this": lookup.push_segment_map,
            "that": lookup.push_segment_map,
        }

        # pop operations
        pop_lists = {
            "temp": lookup.pop_temp,
            "pointer": lookup.pop_pointer,
            "static": lookup.pop_static,
            "local": lookup.pop_segment_map,
            "argument": lookup.pop_segment_map,
            "this": lookup.pop_segment_map,
            "that": lookup.pop_segment_map,
        }

        for i, line in enumerate(lines):
            parsed_commands.append("//" + line.upper())
            words = line.split()
            # if the line is an arithmetic operation
            if len(words) == 1:
                operation = words[0]
                if operation in ["eq", "gt", "lt"]:
                    parsed_commands.extend(firstword_lists[operation](i))
                elif operation in firstword_lists and operation not in [
                    "eq",
                    "gt",
                    "lt",
                ]:
                    parsed_commands.extend(firstword_lists[operation])
                elif operation == "return":
                    # The return command in VM language returns from a function.
                    parsed_commands.extend(lookup.write_return())

            elif len(words) == 3:
                # the operation of the line
                operation = words[0]
                # the segment to be accessed
                segment = words[1]
                # the offset from the base address of the corresponding segment
                index = words[2]

                if operation == "push":
                    if segment in ["local", "argument", "this", "that"]:
                        parsed_commands.extend(push_lists[segment](segment, index))
                    elif segment in ["temp", "pointer", "constant"]:
                        parsed_commands.extend(push_lists[segment](index))
                    elif segment == "static":
                        parsed_commands.extend(push_lists[segment](index, filename))

                elif operation == "pop":
                    if segment in ["local", "argument", "this", "that"]:
                        parsed_commands.extend(pop_lists[segment](segment, index))
                    elif segment in ["temp", "pointer"]:
                        parsed_commands.extend(pop_lists[segment](index))
                    elif segment == "static":
                        parsed_commands.extend(pop_lists[segment](index, filename))

                elif operation == "function":
                    # The function command in VM language declares a function.
                    function_name = words[1]
                    num_locals = words[2]
                    parsed_commands.extend(
                        lookup.write_function(function_name, num_locals)
                    )
                elif operation == "call":
                    # The call command in VM language calls a function.
                    function_name = words[1]
                    num_args = words[2]
                    parsed_commands.extend(
                        lookup.write_call(function_name, num_args, i)
                    )

            else:
                operation = words[0]
                if operation == "label":
                    # The label command in VM language marks a position in the code.
                    label_name = words[1]
                    parsed_commands.extend(lookup.write_label(label_name))

                elif operation == "goto":
                    # The goto command in VM language performs an unconditional jump.
                    label_name = words[1]
                    parsed_commands.extend(lookup.write_goto(label_name))

                elif operation == "if-goto":
                    # The if-goto command in VM language performs a conditional jump.
                    label_name = words[1]
                    parsed_commands.extend(lookup.write_ifgoto(label_name))

        return parsed_commands
