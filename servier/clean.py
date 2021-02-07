# -*- coding: UTF-8 -*-

"""
Main file for cleaning data
"""

# import from standard library
import pandas as pd
from functools import reduce

# import project library
from servier.read import read_csv, read_json
from servier.utilities import remove_special_character

def clean_clinical_trials() -> None:
    """
    Clean the clinical_trials DataFrame
    """
    ct = read_csv("clinical_trials.csv")
    ct["journal"] = ct["journal"].apply(remove_special_character)
    ct["scientific_title"] = ct["scientific_title"].apply(remove_special_character)
    ct['date'] = pd.to_datetime(ct['date'])
    ct = ct.groupby(["date", "scientific_title"], as_index=False).first()
    save_csv(ct, 'clinical_trials_cleaned.csv')
