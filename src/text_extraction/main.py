""" Entrance file for the text extraction step of step 1 of the Knox pipeline """
from text_extraction.text_extractor import TextExtractor
from folder_watcher.folder_watcher import FolderWatcher
from settings import SETTINGS

if __name__ == '__main__':
    text_extractor = TextExtractor()

    folder_watcher = FolderWatcher(SETTINGS['text_extraction']["watched_folder"], text_extractor.read)

    folder_watcher.watch()
