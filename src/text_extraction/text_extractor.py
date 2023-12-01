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

    def read(self, input_file, file_name, index, uploader):
        """ Inner function that reads images and outputs the OCR text"""

        out_path = f"{self.out_dir}{re.sub(r'[^.]+$', 'txt', os.path.basename(input_file))}"

        text = str(((pytesseract.image_to_string(Image.open(input_file),lang="dan"))))

        print("Reading file" + input_file)

        text = text.replace("-\n", "")

        # Extract the title from the text (assumes title is at the beginning)
        title_match = re.search(r'^[^\n]+', text)
        title = title_match.group(0) if title_match else "No Title Found"

        # Split text into sentences
        sentences = re.split(
            r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text
        )

        # Save each sentence as a new line in the output file with metadata
        with open(out_path, 'w', encoding='utf-8') as file:
            # Write File name, Uploader, and Index information once
            file.write(
                f"File Name: {file_name}\n"
                f"Uploader: {uploader}\n"
                f"Index: {index}\n"
                f"Title: {title}\n\n"
            )

            for i, sentence in enumerate(sentences):
                metadata = f"Sentence Index: {i + 1}\n"
                file.write(metadata + sentence + '\n')
            print(text)

        if os.path.exists(input_file):
            os.remove(input_file)
