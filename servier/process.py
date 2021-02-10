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
from typing import Union

# import from the library
from servier.utilities import read_csv, save_csv
from servier.utilities import save_pickle, save_json, read_pickle

# Inspired by https://albertauyeung.github.io/2020/06/15/python-trie.html
class TrieNode:
    """A node in the trie structure"""

    def __init__(self, char: str) -> None:
        # the character stored in this node
        self.char = char

        # whether this can be the end of a word
        self.is_end = False

        self.publications = set()

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

    def insert(self, word: str, id: Union[str, int], journal: str, date: str) -> None:
        """Insert a word into the trie"""
        publication = (id, journal, date)
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
        node.publications.add(publication)

    def query(self, x: str) -> list:
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
            return list(node.publications)
        else:
            return []


def inject_articles(articles: pd.DataFrame) -> Trie:
    """
    Inject documents into a trie structure.
    Return a Trie object where word are ready to be queried.
    """
    trie = Trie()
    cols = ["id", "journal", "title", "date"]
    articles = articles[cols].to_records(index=False)
    for id, journal, title, date in articles:
        for word in title.split():
            trie.insert(word, id, journal, date)
    return trie


def drug_mentions(df: pd.DataFrame, publication_type) -> None:
    """
    Compute drugs search on journals either on
    medical publication or clinical trials

    params:

    df:pd.DataFrame: Must contain 4 columns with this exact
                     name (journal, id, title, date)
    publication_type:str: either 'pubmed' or 'clinical_trial'
    schema of final json looks like:

    TODO
    {'xxx'}
    """
    if publication_type == "pubmed":
        df = read_csv("pubmed_cleaned.csv")
    elif publication_type == "clinical_trial":
        df = read_csv("clinical_trials_cleaned.csv")
    drugs = read_csv("drugs_cleaned.csv")
    trie = inject_articles(df)
    res = {}
    for row in drugs.iterrows():
        atccode = row[1]["atccode"]
        drug = row[1]["drug"]
        mentions = trie.query(drug)
        for id, journal, date in mentions:
            match = (str(id), atccode, date)
            if journal not in res:
                res[journal] = {}
                res[journal][publication_type] = [match]
            else:
                res[journal][publication_type].append(match)
    filename = "{}_mentions.pickle".format(publication_type)
    save_pickle(res, filename)


def drug_mention_pubmed():
    """
    Compute drug mention on Medical publication
    """
    pubmed = read_csv("pubmed_cleaned.csv")
    drug_mentions(pubmed, "pubmed")


def drug_mention_clinical_trial():
    """
    Compute drug mention on Medical publication
    """
    ct = read_csv("clinical_trials_cleaned.csv")
    drug_mentions(ct, "clinical_trial")


def merge_pubmed_clinical_trial():
    """
    Return the final json output
    """
    pubmed = read_pickle("pubmed_mentions.pickle")
    ct = read_pickle("clinical_trial_mentions.pickle")
    res = {}

    def fill_res(d, publication_type):
        for journal, match in d.items():
            if journal in res:
                res[journal][publication_type] = match
            else:
                res[journal] = {}
                res[journal][publication_type] = match

    fill_res(pubmed, "pubmed")
    fill_res(ct, "clinical_trial")
    save_json(res, "output.json")
