"""
Module for handling metadata in the Knox Pipeline.
"""

class MetadataHandler:
    """
    Class to handle metadata for text extraction.
    """
    def __init__(self):
        """
        Initialize the MetadataHandler.
        """
        self.metadata = {}
        self.current_position = 0

    def update_position(self, length):
        """
        Update the current position and return start and end indices.
        """
        start_index = self.current_position
        end_index = start_index + length
        self.current_position = end_index
        return start_index, end_index

    def write_metadata(self, file, metadata_dict):
        """
        Write metadata to the given file.
        """
        metadata_str = "\n".join([f"{key}: {value}" for key, value in metadata_dict.items()])
        file.write(metadata_str + "\n\n")

    def write_file_metadata(self, file_name, uploader, index, title):
        """
        Write file metadata
        """
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
        