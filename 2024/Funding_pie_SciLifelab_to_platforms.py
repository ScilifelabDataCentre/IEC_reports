"""This script will generate a pie chart showing SciLifeLab funding to different platforms"""

import pandas as pd
import plotly.graph_objects as go
import os
from colour_science_2023 import (
    SCILIFE_COLOURS,
)

df = pd.read_excel(
    "Data/SciLifeLab Funding 2024 to Platforms.xlsx",
    sheet_name="Funding Platforms",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)


plat_map = {
    "Drug Discovery and Development": "Drug Discovery <br>and Development",
    "Cellular and Molecular Imaging": "Cellular and <br>Molecular Imaging",
    "Clinical Proteomics and Immunology": "Clinical Proteomics <br>and Immunology",
    "Chemical Biology and Genome Engineering": "Chemical Biology <br>and Genome Engineering",
}

df_basic = df.replace(plat_map, regex=True)


colours = [
    SCILIFE_COLOURS[0],
    SCILIFE_COLOURS[14],
    SCILIFE_COLOURS[17],
    SCILIFE_COLOURS[13],
    SCILIFE_COLOURS[4],
    SCILIFE_COLOURS[2],
    SCILIFE_COLOURS[5],
    SCILIFE_COLOURS[12],
    SCILIFE_COLOURS[8],
    SCILIFE_COLOURS[16],
    SCILIFE_COLOURS[18],
    SCILIFE_COLOURS[7],
]

df_basic["Funding (MSEK)"] = df_basic["Funding 2024(MSEK)"].round().astype(int)
# print(df_basic)

fig = go.Figure(
    go.Pie(
        values=df_basic["Funding (MSEK)"],
        labels=df_basic["Platform"],
        hole=0.7,
        marker=dict(colors=colours, line=dict(color="#000000", width=1)),
        direction="clockwise",
        sort=True,
    )
)

fig.update_traces(
    textposition="outside",
    texttemplate="%{label} <br>%{value}",
    textfont=dict(family="Arial", size=25),
)
fig.update_layout(
    margin=dict(l=100, r=100, b=100, t=100),
    showlegend=False,
    width=1000,
    height=1000,
    autosize=False,
)
if not os.path.isdir("Plots"):
    os.mkdir("Plots")
# fig.show()

fig.write_image("Plots/Distribution_SciLifeLab_funding_to_platforms.png", scale=3)
# fig.write_image("Plots/dist_fund_platform.svg", scale=3)
