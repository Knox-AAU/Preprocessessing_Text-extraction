"""Module checking if input file is correct extension compared to files actual extension"""
import shutil
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
            raise FileNotFoundError("No file has been selected")

        if os.path.exists(self.inputfile) is False:
            raise FileNotFoundError("File doesn't exist in folder")

        actual_ext_type = self._get_extension(self.inputfile)
        if actual_ext_type == os.path.splitext(self.inputfile):
            return self.inputfile

        return self.convert_file(self.inputfile, actual_ext_type)

    def convert_file(self, file: str, ext: str) -> str:
        """Converting file extension to actual extension"""
        old_file_ext = os.path.basename(file).split("/")[-1]
        new_file_ext = old_file_ext.replace(old_file_ext.split(".")[-1], ext)
        shutil.move(old_file_ext, new_file_ext)
        return new_file_ext

    def _get_extension(self, inputfile) -> str:
        return self.magic.from_file(inputfile).split("/")[-1]
