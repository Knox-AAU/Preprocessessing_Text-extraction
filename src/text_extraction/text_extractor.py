""" Text extraction module for the Knox Pipeline """
import dataclasses
import os
import re
from PIL import Image
import pytesseract
from .postprocessing import clean_sentence

@dataclasses.dataclass
class TextExtractor():
    """ Text extraction interface """
    def __init__(self):
        self.out_dir = ""
        self.dpi = 500

    def read(self, input_file):
        """ Inner function that reads images and outputs the OCR text"""

        out_path = f"{self.out_dir}{re.sub(r'[^.]+$', 'txt', os.path.basename(input_file))}"

        text = str(((pytesseract.image_to_string(Image.open(input_file),lang="dan"))))

        print("Reading file" + input_file)

        text = text.replace("-\n", "")

        cleaned_text = clean_sentence(text)

        # Save each sentence as a new line in the output file
        with open(out_path, 'w', encoding='utf-8') as file:
            print(cleaned_text)
            file.write(cleaned_text)

        if os.path.exists(input_file):
            os.remove(input_file)
