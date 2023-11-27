""" File watcher - please send help """
import os
from time import sleep
import dataclasses
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class _Watcher(FileSystemEventHandler):
    def __init__(self, function_to_run):
        self.function_to_run = function_to_run

    def on_created(self, event):
        if not event.is_directory:
            size_before = -1
            while os.path.getsize(event.src_path) != size_before:
                size_before = os.path.getsize(event.src_path)
                sleep(0.1)
            full_path = os.path.join(os.getcwd(), event.src_path)
            full_path = event.src_path
            self.function_to_run(full_path)

@dataclasses.dataclass
class FolderWatcher:
    """ 
    :description: Folder watcher class that allows to watch a folder and
    handle files being created in that folder\n
    Takes two parameters\n
    :param: path_to_watch is a path to the folder that should be watched\n
    :param: function_to_run is the function that should be applied to the file that is found.
    this function should start by reading the file
    """

    def __init__(self, path_to_watch, function_to_run):
        self.path_to_watch = path_to_watch
        self.function_to_run = function_to_run

    def watch(self):
        """This method is a wrapper function that watches the folder and 
        applys a function to files in the folder"""

        watcher = _Watcher(self.function_to_run)

        observer = Observer()
        observer.schedule(watcher, path=self.path_to_watch, recursive=True)
        observer.start()

        try:
            while True:
                sleep(1)

        except KeyboardInterrupt:
            observer.stop()

        observer.join()
