"""Entrance file for the file loader step of step 1 of the Knox pipeline"""
from file_loader.file_loader import FileLoader
from folder_watcher.folder_watcher import FolderWatcher

if __name__ == '__main__':
    file_loader = FileLoader()

    folder_watcher = FolderWatcher("watched/file_loader", file_loader.readextension)

    folder_watcher.watch()
