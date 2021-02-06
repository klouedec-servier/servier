# -*- coding: UTF-8 -*-

"""
Main file for reading raw data
"""

# import from standart library
import pandas as pd
from os.path import join

# project import
from servier.data import DATA_SOURCE


def read_drugs():
    filename = join(DATA_SOURCE, "drugs.csv")
    df = pd.read_csv(filename)
    return df
