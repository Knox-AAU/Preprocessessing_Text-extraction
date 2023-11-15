""" Spellchecker is the code doing the checking of 
words whether they follow the english language 
"""
import dataclasses

@dataclasses.dataclass
class TrieNode:
    """A node in the trie structure"""

    def __init__(self, char):
        # the character stored in this node
        self.char = char

        # whether this can be the end of a word
        self.is_end = False

        # a counter indicating how many times a word is inserted
        # (if this node's is_end is True)
        self.counter = 0

        # a dictionary of child nodes
        # keys are characters, values are nodes
        self.children = {}

@dataclasses.dataclass
class SpellChecker:
    """Spell checking interface - instanisiated with sc = Spellchecker(word_list: string)"""

    def __init__(self, word_list = None):
        """
        Got to have atleast one node in the tree - just stores one empty node
        """
        self.root = TrieNode("")
        self.word_list = word_list
        self.output = []
        self.ready = False

        if self.word_list is not None:
            with open(self.word_list, encoding='utf-8') as f:
                for line in f:
                    self.insert(line.strip().lower())

        self.ready = True
        print("Spellchecker initialized")

    def insert(self, word):
        """Insert a word into the trie"""
        node = self.root
        # Loops every character in the word and check if there is no child containing the char =>
        # creates a node at the current
        for char in word:
            if char in node.children:
                node = node.children[char]
            else:
                # If a character is not found, create a new node in the trie
                new_node = TrieNode(char)
                node.children[char] = new_node
                node = new_node

        # Mark the end of a word
        node.is_end = True
        # Increment the counter to indicate that we see this word once more
        node.counter += 1

    def dfs(self, node, prefix):
        """Depth-first traversal of the trie

        Arguments:
            - node: the node to start with
            - prefix: the current prefix, for tracing a
                word while traversing the trie
        """
        if node.is_end:
            self.output.append((prefix + node.char, node.counter))

        for child in node.children.values():
            self.dfs(child, prefix + node.char)

    def query(self, x):
        """
        Given a prefix, get all words stored in the the trie with that prefix,
        sort them by the number of times they have been inserted
        """
        # Keep all variants of the query - can be multiple different
        self.output = []
        node = self.root

        # Check if the prefix is in the trie
        for char in x:
            if char in node.children:
                node = node.children[char]
            else:
                # cannot found the prefix, return empty list
                return []

        # Traverse the trie to get all candidates
        self.dfs(node, x[:-1])

        # Sort the results in reverse order and return
        return sorted(self.output, key=lambda x: x[1], reverse=True)

    def handle_files_print(self, read_file):
        """ Test """

        if self.ready is True:
            validwords = 0
            invalidwords = 0

            with open(read_file, 'r', encoding="utf-8") as reading_file:
                for line in reading_file.readlines():
                    for word in line.split(" "):
                        if len(self.query(word)) > 0:
                            validwords += 1
                        else:
                            invalidwords += 1

            print(f"Valid words: {validwords}\nInvalid words: {invalidwords}")

    def handle_files(self, read_file):
        """ Test """
        if self.ready is True:
            output_folder = "/watched/output/"
            output_file_path = output_folder + "out_" + str(read_file).rsplit('/', maxsplit=1)[-1]

            print(output_file_path)

            with open(read_file, 'r', encoding="utf-8") as reading_file:
                with open(output_file_path, 'w', encoding="utf-8") as output_file:
                    for line in reading_file.readlines():
                        for word in line.split(" "):

                            word = word.strip()

                            if len(self.query(word)) > 0:
                                output_file.write(f"{word}\n")
