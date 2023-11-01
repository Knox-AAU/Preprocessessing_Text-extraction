
""" Entrance file for the initial step of the Knox pipeline """
from Queue.queue import Queue
from Spellchecking.spell_checker import SpellChecker
from TextExtraction.text_extractor import TextExtractor

def main():
    """ Main function of the Knox Pipeline """
    extraction_verification_queue = Queue()

    spell_checker = SpellChecker('src/Spellchecking/wordList.txt')
    text_extractor = TextExtractor(
        "src/TextExtraction/testData/test1.pdf", 
        extraction_verification_queue
    )

    # Start the threads working
    text_extractor.start_extraction()
    spell_checker.consume_queue(extraction_verification_queue)

    # Wait for the threads to stop
    text_extractor.end_extraction()
    spell_checker.end_consumation()


if __name__ == '__main__':
    main()
    