""" Entrance file for the spell checking step of step 1 of the Knox pipeline """
from folder_watcher.folder_watcher import FolderWatcher
from spell_checking.spell_checker import SpellChecker

if __name__ == '__main__':
    spellchecker = SpellChecker("src/spell_checking/wordList.txt")

    spellchecker.out_dir = "/watched/output/"

    folderwatcher = FolderWatcher("/watched/spell_checking", spellchecker.handle_files)

    folderwatcher.watch()
