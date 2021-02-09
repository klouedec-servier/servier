# -*- coding: UTF-8 -*-

"""
Main file for utilities function
"""

# import from standard library
from functools import reduce
from os.path import join
from typing import Union
import pandas as pd
import string

# import from project

from servier.data import DATA_SOURCE


def save_csv(df: pd.DataFrame, output_name: str) -> None:
    filename = join(DATA_SOURCE, output_name)
    df.to_csv(output_name, index=False)


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


def replace_punctuation(s):
    s = s.translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation)))
    return s

