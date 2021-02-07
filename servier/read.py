# -*- coding: UTF-8 -*-

"""
Main file for reading raw data
"""

# import from standart library
import pandas as pd
from os.path import join
import json

# project import
from servier.data import DATA_SOURCE


def read_drugs():
    filename = join(DATA_SOURCE, "drugs.csv")
    df = pd.read_csv(filename)
    return df


def read_pubmed_csv():
    filename = join(DATA_SOURCE, "pubmed.csv")
    df = pd.read_csv(filename)
    return df


def read_pubmed_json():
    filename = join(DATA_SOURCE, "pubmed.json")
    with open(filename, "r") as f:
        pubmed = json.load(f)
    return pubmed

def read_clinical_trials():
    filename = join(DATA_SOURCE, "clinical_trials.csv")
    df = pd.read_csv(filename)
    return df
