""" Text extraction module for the Knox Pipeline """
import dataclasses
import os
import re
from PIL import Image
import pytesseract

@dataclasses.dataclass
class TextExtractor():
    """ Text extraction interface """
    def __init__(self):
        self.out_dir = ""
        self.dpi = 500

    def read(self, input_file):
        """ Inner function that reads images and outputs the OCR text"""

        out_path = f"{self.out_dir}{re.sub(r'[^.]+$', 'txt', os.path.basename(input_file))}"

        text = str(((pytesseract.image_to_string(Image.open(input_file)))))

        print("Reading file" + input_file)

        text = text.replace("-\n", "")

        # Save each sentence as a new line in the output file
        with open(out_path, 'w', encoding='utf-8') as file:
            print(text)
            file.write(text)

        if os.path.exists(input_file):
            os.remove(input_file)
