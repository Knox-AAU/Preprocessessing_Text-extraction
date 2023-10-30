"""Module checking if input file is correct extension compared to files actual extension"""
import os
import magic

class ExtChecker():
    """Checking if file got correct extension type and changes it if necessary"""
    def __init__(self, inputfile:str = None) -> None:
        self.inputfile = inputfile
        self.magic = magic.Magic(mime=True)

    def check_file(self) -> str:
        """Checking file extension and calling convert if not actual extension"""
        if self.inputfile is None:
            raise ValueError("No file has been selected")
        
        if os.path.exists(self.inputfile) == False:
            raise FileNotFoundError("File doesn't exist in folder")

        actual_ext_type = self.magic.from_file(self.inputfile).split("/")[-1]
        if actual_ext_type == os.path.splitext(self.inputfile):
            return self.inputfile

        return self.convert_file(self.inputfile, actual_ext_type)

    def convert_file(self, file: str, actual_ext: str) -> str:
        """Converting file extension to actual extension"""
        old_file_ext = os.path.basename(file).split("/")[-1]
        new_file_ext = old_file_ext.replace(old_file_ext.split(".")[-1], actual_ext)
        return new_file_ext
