# -*- coding: UTF-8 -*-

"""
Main file for cleaning data
"""

# import from standard library
import pandas as pd
from scipy import interpolate
from functools import reduce

# import project library
from servier.read import read_yaml, read_csv
from servier.utilities import remove_special_character, save_csv

def clean_clinical_trials() -> None:
    """ Clean the clinical_trials DataFrame """
    ct = read_csv("clinical_trials.csv")
    ct["journal"] = ct["journal"].apply(remove_special_character)
    ct["journal"] = ct["journal"].str.lower()
    ct["scientific_title"] = ct["scientific_title"].apply(remove_special_character)
    ct["scientific_title"] = ct["scientific_title"].str.lower()
    ct['date'] = pd.to_datetime(ct['date'])
    ct = ct.groupby(["date", "scientific_title"], as_index=False).first()
    save_csv(ct, 'clinical_trials_cleaned.csv')


def clean_drugs() -> None:
    """ Clean the drugs DataFrame """
    drugs = read_csv("drugs.csv")
    drugs["drug"] = drugs["drug"].str.lower()
    save_csv(drugs, "drugs_cleaned.csv")

def clean_pubmed_csv() -> pd.DataFrame:
    """ Clean the pubmed_csv DataFrame """
    pubmed = read_csv("pubmed.csv")
    pubmed['date'] = pd.to_datetime(pubmed['date'])
    return pubmed


def my_extrapolate_func(scipy_interpolate_func, new_x):
    x1, x2 = scipy_interpolate_func.x[0], scipy_interpolate_func.x[-1]
    y1, y2 = scipy_interpolate_func.y[0], scipy_interpolate_func.y[-1]
    slope = (y2 - y1) / (x2 - x1)
    return y1 + slope * (new_x - x1)


def clean_pubmed_yaml() -> pd.DataFrame:
    """ Clean the pubmed_json DataFrame """
    pubmed = read_yaml("pubmed.json")
    pubmed = pd.DataFrame(pubmed)
    pubmed['id'] = pd.to_numeric(pubmed['id'], errors='coerce').astype('Float64')
    # Linear extrapolation of id
    # https://stackoverflow.com/questions/31332981/pandas-interpolation-replacing-nans-after-the-last-data-point-but-not-before-th/38325187
    pubmed_id_no_nan = pubmed.id.dropna()
    func = interpolate.interp1d(pubmed_id_no_nan.index.values,
                                   pubmed_id_no_nan.values,
                                   kind='linear',
                                   bounds_error=False)
    pubmed['id'] = pd.Series(my_extrapolate_func(func, pubmed.index.values), index=pubmed.index)
    return pubmed


def clean_pubmed() -> None:
    """
    Merge cleaned pubmed_csv and pubmed_yaml
    """
    pubmed_csv = clean_pubmed_csv()
    pubmed_json = clean_pubmed_yaml()
    pubmed = pd.concat([pubmed_csv, pubmed_json])
    save_csv(pubmed, "pubmed_cleaned.csv")
