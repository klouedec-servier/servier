# -*- coding: UTF-8 -*-

"""
Main file for utilities function
"""

# import from standard library
from functools import reduce
from os.path import join
from typing import Union
import pandas as pd
import pickle
import string
import yaml
import json

# import from project

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
        data = yaml.load(f)
    return data


def read_pickle(filename: str) -> dict:
    filename = join(DATA_SOURCE, filename)
    with open(filename, 'rb') as handle:
        d = pickle.load(handle)
    return d


def save_csv(df: pd.DataFrame, output_name: str) -> None:
    filename = join(DATA_SOURCE, output_name)
    df.to_csv(filename, index=False)


def save_pickle(d: dict, filename: str) -> None:
    filename = join(DATA_SOURCE, filename)
    with open(filename, 'wb') as handle:
        pickle.dump(d, handle, protocol=pickle.HIGHEST_PROTOCOL)


def save_json(d: dict, filename: str) -> None:
    filename = join(DATA_SOURCE, filename)
    with open(filename, 'w') as f:
        json.dump(d, f)


def remove_special_character(s: Union[str, float]) -> Union[str, float]:
    """
    Return a string removing certain escaped characters
    params
    :s: str
    return params
    :s: str
    """
    # Return nan if nan
    if s != s:
        return s
    chars_to_remove = ['\\xc3', '\\x28', '\\xb1']
    repls = tuple((char, "") for char in chars_to_remove)
    s = reduce(lambda a, kv: a.replace(*kv), repls, s)
    return s


def replace_punctuation(s: str) -> str:
    """ Replace punctuation with space """
    s = s.translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation)))
    return s
