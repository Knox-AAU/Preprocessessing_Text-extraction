""" Settings file for shared information across files """
WATCHED_FOLDER_BASE = "/watched/"

SETTINGS = {
    # File loader settings
    "file_loader": {
        "watched_folder": WATCHED_FOLDER_BASE + 'file_loader',
    },

    # Text extractor settings
    "text_extraction": {
        "watched_folder": WATCHED_FOLDER_BASE + 'text_extraction',
        "dpi": 500,
    },

    # Spell checker settings
    "spell_checking" : {
        "watched_folder": WATCHED_FOLDER_BASE + 'spell_checking',
        "output_folder": WATCHED_FOLDER_BASE + 'output',
    }
}
