""" Text extraction module for the Knox Pipeline """
import dataclasses
import os
import re
from PIL import Image
import pytesseract
from metadata_handler import MetadataHandler

@dataclasses.dataclass
class TextExtractor():
    """ Text extraction interface """
    def __init__(self):
        self.out_dir = ""
        self.dpi = 500
        self.metadata_handler = MetadataHandler()

    def read(self, input_file, file_name, index, uploader):
        """ Inner function that reads images and outputs the OCR text"""
        out_path = f"{self.out_dir}{re.sub(r'[^.]+$', 'txt', os.path.basename(input_file))}"

        text = str(((pytesseract.image_to_string(Image.open(input_file),lang="dan"))))

        print("Reading file" + input_file)

        text = text.replace("-\n", "")
        title_match = re.search(r'^[^\n]+', text)
        title = title_match.group(0) if title_match else "No Title Found"

        # Save each sentence as a new line in the output file
        with open(out_path, 'w', encoding='utf-8') as file:
            # Use MetadataHandler to write metadata
            self.metadata_handler.write_metadata(file, file_name, uploader, index, title)

            sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
            
            for i, sentence in enumerate(sentences):
                # Use MetadataHandler to write sentence metadata
                self.metadata_handler.write_sentence_metadata(file, sentence, i + 1)

            print(text)
            file.write(text)

        if os.path.exists(input_file):
            os.remove(input_file)
            