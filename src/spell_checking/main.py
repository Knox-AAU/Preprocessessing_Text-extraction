""" Entrance file for the spell checking step of step 1 of the Knox pipeline """
from spell_checking.spell_checker import SpellChecker
from folder_watcher.folder_watcher import FolderWatcher
from settings import SETTINGS

if __name__ == '__main__':
    spellchecker = SpellChecker("src/spell_checking/wordList.txt")

    folderwatcher = FolderWatcher(
        SETTINGS["spell_checking"]['watched_folder'],
        spellchecker.handle_files
    )

    folderwatcher.watch()
