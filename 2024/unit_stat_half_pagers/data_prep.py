import pandas as pd
from pathlib import Path
import numpy as np
import json
import unicodedata


def fix_spl_char(value):
    return (
        unicodedata.normalize("NFKD", value)
        .encode("ascii", "ignore")
        .decode("utf-8")
        .strip()
    )


Path("Parsed_data").mkdir(parents=True, exist_ok=True)

### FAC MAP
# to their labels in the publication database
fac_map_input = pd.read_excel(
    "Data/Reporting Units 2023.xlsx",
    sheet_name="Blad1",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

# fac_map_input["PDB label"] = fac_map_input["PDB label"].str.replace(
#     r"\(.*\)", "", regex=True
# )

# You need the above to make sure you don't get spaces in file names
fac_map_input = fac_map_input[["Unit", "PDB label"]]
fac_map_input = fac_map_input.replace("", np.nan)
fac_map_input["PDB label"] = fac_map_input["PDB label"].fillna(fac_map_input["Unit"])
fac_map_input.rename(columns={"PDB label": "Label"}, inplace=True)
fac_map = {}
for labels, unit in zip(fac_map_input.Label, fac_map_input.Unit):
    unit = unit.strip()
    labels = labels.split("+")
    for l in labels:
        l = l.strip()
        fac_map[l] = unit

with open("Parsed_data/unit_list.json", "w") as ojson:
    json.dump(list(fac_map_input.Unit), ojson, indent=4)

### AFFILIATES
# Years of interest in 2024 - 2021-23
# We have 3 data files from OO for this (one for each year)

aff_y1_raw = pd.read_excel(
    "Data/Users 2021.xlsx",
    sheet_name="Unit Users 2021",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

aff_y2_raw = pd.read_excel(
    "Data/Users 2022.xlsx",
    sheet_name="Users Duplc. for Units removed",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

aff_y3_raw = pd.read_excel(
    "Data/Users 2023.xlsx",
    sheet_name="Users Duplc. for Units Removed",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)
# We need to combine 'Advanced Fish Technologies' to 'Spatial Proteomics'
aff_y1_raw["Unit"] = aff_y1_raw["Unit"].replace(fac_map)
aff_y2_raw["Unit"] = aff_y2_raw["Unit"].replace(fac_map)
aff_y3_raw["Unit"] = aff_y3_raw["Unit"].replace(fac_map)

# Want to get counts of how many of each individual affiliation, for each unit

affiliates_data_y1 = aff_y1_raw.groupby(["Unit", "PI affiliation"]).size().reset_index()
affiliates_data_y2 = aff_y2_raw.groupby(["Unit", "PI affiliation"]).size().reset_index()
affiliates_data_y3 = aff_y3_raw.groupby(["Unit", "PI affiliation"]).size().reset_index()

affiliates_data_y1.columns = ["Unit", "PI_aff", "Count"]
affiliates_data_y2.columns = ["Unit", "PI_aff", "Count"]
affiliates_data_y3.columns = ["Unit", "PI_aff", "Count"]

affiliates_data_y1.insert(loc=2, column="Year", value="2021")
affiliates_data_y2.insert(loc=2, column="Year", value="2022")
affiliates_data_y3.insert(loc=2, column="Year", value="2023")

aff_comb = pd.concat([affiliates_data_y1, affiliates_data_y2, affiliates_data_y3])

# Now need to replace all of the affiliation names with a shortened version
aff_map_abbr = {
    "Chalmers University of Technology": "Chalmers",
    "KTH Royal Institute of Technology": "KTH",
    "Swedish University of Agricultural Sciences": "SLU",
    "Karolinska Institutet": "KI",
    "Linköping University": "LiU",
    "Lund University": "LU",
    "Naturhistoriska Riksmuséet": "NRM",
    "Stockholm University": "SU",
    "Umeå University": "UmU",
    "University of Gothenburg": "GU",
    "Uppsala University": "UU",
    "Örebro University": "ÖU",
    "International University": "Int Univ",
    "Other Swedish University": "Other Swe Univ",
    "Other Swedish organization": "Other Swe Org",
    "Other international organization": "Other Int Org",
    "Industry ": "Industry",
    "Industry": "Industry",
    "Healthcare": "Healthcare",
}

affiliate_data = aff_comb.replace(aff_map_abbr, regex=True)
affiliate_data.to_csv("Parsed_data/affiliate_data.tsv", index=False, sep="\t")


### UNIT DATA ## changes to unit from facility, will change throughout the script.
# Single data contains all basic data for unit
# Read in to pdf almost directly
# rename columns for clarity
Unit_data = pd.read_excel(
    "Data/Single data 2023.xlsx",
    sheet_name="Single Data",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

# below, rename columns for interest to short names for easy use
Unit_data.rename(
    columns={
        "Head of Unit": "HOU",
        "Co-Head of Unit": "Co_HOU",
        "Platform Scientific Director": "PSD",
        "SciLifeLab unit since": "SLL_since",
        "Host university": "H_uni",
        "FTEs": "SLL_FTEs",
        "Funding 2023 SciLifeLab (kSEK)": "Fund_SLL",
        "Funding 2023 Other (kSEK)": "Fund_other",
        "User Fees 2023 Total (kSEK)": "Fee_total",
    },
    inplace=True,
)

Unit_data.to_csv("Parsed_data/unit_data.tsv", index=False, sep="\t")

###PUBLICATIONS!

# Used in the two graphs for one-pagers
# Need to use this data in 2 ways:
# (1) Make a barplot of publications by category
# (2) Make the barplot with JIF scores
# whilst the rest of the data comes from OO,
# This data is taken from:
# (1) publications database
# (2) publications db and JIF scores

# Focus on data for (1) - extract individual labels for records from pub db

Pubs_cat_raw = pd.read_excel(
    "Data/infra_publications_individlabels_20240117.xlsx",
    sheet_name="Publications",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

Pubs_cat_raw = Pubs_cat_raw[
    (Pubs_cat_raw["Year"] > 2020) & (Pubs_cat_raw["Year"] < 2024)
]

# # Need to get data for (fac) and groupby

pub_sub = Pubs_cat_raw[["Year", "Labels", "Qualifiers"]]
pub_sub = pub_sub.replace(r"^\s*$", "No category", regex=True)
pub_sub["Labels"] = pub_sub["Labels"].replace(fac_map)
pub_sub["Labels"] = pub_sub["Labels"].str.replace(r" \(.*\)", "", regex=True)
pub_sub["Qualifiers"] = pub_sub["Qualifiers"].astype("category")

# # Clinical Biomarkers and PLA and Single Cell Proteomics merged to Affinity Proteomics Uppsala.
# # Manually deleted 'duplicates' for labels in file - so only one of the above labels for any paper
# pub_sub = pub_sub.replace(
#     "Clinical Biomarkers", "Affinity Proteomics Uppsala", regex=True
# )

# pub_sub = pub_sub.replace(
#     "PLA and Single Cell Proteomics", "Affinity Proteomics Uppsala", regex=True
# )

pub_cat_data = pub_sub.groupby(["Year", "Labels", "Qualifiers"]).size().reset_index()

# # # in 2021 (onwards), don't need the previous duplication for the two mass cytometry centres

# Need to name the column produced by groupby
pub_cat_data.columns = ["Year", "Unit", "Qualifiers", "Count"]
pub_cat_data.to_csv("Parsed_data/pub_cat_data.tsv", index=False, sep="\t")

# Now for data for (2)
# This time work with pub data with labels combined
# i.e. one record per publication

Pubs_JIF_raw = pd.read_excel(
    "Data/infra_publications_20240117.xlsx",
    sheet_name="Publications",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

Pubs_JIF_raw = Pubs_JIF_raw[
    (Pubs_JIF_raw["Year"] > 2020) & (Pubs_JIF_raw["Year"] < 2024)
]

JIF_scores_raw = pd.read_excel(
    "Data/JCR_JournalResults_2023_MB_neat.xlsx",
    sheet_name="AIS_2",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

# Need to join the two above files and align JIF with ISSN/ISSN-L
# simpler to work with only columns of interest

Pubs_JIF_sub = Pubs_JIF_raw[
    [
        "Title",
        "Year",
        "Labels",
        "Journal",
        "ISSN",
        "ISSN-L",
    ]
]

JIF_scores_sub = JIF_scores_raw[
    [
        "ISSN",
        "eISSN",
        "Journal name",
        "JCR Abbreviation",
        "JIF Without Self Cites",
    ]
]

# Must maximise matching of JIF. I recommend checking over
# May be necessary to do some manual work

Pubs_JIF_sublow = Pubs_JIF_sub.apply(lambda x: x.astype(str).str.lower())
JIF_scores_sublow = JIF_scores_sub.apply(lambda x: x.astype(str).str.lower())
Pubs_JIF_sublow["Journal"] = Pubs_JIF_sublow["Journal"].str.replace(".", "", regex=True)
JIF_scores_sublow["JCR Abbreviation"] = JIF_scores_sublow[
    "JCR Abbreviation"
].str.replace("-basel", "", regex=True)

JIF_merge = pd.merge(
    Pubs_JIF_sublow,
    JIF_scores_sublow,
    how="left",
    on="ISSN",
)

JIF_mergebackori = pd.merge(
    Pubs_JIF_sublow,
    JIF_merge,
    on=[
        "Title",
        "Year",
        "Labels",
        "Journal",
        "ISSN",
        "ISSN-L",
    ],
)

JIF_mergebackori.drop_duplicates(subset="Title", keep="first", inplace=True)

JIF_merge_ISSNL = pd.merge(
    JIF_mergebackori,
    JIF_scores_sublow,
    how="left",
    left_on="ISSN-L",
    right_on="ISSN",  # changed to eISSN from ISSN (new file from clarivate)
)

JIF_merge_ISSNL.drop_duplicates(subset="Title", keep="first", inplace=True)

JIF_merge_ISSNL["JIF Without Self Cites_x"] = JIF_merge_ISSNL[
    "JIF Without Self Cites_x"
].fillna(JIF_merge_ISSNL["JIF Without Self Cites_y"])

JIF_merge_ISSNL = JIF_merge_ISSNL.drop(
    [
        "eISSN_x",
        "eISSN_y",
        "Journal name_x",
        "JCR Abbreviation_x",
        "ISSN_y",
        "eISSN_y",
        "Journal name_y",
        "JCR Abbreviation_y",
        "JIF Without Self Cites_y",
    ],
    axis=1,
)

# now attempt to match on journal names

JIF_merge_abbnames = pd.merge(
    JIF_merge_ISSNL,
    JIF_scores_sublow,
    how="left",
    left_on="Journal",
    right_on="JCR Abbreviation",
)

JIF_merge_abbnames["JIF Without Self Cites_x"] = JIF_merge_abbnames[
    "JIF Without Self Cites_x"
].fillna(JIF_merge_abbnames["JIF Without Self Cites"])

JIF_merge_abbnames.drop_duplicates(subset="Title", keep="first", inplace=True)

JIF_merge_abbnames = JIF_merge_abbnames.drop(
    [
        "ISSN",
        "eISSN",
        "Journal name",
        "JCR Abbreviation",
        "JIF Without Self Cites",
    ],
    axis=1,
)

JIF_merge_weISSN = pd.merge(
    JIF_merge_abbnames,
    JIF_scores_sublow,
    how="left",
    left_on="ISSN_x",
    right_on="eISSN",
)

JIF_merge_weISSN.drop_duplicates(subset="Title", keep="first", inplace=True)

JIF_merge_weISSN["JIF Without Self Cites_x"] = JIF_merge_weISSN[
    "JIF Without Self Cites_x"
].fillna(JIF_merge_weISSN["JIF Without Self Cites"])

JIF_merge_weISSN = JIF_merge_weISSN.drop(
    [
        "ISSN",
        "eISSN",
        "Journal name",
        "JCR Abbreviation",
        "JIF Without Self Cites",
    ],
    axis=1,
)

## below prints out a file that can be checked to determine whether
## manual work may increase the number of matches

# JIF_merge_weISSN.to_excel("Check_manual_improve_infra_2.xlsx")

JIF_merge_weISSN.rename(
    columns={
        "ISSN_x": "ISSN",
        "JIF Without Self Cites_x": "JIF",
    },
    inplace=True,
)

JIF_merge_weISSN = JIF_merge_weISSN.replace("n/a", np.nan)

JIF_merge_weISSN["JIF"] = JIF_merge_weISSN["JIF"].fillna(-1)

JIF_merge_weISSN["JIF"] = pd.to_numeric(JIF_merge_weISSN["JIF"])


# Match this to the database with the labels seperated (easiest way to seperate out labels)

JIF_merge_weISSN_sub = JIF_merge_weISSN[["Title", "JIF"]]

Pubs_cat_raw["Title"] = Pubs_cat_raw["Title"].str.lower()

match_JIF_seplabs = pd.merge(
    Pubs_cat_raw,
    JIF_merge_weISSN_sub,
    how="left",
    on="Title",
)

match_JIF_seplabs["JIF"] = match_JIF_seplabs["JIF"].fillna(-1)
match_JIF_seplabs["JIF"] = pd.to_numeric(match_JIF_seplabs["JIF"])
match_JIF_seplabs["JIFcat"] = pd.cut(
    match_JIF_seplabs["JIF"],
    bins=[-1, 0, 6, 9, 25, 1000],
    include_lowest=True,
    labels=["JIF unknown", "JIF <6", "JIF 6-9", "JIF 9-25", "JIF >25"],
)

# # replace facility labels

match_JIF_seplabs["Labels"] = match_JIF_seplabs["Labels"].str.replace(
    r" \(.*\)", "", regex=True
)
match_JIF_seplabs["Labels"] = match_JIF_seplabs["Labels"].replace(fac_map)

# Need to do a group by and check the sums work! (and align with above pub numbers)

JIF_data = match_JIF_seplabs.loc[:, ("Year", "Labels", "JIFcat", "Qualifiers")]

# need to drop out the technology development papers
JIF_data.drop(
    JIF_data[JIF_data["Qualifiers"] == "Technology development"].index, inplace=True
)

JIF_data = JIF_data.groupby(["Year", "Labels", "JIFcat"]).size().reset_index()
JIF_data.columns = ["Year", "Unit", "JIFcat", "Count"]
JIF_data.to_csv("Parsed_data/pub_jif_data.tsv", index=False, sep="\t")


# # As a check, can compare publications data divided by category and JIF for each unit
# # The total numbers for each unit and for each year should align.
# JIF_data.to_excel("Check_JIFdata_Jan24.xlsx")
# pub_cat_data.to_excel("Check_pubcatdata_Jan24.xlsx")

# Tech_dev = pub_cat_data[(pub_cat_data["Qualifiers"] == "Technology development")]
# print(Tech_dev.Count)
