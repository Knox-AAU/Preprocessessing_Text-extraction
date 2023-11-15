""" Entrance file for the spell checking step of step 1 of the Knox pipeline """
from spell_checking.spell_checker import SpellChecker
from folder_watcher.folder_watcher import FolderWatcher

if __name__ == '__main__':
    spellchecker = SpellChecker("src/spell_checking/wordList.txt")

    folderwatcher = FolderWatcher("watched/spell_checking", spellchecker.handle_files)

    folderwatcher.watch()
