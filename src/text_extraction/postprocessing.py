""" This file contains the function for cleaning and processing words """
import re

def clean_sentence(sentence: str) -> str:
    """ Cleans a sentence by splitting the sentence and calling clean_word on each word"""

    words = sentence.split()
    cleaned_words = [clean_word(word) for word in words]

    # Remove any '' if empty string was returned from clean_word
    cleaned_words = [word for word in cleaned_words if word.strip() != '']

    processed_sentence = ' '.join(cleaned_words)

    return processed_sentence

def clean_word(word: str) -> str:
    """ Cleans a word making it as clean as possible for 
    positive detection in the spell_checking module """
    invalid_characters = ['.', '-', ';', ',']
    invalid_numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    # Pre cleaning for common start point
    word = word.lower() # Make entire sentence lowercase
    word = word.strip() # Strip away starting and ending whitespace

    # If word is just 1 character and the word is in the invalid characters return nothing
    if len(word) == 1 and word in invalid_characters:
        return ""

    # Detect if word contains numbers => remove
    if any(num in word for num in invalid_numbers):
        word = re.sub(r"[123456789]*", "", word)

    # Detect if word contains special characters => remove

    # Check if any char of the word is in the invalid_characters
    if any(char in word for char in invalid_characters):
        word = re.sub(r"[\.\,\-\;]*", "", word)

    return word
