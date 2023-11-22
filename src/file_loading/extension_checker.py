"""Module checking if input file is correct extension compared to files actual extension"""
import shutil
import os
import re
import magic

class ExtChecker():
    """Checking if file got correct extension type and changes it if necessary"""
    def __init__(self, inputfile:str = None) -> None:
        self.inputfile = inputfile
        self.magic = magic.Magic(mime=True)

    def check_file(self) -> str:
        """Checking file extension and calling convert if not actual extension"""
        if self.inputfile is None:
            raise FileNotFoundError("No file has been selected")

        if os.path.exists(self.inputfile) is False:
            raise FileNotFoundError("File doesn't exist in folder")
        actual_ext_type = self.get_extension(self.inputfile)

        if actual_ext_type == os.path.splitext(self.inputfile)[1].replace('.',''):
            return self.inputfile

        return self.convert_file(self.inputfile, actual_ext_type)

    def convert_file(self, file: str, ext: str) -> str:
        """Converting file extension to actual extension"""
        new_file = re.sub(r'[^.]+$', ext, file)
        shutil.move(file, new_file)
        return new_file

    def get_extension(self, inputfile) -> str:
        """Gets the extension of the file"""
        return self.magic.from_file(inputfile).split("/")[-1]
