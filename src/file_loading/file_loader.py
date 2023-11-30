"""FileLoader needs to load files, check extension and format is usable for next step"""
import dataclasses
import re
import os
import pdf2image
from pdf2image.exceptions import PDFPopplerTimeoutError, PDFSyntaxError
from file_loading.extension_checker import ExtChecker

@dataclasses.dataclass
class ImageStructure:
    """Structure of the images we want to give to the next step"""
    def __init__(self) -> None:
        self.image = None
        self.file_name = None
        self.index = None

@dataclasses.dataclass
class FileLoader:
    """ handling of files """

    def __init__(self):
        self.extension = None
        self.path = None
        self.output_folder = ""
        self.last_load_status = False

    def openpdf(self):
        """loads pdf"""
        try:
            images = pdf2image.convert_from_path(self.path)
            for index, image in enumerate(images):
                ims = ImageStructure()
                ims.file_name = os.path.basename(self.path)
                ims.image = image
                ims.index = index
                self._output_file(ims)

            self.last_load_status = True
        except (NotImplementedError, PDFPopplerTimeoutError, PDFSyntaxError):
            self.last_load_status = False

    def _output_file(self,image):
        """Saves image as png format in text_extraction output folder"""
        output_file_path = self.output_folder + "out_" + str(image.index) + "_" + image.file_name
        new_file = re.sub(r'[^.]+$', "png", output_file_path)
        image.image.save(new_file)

    def _remove_file(self):
        """removes files"""
        if self.last_load_status is True:
            if os.path.exists(self.path):
                os.remove(self.path)

    def handle_files(self, read_file):
        """ handles calling file_loader functions when told by folder_watcher """

        extension_checker = ExtChecker()
        extension_checker.inputfile = read_file

        self.path = extension_checker.check_file()
        self.extension = extension_checker.get_extension(read_file)

        match self.extension:
            case 'pdf':
                self.openpdf()
        self._remove_file()
        