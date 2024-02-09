"""This script will generate a pie chart of national and DDD funding"""

import pandas as pd
import plotly.graph_objects as go
import os
from colour_science_2023 import (
    SCILIFE_COLOURS,
)

df = pd.read_excel(
    "Data/SciLifeLab National Funding 2024.xlsx",
    sheet_name="Funding Univ",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

df.rename(
    columns={
        "Funding 2024 (MSEK)": "Funding (MSEK)",
    },
    inplace=True,
)

df["Category"] = df["Category"].replace(
    "Collaborations & External Relations", "Collaborations & External Relations"
)
df["Category"] = df["Category"].replace(
    "Infrastructure Platforms", "Infrastructure<br>Platforms"
)

df["Category"] = df["Category"].replace("Training and courses ", "Training & courses ")
df["Category"] = df["Category"].replace(
    "Site costs, Campus Solna & Navet", "Site costs, Campus Solna<br>& Navet"
)

colours = [
    SCILIFE_COLOURS[0],
    SCILIFE_COLOURS[14],
    SCILIFE_COLOURS[17],
    SCILIFE_COLOURS[13],
    SCILIFE_COLOURS[4],
    SCILIFE_COLOURS[2],
    SCILIFE_COLOURS[6],
    SCILIFE_COLOURS[12],
    SCILIFE_COLOURS[8],
    SCILIFE_COLOURS[16],
    SCILIFE_COLOURS[18],
    SCILIFE_COLOURS[7],
]

df["Funding (MSEK)"] = df["Funding (MSEK)"].round(1)  # .astype(int)
# print(df)

fig = go.Figure(
    go.Pie(
        values=df["Funding (MSEK)"],
        labels=df["Category"],
        hole=0.7,
        marker=dict(colors=colours, line=dict(color="#000000", width=1)),
        direction="clockwise",
        sort=True,
    )
)

fig.update_traces(
    textposition="outside",
    texttemplate="%{label} <br>%{value} ",
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

fig.write_image("Plots/Scilifelab_National_and_DDD.png", scale=3)
# fig.write_image("Plots/SLL_nat_and_DDD_fund.svg", scale=3)