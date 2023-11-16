"""Entrance file for the file loader step of step 1 of the Knox pipeline"""
from file_loading.file_loader import FileLoader
from folder_watcher.folder_watcher import FolderWatcher
from settings import SETTINGS

if __name__ == '__main__':
    file_loader = FileLoader()

    folder_watcher = FolderWatcher(
        SETTINGS['file_loader']['watched_folder'],
        file_loader.handle_files
    )

    folder_watcher.watch()
