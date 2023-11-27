"""Entrance file for the file loader step of step 1 of the Knox pipeline"""
from folder_watcher.folder_watcher import FolderWatcher
from file_loading.file_loader import FileLoader

if __name__ == '__main__':
    file_loader = FileLoader()

    folder_watcher = FolderWatcher("/watched/file_loader", file_loader.handle_files)

    folder_watcher.watch()
