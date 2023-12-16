""" Entrance file for the text extraction step of step 1 of the Knox pipeline """
from text_extraction.metadata_handler.metadata_handler import MetadataHandler
from text_extraction.text_extractor import TextExtractor
from folder_watcher.folder_watcher import FolderWatcher

if __name__ == '__main__':
    API_URL = "http://knox-proxy01.srv.aau.dk/metadata-api"
    metadata_handler = MetadataHandler(api_url=API_URL)

    text_extractor = TextExtractor(metadata_handler)

    text_extractor.out_dir = "/watched/spell_checking/"

    folder_watcher = FolderWatcher("/watched/text_extraction", text_extractor.read)

    folder_watcher.watch()
