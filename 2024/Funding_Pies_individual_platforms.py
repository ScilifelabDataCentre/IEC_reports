# This script can be used as a basis for the funding pie charts to be made per platform
# Need to make one set for actual funding (perhaps this script is sufficient) - only year 2023
# Another set for estimated funding 2024-7

import pandas as pd
import os
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from colour_science_2020 import (
    PLATFORM_FUNDING_COLOURS,
)

Indiv_plat_fund_data = pd.read_excel(
    "Data/Platform_funding_2021_Lianemodforpython.xlsx",
    sheet_name="Blad1",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

Indiv_plat_fund_data["Fund_MSEK"] = Indiv_plat_fund_data["Funding"] / 1000


def platform_fund_func(input):
    colours = np.array([""] * len(input["Platform"]), dtype=object)
    for i in input["Funder"]:
        colours[np.where(input["Funder"] == i)] = PLATFORM_FUNDING_COLOURS[str(i)]
    input["Funder"] = input["Funder"].replace(
        "SciLifeLab Base",
        "SciLifeLab<br>Base",
    )
    input["Funder"] = input["Funder"].replace(
        "SciLifeLab Instrument",
        "SciLifeLab<br>Instrument",
    )
    input["Funder"] = input["Funder"].replace(
        "University",
        "University<br>",
    )
    fig = go.Figure(
        go.Pie(
            values=input["Fund_MSEK"],
            labels=input["Funder"],
            hole=0.6,
            marker=dict(colors=colours, line=dict(color="#000000", width=1)),
            direction="clockwise",
            sort=True,
        )
    )
    fig.update_traces(
        textposition="outside",
        texttemplate="%{label} (%{value:.1f})",
    )
    fig.update_layout(
        margin=dict(l=0, r=0, b=0, t=0),
        font=dict(size=38),
        annotations=[
            dict(
                showarrow=False,
                text="{}".format(round(sum(input["Fund_MSEK"]), 1)),
                font=dict(size=50),  # should work for all centre bits
                x=0.5,
                y=0.5,
            )
        ],
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        width=1000,
        height=1000,
        autosize=False,
    )
    if not os.path.isdir("Plots/Platform_fund_pies"):
        os.mkdir("Plots/Platform_fund_pies")
    fig.write_image(
        "Plots/Platform_fund_pies/{}_fundingpie.svg".format(
            input["Platform"][input["Platform"].first_valid_index()]
        )
    )
    fig.write_image(
        "Plots/Platform_fund_pies/{}_fundingpie.png".format(
            input["Platform"][input["Platform"].first_valid_index()]
        )
    )


# platform_fund_func(
#     Indiv_plat_fund_data[(Indiv_plat_fund_data["Platform"] == "Genomics")]
# )

for z in Indiv_plat_fund_data["Platform"].unique():
    platform_fund_func(Indiv_plat_fund_data[(Indiv_plat_fund_data["Platform"] == z)])


# Modify function for particular labels
def platform_fund_mod_func(input):
    colours = np.array([""] * len(input["Platform"]), dtype=object)
    for i in input["Funder"]:
        colours[np.where(input["Funder"] == i)] = PLATFORM_FUNDING_COLOURS[str(i)]
    input["Funder"] = input["Funder"].replace(
        "SciLifeLab Base",
        "SciLifeLab<br>Base",
    )
    input["Funder"] = input["Funder"].replace(
        "SciLifeLab Instrument",
        "SciLifeLab<br>Instrument",
    )
    input["Funder"] = input["Funder"].replace(
        "University",
        "University<br>",
    )
    input["Funder"] = input["Funder"].replace(
        "Healthcare",
        "Healthcare<br>",
    )
    input["Funder"] = input["Funder"].replace(
        "Vinnova",
        "Vinnova<br>",
    )
    fig = go.Figure(
        go.Pie(
            values=input["Fund_MSEK"],
            labels=input["Funder"],
            hole=0.6,
            marker=dict(colors=colours, line=dict(color="#000000", width=1)),
            direction="clockwise",
            sort=True,
        )
    )
    fig.update_traces(
        textposition="outside",
        texttemplate="%{label} (%{value:.1f})",
    )
    fig.update_layout(
        margin=dict(l=0, r=0, b=0, t=0),
        font=dict(size=38),
        annotations=[
            dict(
                showarrow=False,
                text="{}".format(round(sum(input["Fund_MSEK"]), 1)),
                font=dict(size=50),  # should work for all centre bits
                x=0.5,
                y=0.5,
            )
        ],
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        width=1000,
        height=1000,
        autosize=False,
    )
    if not os.path.isdir("Plots/Platform_fund_pies"):
        os.mkdir("Plots/Platform_fund_pies")
    fig.write_image(
        "Plots/Platform_fund_pies/{}_fundingpie.svg".format(
            input["Platform"][input["Platform"].first_valid_index()]
        )
    )
    fig.write_image(
        "Plots/Platform_fund_pies/{}_fundingpie.png".format(
            input["Platform"][input["Platform"].first_valid_index()]
        )
    )


# platform_fund_mod_func(
#     Indiv_plat_fund_data[
#         (Indiv_plat_fund_data["Platform"] == "Clinical Proteomics and Immunology")
#     ]
# )


# Modify function for particular labels for clinical genomics specifically
def platform_fund_CG_func(input):
    colours = np.array([""] * len(input["Platform"]), dtype=object)
    for i in input["Funder"]:
        colours[np.where(input["Funder"] == i)] = PLATFORM_FUNDING_COLOURS[str(i)]
    input["Funder"] = input["Funder"].replace(
        "SciLifeLab Instrument",
        "SciLifeLab Instrument<br>",
    )
    input["Funder"] = input["Funder"].replace(
        "SciLifeLab Base",
        "SciLifeLab Base<br>",
    )
    input["Funder"] = input["Funder"].replace(
        "University",
        "University<br>",
    )
    input["Funder"] = input["Funder"].replace(
        "Healthcare",
        "Healthcare<br>",
    )
    input["Funder"] = input["Funder"].replace(
        "Vinnova",
        "Vinnova<br>",
    )
    fig = go.Figure(
        go.Pie(
            values=input["Fund_MSEK"],
            labels=input["Funder"],
            hole=0.6,
            marker=dict(colors=colours, line=dict(color="#000000", width=1)),
            direction="clockwise",
            sort=True,
        )
    )
    fig.update_traces(
        textposition="outside",
        texttemplate="%{label} (%{value:.1f})",
    )
    fig.update_layout(
        margin=dict(l=0, r=0, b=0, t=0),
        font=dict(size=38),
        annotations=[
            dict(
                showarrow=False,
                text="{}".format(round(sum(input["Fund_MSEK"]), 1)),
                font=dict(size=50),  # should work for all centre bits
                x=0.5,
                y=0.5,
            )
        ],
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        width=1000,
        height=1000,
        autosize=False,
    )
    if not os.path.isdir("Plots/Platform_fund_pies/"):
        os.mkdir("Plots/Platform_fund_pies/")
    fig.write_image(
        "Plots/Platform_fund_pies/{}_fundingpie.svg".format(
            input["Platform"][input["Platform"].first_valid_index()]
        )
    )
    fig.write_image(
        "Plots/Platform_fund_pies/{}_fundingpie.png".format(
            input["Platform"][input["Platform"].first_valid_index()]
        )
    )


# platform_fund_CG_func(
#     Indiv_plat_fund_data[(Indiv_plat_fund_data["Platform"] == "Clinical Genomics")]
# )
