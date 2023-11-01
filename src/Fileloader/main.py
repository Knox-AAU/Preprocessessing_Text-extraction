"""Main"""
import os
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from .file_loader import FileLoader

fileLoader = FileLoader()

class FileWatcher(FileSystemEventHandler):
    """watches for new files in input folder"""

    def on_created(self, event):
        fileLoader.readextension(event.src_path)
        fileLoader.last_load_status = False
        #next line can be removed, primarily used for debugging to see what is being loaded
        print("File created with extension: ", fileLoader.extension)
        #matches the supported files formats
        match fileLoader.extension:
            case '.pdf':
                fileLoader.openpdf()
            case '.png' | '.jpg':
                fileLoader.openimage()
        #next line can be removed, primarily used for debugging to see what is being loaded
        fileLoader.printcontent()
        #can be sent here if we want to feed it slowly as we load the files
        if os.listdir(fileLoader.path + fileLoader.extension):
            fileLoader.finished_loading = True


event_handler = FileWatcher()
observer = Observer()

if __name__ == "__main__":
    #this observer runs and if any new files is moved into the folder it reacts
    observer.schedule(event_handler, path='./input', recursive=True)
    observer.start()

    while True:
        try:
            if fileLoader.finished_loading is True:
                #send the loaded files to next layer here, or if it runs all the time
                # then just send it each loop a file is loaded
                print('done')
        except KeyboardInterrupt:
            observer.stop()
