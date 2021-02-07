# -*- coding: UTF-8 -*-

"""
Main file for reading raw data
"""

# import from standard library
import pandas as pd
from os.path import join
import json

# project import
from servier.data import DATA_SOURCE


def read_csv(filename: str) -> pd.DataFrame:
    """
    Read csv file located in the data folder
    """
    filename = join(DATA_SOURCE, filename)
    df = pd.read_csv(filename)
    return df


def read_json(filename: str) -> pd.DataFrame:
    """
    Read json file located in the data folder
    """
    filename = join(DATA_SOURCE, filename)
    with open(filename, "r") as f:
        pubmed = json.load(f)
    return pubmed
