"""This script produces the plots required for the one-pagers"""

# 5 plots required in total for each reporting facility included in the 2022 mid term report
# 3 pie charts showing users in each year 2021-2023
# 2 stacked bar plots (one for JIF score, one for type of publication: service, collab...)

import pandas as pd
from pathlib import Path
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from colour_science_2024 import (
    SCILIFE_COLOURS,
    FACILITY_USER_AFFILIATION_COLOUR_OFFICIAL_ABB,
)

from data_loader import pub_cat_data, pub_jif_data, affiliate_data


def get_highest_val(pdata):
    Years_int = pdata["Year"].unique()
    Year_one = pdata[(pdata["Year"] == Years_int[0])]
    Year_two = pdata[(pdata["Year"] == Years_int[1])]
    Year_three = pdata[(pdata["Year"] == Years_int[2])]

    highest_y_value = max(
        Year_one["Count"].sum(), Year_two["Count"].sum(), Year_three["Count"].sum()
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

    return (yaxis_tick, highest_y_value)


def publication_plot(unit, pformat="svg"):
    unit_cat_data = pub_cat_data[pub_cat_data["Unit"] == unit]
    tecdev = unit_cat_data[unit_cat_data["Qualifiers"] == "Technology development"]
    collab = unit_cat_data[unit_cat_data["Qualifiers"] == "Collaborative"]
    service = unit_cat_data[unit_cat_data["Qualifiers"] == "Service"]
    nocat = unit_cat_data[unit_cat_data["Qualifiers"] == "No category"]
    unit_cat_data.drop(
        unit_cat_data[unit_cat_data["Qualifiers"] == "Technology development"].index,
        inplace=True,
    )

    # add No category if exists
    data = []
    if sum(nocat.Count) != 0:
        data.append(
            go.Bar(
                name="No category ",
                x=nocat.Year,
                y=nocat.Count,
                width=0.75,
                marker=dict(
                    color=SCILIFE_COLOURS[17], line=dict(color="#000000", width=1)
                ),
            ),
        )

    # create bar plot only there in any data to show
    cat_plot_file = False
    if any(pd.concat([tecdev, collab, service, nocat]).Count):
        data = data + [
            go.Bar(
                name="Collaborative ",
                x=collab.Year,
                y=collab.Count,
                width=0.75,
                marker=dict(
                    color=SCILIFE_COLOURS[12], line=dict(color="#000000", width=1)
                ),
            ),
            go.Bar(
                name="Service ",
                x=service.Year,
                y=service.Count,
                width=0.75,
                marker=dict(
                    color=SCILIFE_COLOURS[0], line=dict(color="#000000", width=1)
                ),
            ),
        ]

        fig = go.Figure(data=data)
        fig.update_layout(
            barmode="stack",
            plot_bgcolor="white",
            font=dict(family="Arial", size=25),
            autosize=False,
            margin=go.layout.Margin(t=30, r=50, b=50, l=60),
            showlegend=True,
        )

        # modify x-axis
        Years = unit_cat_data["Year"].unique().astype(str)
        fig.update_xaxes(
            showgrid=True,
            linecolor="black",
            ticktext=[
                "<b>" + Years[0] + "</b>",
                "<b>" + Years[1] + "</b>",
                "<b>" + Years[2] + "</b>",
            ],
            tickvals=[Years[0], Years[1], Years[2]],
        )
        # modify y-axis
        yaxis_tick, highest_y_value = get_highest_val(unit_cat_data)
        fig.update_yaxes(
            dtick=yaxis_tick,
            range=[0, int(highest_y_value * 1.15)],
            showgrid=True,
            gridcolor="#3f3f3f",
            linecolor="black",
        )

        # create output dir if doesn't exist
        Path("Plots/pub_plots/").mkdir(parents=True, exist_ok=True)

        # write plot to a file
        cat_plot_file = "Plots/pub_plots/{}_cat.{}".format(
            unit.replace(" ", "_"), pformat
        )
        fig.write_image(cat_plot_file)

    # Start create publication JIF plot
    unit_jif_data = pub_jif_data[pub_jif_data["Unit"] == unit]

    UnknownJIF = unit_jif_data[(unit_jif_data["JIFcat"] == "JIF unknown")]
    Undersix = unit_jif_data[(unit_jif_data["JIFcat"] == "JIF <6")]
    sixtonine = unit_jif_data[(unit_jif_data["JIFcat"] == "JIF 6-9")]
    ninetotwentyfive = unit_jif_data[(unit_jif_data["JIFcat"] == "JIF 9-25")]
    overtwentyfive = unit_jif_data[(unit_jif_data["JIFcat"] == "JIF >25")]

    # create bar plot if only any data to show
    jif_plot_file = False
    if any(
        pd.concat(
            [UnknownJIF, Undersix, sixtonine, ninetotwentyfive, overtwentyfive]
        ).Count
    ):
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
            font=dict(family="Arial", size=25),
            autosize=False,
            margin=go.layout.Margin(t=30, r=50, b=50, l=60),
            showlegend=True,
        )

        # modify x-axis
        Years = unit_jif_data["Year"].unique().astype(str)
        fig.update_xaxes(
            showgrid=True,
            linecolor="black",
            ticktext=[
                "<b>" + Years[0] + "</b>",
                "<b>" + Years[1] + "</b>",
                "<b>" + Years[2] + "</b>",
            ],
            tickvals=[Years[0], Years[1], Years[2]],
        )
        # modify y-axis
        yaxis_tick, highest_y_value = get_highest_val(unit_cat_data)
        # modify y-axis
        fig.update_yaxes(
            dtick=yaxis_tick,
            range=[0, int(highest_y_value * 1.15)],
            showgrid=True,
            gridcolor="#3f3f3f",
            linecolor="black",
        )

        # write plot to a file
        jif_plot_file = "Plots/pub_plots/{}_jif.{}".format(
            unit.replace(" ", "_"), pformat
        )
        fig.write_image(jif_plot_file)

    return (cat_plot_file, jif_plot_file, sum(tecdev.Count))


