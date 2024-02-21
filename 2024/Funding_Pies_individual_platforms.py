# This script can be used as a basis for the funding pie charts to be made per platform
# Need to make one set for actual funding (perhaps this script is sufficient) - only year 2023
# Another set for estimated funding 2024-7

import pandas as pd
import os
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from colour_science_2023 import (
    PLATFORM_FUNDING_COLOURS,
)

def platform_fund_func(input, vcol, fext):
    colours = np.array([""] * len(input["Platform"]), dtype=object)
    for i in input["Name/type of financier"]:
        colours[np.where(input["Name/type of financier"] == i)] = PLATFORM_FUNDING_COLOURS[str(i)]

    fig = go.Figure(
        go.Pie(
            values=input[vcol],
            labels=input["Name/type of financier"],
            hole=0.6,
            marker=dict(colors=colours, line=dict(color="#000000", width=1)),
            direction="clockwise",
            sort=True,
        )
    )
    fig.update_traces(
        textposition="outside",
        texttemplate="%{label} <br>(%{value:.1f}) ",
        textfont=dict(family="Arial", size=32),
    )

    fig.update_layout(
        margin=dict(l=0, r=0, b=0, t=0),
        annotations=[
            dict(
                showarrow=False,
                text="{}".format(round(sum(input[vcol]), 1)),
                font=dict(family="Arial", size=52),  # should work for all centre bits
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

    # fig.write_image(
    #     "Plots/Platform_fund_pies/{}_fundingpie.svg".format(
    #         input["Platform"][input["Platform"].first_valid_index()]
    #     )
    # )
    fig.write_image(
        "Plots/Platform_fund_pies/{} {}.png".format(
            input["Platform"][input["Platform"].first_valid_index()],
            fext
        )
    )

to_iterate = [
    ("2024 with SciLifeLab funding", "2024 (MSEK)", "2024"),
    ("2025–2028 with SciLifeLab fund", "2025–2028 (MSEK)", "2025-2028")
    ]

for sname, vcol, fext in to_iterate:
    Indiv_plat_fund_data = pd.read_excel(
        "Data/Total Funding and User Fees per Platform.xlsx",
        sheet_name=sname,
        header=0,
        engine="openpyxl",
        keep_default_na=False,
    )

    for z in Indiv_plat_fund_data["Platform"].unique():
        print("Processing platform - {}".format(z))
        platform_fund_func(Indiv_plat_fund_data[(Indiv_plat_fund_data["Platform"] == z)], vcol, fext)
