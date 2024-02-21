"""Script to count collabrations between units"""

import pandas as pd
import numpy as np

unit_map = {
    "Bioinformatics Support for Computational Resources": "",
    "Bioinformatics Long-term Support WABI": "",
    "Bioinformatics Support and Infrastructure": "",
    "Bioinformatics Support, Infrastructure and Training": "Support, Infrastructure and Training",
    "Genome Engineering Zebrafish": "",
    "NGI Long read" : "National Genomics Infrastructure",
    "NGI Other" : "National Genomics Infrastructure",
    "NGI Proteomics" : "National Genomics Infrastructure",
    "NGI SNP genotyping" : "National Genomics Infrastructure",
    "NGI Short read" : "National Genomics Infrastructure",
    "NGI Single cell" : "National Genomics Infrastructure",
    "NGI Spatial omics" : "National Genomics Infrastructure",
    "NGI Stockholm" : "National Genomics Infrastructure",
    "NGI Uppsala" : "National Genomics Infrastructure",
    "Support for Computational Resources": "",
    "Systems Biology": ""
}

pub_data = pd.read_excel(
    "Data/test_facmap.xlsx",
    sheet_name="Sheet1",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

pub_data["Labels"] = pub_data["Labels"].replace(unit_map, regex=True)
labels = pub_data["Labels"]

total_collab = 0
counted_labels = []

for label in labels:
    label = label.split('|')
    all_labels = [l.strip() for l in filter(bool, label)]
    if len(set(all_labels)) > 1:
        total_collab += 1
    # for l in all_labels:
    #     if l not in counted_labels:
    #         counted_labels.append(l)

print(total_collab)
