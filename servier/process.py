# -*- coding: UTF-8 -*-

"""
Main file for processing cleaned_data data
We use a trie node to search word in a corpus of scientific articles.
We go through all the articles once for all the drugs.
This version is lighter in storage than a reverse index solution as we only store letters.
"""

# import from standart library
from collections import Counter
import glob
import pandas as pd

# import from the library
from servier.utilities import save_csv

# Inspired by https://albertauyeung.github.io/2020/06/15/python-trie.html
class TrieNode:
    """A node in the trie structure"""

    def __init__(self, char):
        # the character stored in this node
        self.char = char

        # whether this can be the end of a word
        self.is_end = False

        self.documents = set()

        # a dictionary of child nodes
        # keys are characters, values are nodes
        self.children = {}


class Trie(object):
    """The trie object"""

    def __init__(self):
        """
        The trie has at least the root node.
        The root node does not store any character
        """
        self.root = TrieNode("")
        self.documents = set()

    def insert(self, word, document):
        """Insert a word into the trie"""
        self.documents.add(document)
        node = self.root

        # Loop through each character in the word
        # Check if there is no child containing the character, create a new child for the current node
        for char in word:
            if char in node.children:
                node = node.children[char]
            else:
                # If a character is not found,
                # create a new node in the trie
                new_node = TrieNode(char)
                node.children[char] = new_node
                node = new_node

        # Mark the end of a word
        node.is_end = True
        node.documents.add(document)


    def query(self, x):
        """Given an input (a word), retrieve all documents stored in
        the trie containing that word
        """
        # Use a variable within the class to keep all possible outputs
        # As there can be more than one word with such prefix
        node = self.root

        # Check if the prefix is in the trie
        for char in x:
            if char in node.children:
                node = node.children[char]
            else:
                # cannot found the prefix, return empty list
                return []
        if node.is_end:
            return list(node.documents)
        else:
            return []


def inject_articles(articles: Union(numpy.recarray, List, tuple))):
    trie = Trie()
    for journal, title in articles:
        for word in title.split():
            trie.insert(word, journal)
    return trie
