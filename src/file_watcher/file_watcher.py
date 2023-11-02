""" File watcher """
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
            # Her gør noget med filer
            full_path = os.path.join(os.getcwd(), event.src_path)
            print(f"File is created: {full_path}")
            self.function_to_run(full_path)

@dataclasses.dataclass
class FileWatcher:
    """ 
    :description: File watcher class that allows to watch a file and
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
        """ This method is a wrapper function that watches the folder and 
        applys a function to files in the folder"""
        watcher = _Watcher(self.function_to_run)

        observer = Observer()
        observer.schedule(watcher, path=self.path_to_watch, recursive=False)
        observer.start()

        try:
            while True:
                sleep(1)

        except KeyboardInterrupt:
            observer.stop()

        observer.join()

if __name__ == '__main__':
    fw = FileWatcher('./input', print)

    fw.watch()
