""" Text extraction module for the Knox Pipeline """
from threading import Thread
from tempfile import TemporaryDirectory
from pathlib import Path
from PIL import Image

import pytesseract
from pdf2image import convert_from_path

# PDF_file = Path(r"./testdata/test5.pdf")

class TextExtractor():
    """ Text extraction interface """
    def __init__(self, input_file, queue):
        self.out_dir= Path("./out").expanduser()
        self.dpi = 500
        self.input_file = input_file
        self.image_file_list = []
        self.queue = queue
        self.thread = None

    def read(self):
        """ Inner function that converts and reads PDFs """
        #Part #1 : Converting PDF to images

        with TemporaryDirectory() as tempdir:
            print("Converting path")
            # Converts the input file to a list of pages
            pdf_pages = convert_from_path(self.input_file, self.dpi)
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
                        # Here the word is split to only have a single word
                        # enter the queue at a time and not the whole text
                        self.queue.add(word)

    def start_extraction(self):
        """ Wrapper function that creates a seperate thread to extract the requested file """
        self.thread = Thread(target=self.read)
        self.thread.daemon = True
        self.thread.start()

    def end_extraction(self):
        """ Method that watches and awaits for the thread to finish """
        self.thread.join()
