"""FileLoader needs to load files, check extension and format is usable for next step"""
import os
import pdf2image
from PIL import Image

class ImageStructure:
    """Structure of the images we want to give to the next step"""
    def __init__(self) -> None:
        #more can be added if we want to save more information about the image loaded
        self.image = None
        self.format = None
        self.size = None
        self.mode = None
        self.file_name = None


class FileLoader:
    """ handling of files """

    def __init__(self):
        self.extension = None
        self.path = None
        self.images = []
        self.last_load_status = False
        self.finished_loading = False

    def readextension(self,string):
        """Reads the extension of the file and selects method to be used"""
        self.path, self.extension = os.path.splitext(string)

    def openpdf(self):
        """loads pdf"""
        try:
            images = pdf2image.convert_from_path(self.path + self.extension)
            self.last_load_status = True
        except Exception as e:
            print(e)
            self.last_load_status = False
        for image in images:
            ims = ImageStructure()
            ims.file_name = os.path.basename(self.path + self.extension)
            ims.image = image
            ims.format = image.format
            ims.size = image.size
            ims.mode = image.mode
            self.images.append(ims)



    def openimage(self):
        """loads images"""
        try:
            image = Image.open(self.path + self.extension)
            self.last_load_status = True
        except Exception as e:
            print(e)
            self.last_load_status = False

        ims = ImageStructure()
        ims.file_name = os.path.basename(self.path + self.extension)
        ims.image = image
        ims.format = image.format
        ims.size = image.size
        ims.mode = image.mode
        self.images.append(ims)

    def printcontent(self):
        """print"""
        for image in self.images:
            print(image.file_name, image.format, image.size, image.mode)

    def removefile(self):
        """removes file after loading"""
        if self.last_load_status is True:
            if os.path.exists(self.path + self.extension):
                os.remove(self.path + self.extension)
