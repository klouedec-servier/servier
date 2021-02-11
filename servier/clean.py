# -*- coding: UTF-8 -*-

"""
Main file for cleaning data
"""

# import from standard library
import pandas as pd
from scipy import interpolate

# import project library
from servier.utilities import read_yaml, read_csv
from servier.utilities import remove_special_character, save_csv
from servier.utilities import replace_punctuation


def clean_clinical_trials() -> None:
    """ Clean the clinical_trials DataFrame """
    ct = read_csv("clinical_trials.csv")
    ct.rename(columns={"scientific_title": "title"}, inplace=True)
    ct["title"] = ct["title"].apply(remove_special_character)
    ct["title"] = ct["title"].str.lower()
    ct["title"] = ct["title"].apply(replace_punctuation)
    ct["journal"] = ct["journal"].apply(remove_special_character)
    ct["date"] = pd.to_datetime(ct["date"])
    ct = ct.groupby(["date", "title"], as_index=False).first()
    save_csv(ct, "clinical_trials_cleaned.csv")


def clean_drugs() -> None:
    """ Clean the drugs DataFrame """
    drugs = read_csv("drugs.csv")
    drugs["drug"] = drugs["drug"].str.lower()
    save_csv(drugs, "drugs_cleaned.csv")


def my_extrapolate_func(scipy_interpolate_func, new_x):
    x1, x2 = scipy_interpolate_func.x[0], scipy_interpolate_func.x[-1]
    y1, y2 = scipy_interpolate_func.y[0], scipy_interpolate_func.y[-1]
    slope = (y2 - y1) / (x2 - x1)
    return y1 + slope * (new_x - x1)


def clean_pubmed_yaml() -> pd.DataFrame:
    """ Clean the pubmed_json DataFrame """
    pubmed = read_yaml("pubmed.json")
    pubmed = pd.DataFrame(pubmed)
    pubmed["id"] = pd.to_numeric(pubmed["id"], errors="coerce").astype("Float64")
    # Linear extrapolation of id
    # https://stackoverflow.com/questions/31332981/pandas-interpolation-replacing-nans-after-the-last-data-point-but-not-before-th/38325187
    pubmed_id_no_nan = pubmed.id.dropna()
    func = interpolate.interp1d(
        pubmed_id_no_nan.index.values,
        pubmed_id_no_nan.values,
        kind="linear",
        bounds_error=False,
    )
    pubmed["id"] = pd.Series(
        my_extrapolate_func(func, pubmed.index.values), index=pubmed.index
    )
    pubmed["id"] = pubmed["id"].astype(int)
    return pubmed


def clean_pubmed() -> None:
    """
    Merge cleaned pubmed_csv and pubmed_yaml
    """
    pubmed_csv = read_csv("pubmed.csv")
    pubmed_json = clean_pubmed_yaml()
    pubmed = pd.concat([pubmed_csv, pubmed_json])
    pubmed["date"] = pd.to_datetime(pubmed["date"])
    pubmed["title"] = pubmed["title"].str.lower()
    pubmed["title"] = pubmed["title"].apply(replace_punctuation)
    save_csv(pubmed, "pubmed_cleaned.csv")