def users_plot(unit, year, pformat="png", name_fsize=25, annotation_fsize=34):
    unit_usr_data = affiliate_data[
        (affiliate_data["Unit"] == unit) & (affiliate_data["Year"] == year)
    ]
    if sum(unit_usr_data.Count) < 2:
        pi_plural = "PI"
    else:
        pi_plural = "PIs"
    u_counts = unit_usr_data["Count"].to_list()
    a_labels = unit_usr_data["PI_aff"].to_list()

    # Create plot only if there is any data
    usr_plot_file = False
    if any(u_counts):
        colours = np.array([""] * len(unit_usr_data["PI_aff"]), dtype=object)
        for i in unit_usr_data["PI_aff"]:
            colours[
                np.where(unit_usr_data["PI_aff"] == i)
            ] = FACILITY_USER_AFFILIATION_COLOUR_OFFICIAL_ABB[str(i)]

        fig = go.Figure(
            go.Pie(
                values=u_counts,
                labels=a_labels,
                text=[
                    "{} ({}%)".format(
                        a_labels[i], round(u_counts[i] / sum(u_counts) * 100, 1)
                    )
                    for i in range(len(unit_usr_data))
                ],
                hole=0.6,
                marker=dict(colors=colours, line=dict(color="#000000", width=1)),
                direction="clockwise",
                sort=True,
                textinfo="text",
                textposition="outside",
            )
        )

        fig.update_layout(
            font=dict(family="Arial", size=name_fsize),
            autosize=False,
            margin=go.layout.Margin(t=30, r=50, b=50, l=60),
            annotations=[
                dict(
                    showarrow=False,
                    text="{} {}".format(sum(unit_usr_data.Count), pi_plural),
                    font=dict(size=annotation_fsize),
                    x=0.5,
                    y=0.5,
                )
            ],
            showlegend=False,
        )

        # create output dir if doesn't exist
        Path("Plots/usr_plots/").mkdir(parents=True, exist_ok=True)

        # write plot to a file
        usr_plot_file = "Plots/usr_plots/{}_{}.{}".format(
            unit.replace(" ", "_"), year, pformat
        )
        fig.write_image(usr_plot_file)

    return usr_plot_file


# Need to make some plots with different label orientation (stacked)


def users_stacked_plot(unit, year, pformat="svg", name_fsize=25, annotation_fsize=34):
    unit_usr_data = affiliate_data[
        (affiliate_data["Unit"] == unit) & (affiliate_data["Year"] == year)
    ]
    if sum(unit_usr_data.Count) < 2:
        pi_plural = "PI"
    else:
        pi_plural = "PIs"
    u_counts = unit_usr_data["Count"].to_list()
    a_labels = unit_usr_data["PI_aff"].to_list()

    # Create plot only if there is any data
    usr_plot_file = False
    if any(u_counts):
        colours = np.array([""] * len(unit_usr_data["PI_aff"]), dtype=object)
        for i in unit_usr_data["PI_aff"]:
            colours[
                np.where(unit_usr_data["PI_aff"] == i)
            ] = FACILITY_USER_AFFILIATION_COLOUR_OFFICIAL_ABB[str(i)]

        fig = go.Figure(
            go.Pie(
                values=u_counts,
                labels=a_labels,
                text=[
                    "{}<br>({}%)".format(
                        a_labels[i], round(u_counts[i] / sum(u_counts) * 100, 1)
                    )
                    for i in range(len(unit_usr_data))
                ],
                hole=0.6,
                marker=dict(colors=colours, line=dict(color="#000000", width=1)),
                direction="clockwise",
                sort=True,
                textinfo="text",
                textposition="outside",
            )
        )

        fig.update_layout(
            font=dict(family="Arial", size=name_fsize),
            autosize=False,
            margin=go.layout.Margin(t=30, r=50, b=50, l=60),
            annotations=[
                dict(
                    showarrow=False,
                    text="{} {}".format(sum(unit_usr_data.Count), pi_plural),
                    font=dict(size=annotation_fsize),
                    x=0.5,
                    y=0.5,
                )
            ],
            showlegend=False,
        )

        # create output dir if doesn't exist
        Path("Plots/usr_plots/").mkdir(parents=True, exist_ok=True)

        # write plot to a file
        usr_plot_file = "Plots/usr_plots/{}_{}.{}".format(
            unit.replace(" ", "_"), year, pformat
        )
        fig.write_image(usr_plot_file)

    return usr_plot_file


# for i in affiliate_data["Unit"].unique():
#     temp = affiliate_data[(affiliate_data["Unit"] == i)]
#     for z in temp["Year"].unique():
#         users_plot(i, z)

# for i in pub_cat_data["Unit"].unique():
#     publication_plot(i)

# User plots for units that look better stacked.

publication_plot("Glycoproteomics and MS Proteomics and MS Proteomics")

# for i in affiliate_data["Year"].unique():
#     temp = affiliate_data[(affiliate_data["Year"] == i)]
#     users_stacked_plot("Ancient DNA", i)

# users_stacked_plot("National Genomics Infrastructure", 2020)
