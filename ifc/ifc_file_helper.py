import ifcopenshell
import os.path
from ifcopenshell import file


def create_ifc_file() -> file:
    return ifcopenshell.file()


def write_ifc_file(fileName: string, directoryPath: path):
    ifc_file.write(path + fileName)
    exists()
