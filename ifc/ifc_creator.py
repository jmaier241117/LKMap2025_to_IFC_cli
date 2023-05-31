import ifcopenshell
import os.path
from ifcopenshell import file


class IfcFileBuilder:
    def __init__(self, file_name):
        self.file = ifcopenshell.file(file_name)


def write_ifc_file(fileName: string, directoryPath: path):
    ifc_file.write(path + fileName)
    exists()
