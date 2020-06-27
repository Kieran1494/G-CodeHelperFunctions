from os import chdir
from Line import Line
from Motion import MotionLine
from pathlib import Path

chdir(r"C:\Users\Kieran\Desktop")


def contruct_glob(extension: str) -> str:
    """
    constructs a glob search pattern from a given extension
    :param extension: extension to make search pattern for
    :return: glob search string
    """
    if extension is not "":
        string = "*."
        for character in extension:
            string = string + f"[{character.upper()}{character.lower()}]"
        return string
    else:
        return "*"


def get_file_list(path: Path, extension, recursive=False) -> list:
    """
    give a list of files with a given extension
    :param path: path to folder
    :param extension: list or string of extensions to be search for e.g. "txt"
    :param recursive: whether to search subfolders
    :return: list of paths to all files with extensions
    """
    if isinstance(extension, (tuple, list)):
        file_list = []
        for ext in extension:
            if recursive:
                search = "**/" + contruct_glob(ext)
            else:
                search = contruct_glob(ext)
            file_list.extend(list(path.glob(search)))
        return file_list
    elif isinstance(extension, str):
        if recursive:
            search = "**/" + contruct_glob(extension)
        else:
            search = contruct_glob(extension)
        return list(path.glob(search))
    else:
        return list()


def read(file: Path) -> list:
    """
    reads gcode file (may be written as a text file) and returns all the x y and extruder values
    :param file: file to read
    :return: dictionary of x, y, e values for each command
    """
    with open(file, 'r') as f:
        lines = f.read().splitlines()
    commands = []
    for line in lines:
        if line:
            commands.append(Line(text=line))
    return commands


def write(commands: list, file: Path):
    """
    writes a list of g-code commands to a file
    :param commands: list of command
    :param file: file to write to
    """
    with open(file, 'w') as f:
        for command in commands:
            f.write(str(command) + '\n')


if __name__ == '__main__':
    path = Path("C:/Users/Kieran/OneDrive/School/High School/AOS/Science/Junior Research Project/Text and G-Code Files")
    files = get_file_list(path=path, extension=["txt", "gcode"], recursive=False)
    read(files[6])
    write([MotionLine(x=5, y=2, z=3)], path / Path("tesajkkj.txt"))

