# -*- coding: UTF-8 -*-

"""
Main file for reading raw data
"""

# import from standard library
import pandas as pd
from os.path import join
import yaml

# project import
from servier.data import DATA_SOURCE


def read_csv(filename: str) -> pd.DataFrame:
    """
    Read csv file located in the data folder
    """
    filename = join(DATA_SOURCE, filename)
    df = pd.read_csv(filename)
    return df


def read_yaml(filename: str) -> pd.DataFrame:
    """
    Read json file located in the data folder
    We used yaml library to read it because the file contains
    an extra comma which is not standard to json.
    Reading it as a yaml is a neat trick around that.
    """
    filename = join(DATA_SOURCE, filename)
    # https://stackoverflow.com/questions/52636846/python-cant-parse-json-with-extra-trailing-comma
    with open(filename) as f:
        pubmed = yaml.load(f)
    return pubmed
