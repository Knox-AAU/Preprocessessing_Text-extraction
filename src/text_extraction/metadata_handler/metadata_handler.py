"""
Module for handling metadata in the Knox Pipeline.
"""
import os
import requests

class MetadataHandler:
    """
    Class to handle metadata for text extraction.
    """
    def __init__(self, api_url):
        """
        Initialize the MetadataHandler.
        """
        self.metadata = {}
        self.current_position = 0
        self.api_url = api_url

    def update_position(self, length):
        """
        Update the current position and return start and end indices.
        """
        start_index = self.current_position
        end_index = start_index + length
        self.current_position = end_index
        return start_index, end_index

    def write_metadata(self, metadata_dict):
        """
        Write metadata to the given file.
        """
        try:
            response = requests.post(
                f"{self.api_url}/metadata",
                json={"metadata": metadata_dict},
                timeout=30
            )
            response.raise_for_status()  # Raises an HTTPError for bad responses (4xx and 5xx)

            if response.status_code == 200 and response.json().get("success"):
                print(f"Metadata added successfully. UUID: {response.json().get('message')}")
            else:
                print("Error adding metadata:", response.json().get("message"))

        except requests.exceptions.RequestException as req_err:
            print("Request error adding metadata:", str(req_err))

        except ValueError as val_err:
            print("Value error decoding JSON response:", str(val_err))

    def write_file_metadata(self, input_file, uploader, index, title):
        """
        Write file metadata
        """
        file_name = os.path.basename(input_file)
        self.metadata = {
            "File Name": file_name,
            "Uploader": uploader,
            "Index": index,
            "Title": title
        }

    def write_sentence_metadata(self, sentence_index, sentence):
        """
        Write sentence index for each line.
        """
        start_index, end_index = self.update_position(len(sentence))
        self.metadata.update({
            "Sentence Index": sentence_index,
            "Start Index": start_index,
            "End Index": end_index
        })

    def reset_metadata(self):
        """
        Reset metadata and current position.
        """
        self.metadata = {}
        self.current_position = 0
        