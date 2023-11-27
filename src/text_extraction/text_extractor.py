""" Text extraction module for the Knox Pipeline """
import dataclasses
from tempfile import TemporaryDirectory
from PIL import Image

import pytesseract
from pdf2image import convert_from_path

@dataclasses.dataclass
class TextExtractor():
    """ Text extraction interface """
    def __init__(self):
        self.out_dir = "/watched/spell_checking/"
        self.dpi = 500
        self.image_file_list = []

    def read(self, input_file):
        """ Inner function that converts and reads PDFs """
        #Part #1 : Converting PDF to images

        out_path = f"{self.out_dir}{input_file.split('/')[-1]}"

        with open(out_path, 'w', encoding='utf-8') as outfile_handle:
            with TemporaryDirectory() as tempdir:
                print("Converting path")
                # Converts the input file to a list of pages
                pdf_pages = convert_from_path(input_file, self.dpi)
                print("Converted path to file")

                # Loop over all the pages found above -> enumerate counts the pages for us
                for page_enumeration, page in enumerate(pdf_pages, start=1):

                    # Create a file name to store the image
                    filename = f"{tempdir}/page_{page_enumeration:03}.jpg"
                    print("Reading file", filename)

                    # Declaring filename for each page of PDF as JPG
                    # PDF page 1 -> page_001.jpg
                    # PDF page 2 -> page_002.jpg

                    # Save the image of the page in system
                    page.save(filename, "JPEG")
                    self.image_file_list.append(filename)
                    print("Creating file " + filename)

                    # Part #2 - Recognizing text from the images using OCR

                    # Iterate from 1 to total number of pages
                    for image_file in self.image_file_list:

                        # Set filename to recognize text from
                        # Again, these files will be:
                        # page_1.jpg
                        # page_2.jpg

                        # Recognize the text as string in image using pytesserct
                        print("Reading file" + image_file)
                        text = str(((pytesseract.image_to_string(Image.open(image_file)))))

                        # Here a clean up of the text can be made
                        # currently only newlines is being replaced with nothing
                        text = text.replace("-\n", "")

                        # Put the read data in the queue for the further steps to handle
                        for word in text.split(' '):
                            word = word.lower()
                            word = word.strip()
                            print(word)
                            # Here the word is split to only have a single word
                            # enter the queue at a time and not the whole text
                            outfile_handle.write(word + '\n')
