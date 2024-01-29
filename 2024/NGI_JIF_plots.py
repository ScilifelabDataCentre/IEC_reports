# This script, I basically need to use to take the JIF data from for NGI

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os
from colour_science_2023 import (
    SCILIFE_COLOURS,
)

# infrastructure data - JIF
from AIS_JIF_data_prep_inf import (
    pubs_jif_ais_info,
)  # need to import the data NOT summarised into groups


# Need to complete the preparation for the JIF files
# can use general JIF data already prepared and QCed for the general infrastructure matching (already imported above)
# We need to match to individual records to get the individual NGI technologies

# Limit the data from JIF matching to only years we need
# no need to limit by units as they aren't individual until matched to individual extractions

pubs_jif_ais_info = pubs_jif_ais_info[
    (pubs_jif_ais_info["Year"] > 2021) & (pubs_jif_ais_info["Year"] < 2024)
]

# get only columns needed for JIF data (for matching to individ labels)

pubs_jif_ais_info_sub = pubs_jif_ais_info[["IUID", "JIF_category"]]

# Now work with individual labels to limit them

Pubs_cat_raw = pd.read_excel(
    "Data/infra_publications_individlabels_20240117.xlsx",
    sheet_name="Publications",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

# Limit individual data to show ONLY years and units we want

Pubs_cat_raw = Pubs_cat_raw.loc[
    Pubs_cat_raw["Labels"].isin(
        [
            "NGI Long read",
            "NGI Proteomics",
            "NGI Short read",
            "NGI Single cell",
            "NGI SNP genotyping",
            "NGI Spatial omics",
            "NGI Other",
        ]
    )
]

Pubs_cat_raw = Pubs_cat_raw[
    (Pubs_cat_raw["Year"] > 2021) & (Pubs_cat_raw["Year"] < 2024)
]

# match on IUID to get JIF categories by individual unit

match_JIF_seplabs = pd.merge(
    Pubs_cat_raw,
    pubs_jif_ais_info_sub,
    how="left",
    on="IUID",
)


# Need to do a group by and check the sums work!

JIF_data = match_JIF_seplabs[["Year", "Labels", "JIF_category", "Qualifiers"]]

# need to drop out the technology development papers before groupby
JIF_data.drop(
    JIF_data[JIF_data["Qualifiers"] == "Technology development"].index, inplace=True
)

JIF_data = JIF_data.groupby(["Year", "Labels", "JIF_category"]).size().reset_index()
JIF_data.columns = ["Year", "Unit", "JIF_category", "Count"]

# # # As a check, can check that the data aligns with what is expected
JIF_data.to_excel("NGI_check_JIF_data.xlsx")

# Now need to create the individual plots for each unit


def JIF_graph_func(input):
    JIFcounts = input
    # split down dataframes to enable stacking
    UnknownJIF = JIFcounts[(JIFcounts["JIF_category"] == "JIF unknown")]
    Undersix = JIFcounts[(JIFcounts["JIF_category"] == "JIF <6")]
    sixtonine = JIFcounts[(JIFcounts["JIF_category"] == "JIF 6-9")]
    ninetotwentyfive = JIFcounts[(JIFcounts["JIF_category"] == "JIF 9-25")]
    overtwentyfive = JIFcounts[(JIFcounts["JIF_category"] == "JIF >25")]
    # Make stacked bar chart
    fig = go.Figure(
        data=[
            go.Bar(
                name="JIF unknown",
                x=UnknownJIF.Year,
                y=UnknownJIF.Count,
                marker=dict(
                    color=SCILIFE_COLOURS[17], line=dict(color="#000000", width=1)
                ),
            ),
            go.Bar(
                name="JIF < 6",
                x=Undersix.Year,
                y=Undersix.Count,
                marker=dict(
                    color=SCILIFE_COLOURS[12], line=dict(color="#000000", width=1)
                ),
            ),
            go.Bar(
                name="JIF 6 - 9",
                x=sixtonine.Year,
                y=sixtonine.Count,
                marker=dict(
                    color=SCILIFE_COLOURS[4], line=dict(color="#000000", width=1)
                ),
            ),
            go.Bar(
                name="JIF 9 - 25",
                x=ninetotwentyfive.Year,
                y=ninetotwentyfive.Count,
                marker=dict(
                    color=SCILIFE_COLOURS[0], line=dict(color="#000000", width=1)
                ),
            ),
            go.Bar(
                name="JIF > 25",
                x=overtwentyfive.Year,
                y=overtwentyfive.Count,
                marker=dict(
                    color=SCILIFE_COLOURS[8], line=dict(color="#000000", width=1)
                ),
            ),
        ]
    )

    fig.update_layout(
        barmode="stack",
        plot_bgcolor="white",
        autosize=False,
        font=dict(size=26),
        margin=dict(r=250, t=0, b=0, l=0),
        width=600,
        height=600,
        showlegend=True,
    )
    # List years to use in x-axis
    Years = JIFcounts["Year"].unique().astype(str)
    Years_int = JIFcounts["Year"].unique()
    # modify x-axis
    fig.update_xaxes(
        title=" ",
        showgrid=True,
        linecolor="black",
        ticktext=[
            "<b>" + Years[0] + "</b>",
            "<b>" + Years[1] + "</b>",
            # "<b>" + Years[2] + "</b>", # in early 2024, only have data for two years,
        ],
        tickvals=[
            Years[0],
            Years[1],
        ],  # , Years[2] # needs adding back into the list when you have at least 3 years of data
    )

    Year_one = JIFcounts[(JIFcounts["Year"] == Years_int[0])]
    Year_two = JIFcounts[(JIFcounts["Year"] == Years_int[1])]
    # Year_three = JIFcounts[(JIFcounts["Year"] == Years_int[2])]

    highest_y_value = max(
        Year_one["Count"].sum(), Year_two["Count"].sum()  # , Year_three["Count"].sum()
    )

    if highest_y_value < 10:
        yaxis_tick = 1
    if highest_y_value >= 10:
        yaxis_tick = 2
    if highest_y_value > 20:
        yaxis_tick = 5
    if highest_y_value > 50:
        yaxis_tick = 10
    if highest_y_value > 100:
        yaxis_tick = 20
    if highest_y_value > 150:
        yaxis_tick = 40
    if highest_y_value > 200:
        yaxis_tick = 50
    if highest_y_value > 1000:
        yaxis_tick = 100

    # modify y-axis
    fig.update_yaxes(
        title=" ",
        showgrid=True,
        gridcolor="black",
        linecolor="black",
        dtick=yaxis_tick,
        range=[0, int(highest_y_value * 1.15)],
    )
    if not os.path.isdir("Plots/JIF_plots/"):
        os.mkdir("Plots/JIF_plots/")
    fig.write_image(
        "Plots/JIF_plots/{}_JIF.svg".format(
            input["Unit"][input["Unit"].first_valid_index()]
        )
    )


# function to iterate through all units for JIF

for i in JIF_data["Unit"].unique():
    JIF_graph_func(JIF_data[(JIF_data["Unit"] == i)])
