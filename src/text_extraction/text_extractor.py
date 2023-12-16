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
    def __init__(self, metadata_handler=None):
        self.out_dir = ""
        self.dpi = 500
        self.metadata_handler = metadata_handler

    def find_title(self, text):
        """Extracts a title from the given text using predefined keywords."""
        cleaned_text = text.replace("-\n", "")
        title_keywords = ["title", "heading", "chapter", "section"]
        pattern = fr'\b(?:{"|".join(title_keywords)})\b.*'
        title_match = re.search(pattern, cleaned_text, re.IGNORECASE)
        title = title_match.group(0) if title_match else "No Title Found"
        return title

    def read(self, input_file, index=None, uploader=None):
        """ Inner function that reads images and outputs the OCR text"""
        file_name = os.path.basename(input_file)

        # Convert index to string
        index_str = str(index)

        # Construct the output file path using bytes
        out_path = os.path.join(
            self.out_dir,
            f"out_{index_str}_{os.path.basename(input_file)}.txt"
        )

        # Check for null bytes in file path
        if '\x00' in out_path:
            print(f"Problematic file path: {out_path}")
            raise ValueError("File path contains embedded null byte.")

        text = str(((pytesseract.image_to_string(Image.open(input_file),lang="dan"))))

        print("Reading file" + input_file)

        title = self.find_title(text)
        self.metadata_handler.write_file_metadata(file_name, uploader, index, title)
        cleaned_text = clean_sentence(text)

        # Save each sentence as a new line in the output file
        with open(out_path, 'w', encoding='utf-8') as file:
            # Use MetadataHandler to write metadata
            self.metadata_handler.write_metadata(file)

            print("Title:", title)
            print("Cleaned Text:", cleaned_text)

            print(text)
            file.write(text)
            file.write(cleaned_text)

        if os.path.exists(input_file):
            os.remove(input_file)
            