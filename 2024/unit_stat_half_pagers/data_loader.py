import pandas as pd
import json

with open("Parsed_data/unit_map.json") as ujson:
    units_map = json.load(ujson)

affiliate_data = pd.read_csv(
    "Parsed_data/affiliate_data.tsv",
    sep="\t",
    header=0
)

unit_data = pd.read_csv(
    "Parsed_data/unit_data.tsv",
    sep="\t",
    header=0,
    dtype=str
)

funding_data = pd.read_csv(
    "Parsed_data/funding_data.tsv",
    sep="\t",
    header=0
)

pub_cat_data = pd.read_csv(
    "Parsed_data/pub_cat_data.tsv",
    sep="\t",
    header=0
)

pub_jif_data = pd.read_csv(
    "Parsed_data/pub_jif_data.tsv",
    sep="\t",
    header=0
)
