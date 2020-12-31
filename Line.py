class Line:

    def __init__(self, text: str = None, code: int = None, code_type: chr = None, comment: str = None,
                 command: str = None, **kwargs):
        self.code = code
        self.comment = comment
        self.command = command
        self.command_type = code_type
        self.coord = ('x', 'y', 'z', 'e')
        self.exclusion = tuple(list(self.coord) + ["m", "g"])
        self.command_coordinates = {k: v for k, v in kwargs.items() if k in self.coord}
        self.command_attributes = {k: v for k, v in kwargs.items() if k not in self.exclusion}
        if isinstance(text, str):
            self._read_text(text=text)
        if not isinstance(self.command, str):
            self._generate_command()

    def _generate_command(self):
        """
        generates the command string from the given variables
        """
        line = ""
        if isinstance(self.code, int):
            line += f"{self.command_type.upper()}{self.code} "
            for key in self.command_coordinates.keys():
                if isinstance(self.command_coordinates[key], (int, float)):
                    line += f"{key.upper()}{self.command_coordinates[key]} "
            for key in self.command_attributes.keys():
                if isinstance(self.command_coordinates[key], (int, float)):
                    line += f"{key.upper()}{self.command_coordinates[key]} "

        self.command = line

    def _grab_keys_values(self, text: str):
        """
        grabs keys and their corresponding value from the text and ensures command is valid
        :param text: command text
        """
        items = text.split()
        if "M" in text and "G" in text:
            raise TwoCodesException
        else:
            for item in items:
                key = item[0].lower()
                if "-" in key:
                    continue
                elif item[1:] == "":
                    number = ""
                elif key == "u":
                    number = item[1:]
                else:
                    number = float(item[1:])
                if key in self.coord:
                    self.command_coordinates[key] = number
                elif key not in self.exclusion:
                    self.command_attributes[key] = number
                elif "m" in key or "g" in key:
                    self.command_type = key
                    self.code = int(number)
                else:
                    pass

    def _read_text(self, text: str):
        """
        read the str of the line and convert to fields
        :param text: text to read
        """
        parts = text.split(";", 1)
        if len(parts) == 2:
            self.comment = parts[1]
        else:
            self.comment = None
        self.command = parts[0]
        self._grab_keys_values(self.command)

    def __str__(self) -> str:
        """
        used when str() is called on the object
        outputs the str necessary for printing / writing to a file
        :return: string version of object
        """
        ret = ""
        if isinstance(self.command, str):
            ret += self.command
        if isinstance(self.comment, str):
            ret += ";" + self.comment
        return ret

    def __mul__(self, other: float):
        """
        scales
        :param other:
        :return:
        """
        if isinstance(other, (float, int)):
            self.command_coordinates.update((x, y * other) for x, y in self.command_coordinates.items())
        return self

    __rmul__ = __mul__

    def __add__(self, other: float):
        if isinstance(other, (float, int)):
            self.command_coordinates.update((x, y + other) for x, y in self.command_coordinates.items())
        return self

    def __sub__(self, other: float):
        if isinstance(other, (float, int)):
            self.command_coordinates.update((x, y - other) for x, y in self.command_coordinates.items())
        return self


class TwoCodesException(Exception):
    def __init__(self):
        self.message = "Given Both M and G as codes"
