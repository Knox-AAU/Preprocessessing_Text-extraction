""" Entrance file for the text extraction step of step 1 of the Knox pipeline """
from folder_watcher.folder_watcher import FolderWatcher
from text_extraction.text_extractor import TextExtractor

if __name__ == '__main__':
    text_extractor = TextExtractor()

    folder_watcher = FolderWatcher("/watched/text_extraction", text_extractor.read)

    folder_watcher.watch()
