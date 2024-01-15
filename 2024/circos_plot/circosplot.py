"""This script can be used to construct circos plots
these plots are otherwise known as chord plots 
it is possible to produce versions for web or print 
using this script."""
# modified by LH from:
# https://nbviewer.jupyter.org/github/empet/Plotly-plots/blob/master/Chord-diagram.ipynb?flush_cache=true

import numpy as np
from numpy import pi
import plotly.graph_objects as go
import os
from plotly.offline import download_plotlyjs, init_notebook_mode, iplot, plot
import pandas as pd
import networkx as nx
from itertools import combinations

# df will require manual changes - a 'test.xlsx' will be created for checking.
# see fac_map file for details
from fac_map_circos import fac_map, df

unit = df["Labels"].str.split("|")
unit = unit.tolist()
# print(unit)
# list of labels that should be considered
# extract from fac_map
values = fac_map.values()
# Note: require at least 6 categories in the matrix(not usually a problem with facilities).
# Note: Only include facilities that collaborated with at least one other facility, or you'll see error
# 'invalid value encountered in true_divide'
# To work out who collaborated, will need some manual work
# can just print everything and see who has no ribbons - will be obvious as arc spacing will be closer
# Remove the ones that didnt collaborate
# can use the below to print out a list of your labels so you can paste below
# labels = list(values)
# print (labels)
# you can rearrange labels in the list below to ensure that the labels on the plot dont overlap
# if you get an error, might be fixed by rearrangement
labels = [
    "Integrated Microscopy Technologies Umeå",  # cc
    "Integrated Microscopy Technologies Gothenburg",  # cc
    "Integrated Microscopy Technologies Stockholm",  # cc
    "National Genomics Infrastructure",  # cc
    "Autoimmunity and Serology Profiling",  # cc
    # "Support for Computational Resources", # OO asked that this always excluded #cc
    "Affinity Proteomics Stockholm",  # cc
    "Affinity Proteomics Uppsala",  # cc
    # "AIDA Data Hub",  # cc - no collab
    "Structural Proteomics",  # cc
    "Cellular Immunomonitoring",  # cc
    "BioImage Informatics",  # cc
    "Cryo-EM",  # cc
    # "Clinical Genomics Örebro",  # cc - no collab
    "CRISPR Functional Genomics",  # cc
    # "Ancient DNA",  # cc - no collab
    "Glycoproteomics",  # cc
    "Drug Discovery and Development",  # cc
    "Spatial Proteomics",  # cc
    # "Exposomics",  # cc - no collab
    "In Situ Sequencing",  # cc
    "Eukaryotic Single Cell Genomics",  # cc
    "Chalmers Mass Spectrometry Infrastructure",  # cc
    "Microbial Single Cell Genomics",  # cc
    "Bioinformatics Support, Infrastructure and Training",  # cc
    # "Chemical Proteomics",  # cc- no collab
    "Swedish NMR Centre",  # cc
    "Chemical Biology Consortium Sweden",  # cc
    # "Spatial Mass Spectrometry",  # cc - no collab
    "Global Proteomics and Proteogenomics",  # cc
    "Swedish Metabolomics Centre",  # cc
    "Clinical Genomics Gothenburg",  # cc
    "Clinical Genomics Uppsala",  # cc
    "Clinical Genomics Lund",  # cc
    "Clinical Genomics Linköping",  # cc
    "Clinical Genomics Umeå",  # cc
    "Clinical Genomics Stockholm",  # cc
]


# produce data matrix
G = nx.MultiGraph()
G = nx.from_edgelist(
    (c for n_nodes in unit for c in combinations(n_nodes, r=2)),
    create_using=nx.MultiGraph,
)
G = nx.to_pandas_adjacency(G, nodelist=labels, dtype="int")
matrix = G.to_numpy()


# functions taken from webpage noted above
def check_data(data_matrix):
    L, M = data_matrix.shape
    if L != M:
        raise ValueError("Data array must have a (n,n) shape")
    return L


L = check_data(matrix)


def moduloAB(x, a, b):  # maps a real number onto the unit circle identified with
    # the interval [a,b), b-a=2*PI
    if a >= b:
        raise ValueError("Incorrect interval ends")
    y = (x - a) % (b - a)
    return y + b if y < 0 else y + a


def test_2PI(x):
    return 0 <= x < 2 * pi


row_sum = [matrix[k, :].sum() for k in range(L)]

# set the gap between two consecutive ideograms
gap = 2 * pi * 0.005
ideogram_length = 2 * pi * np.asarray(row_sum) / sum(row_sum) - gap * np.ones(L)


def get_ideogram_ends(ideogram_len, gap):
    ideo_ends = []
    left = 0
    for k in range(len(ideogram_len)):
        right = left + ideogram_len[k]
        ideo_ends.append([left, right])
        left = right + gap
    return ideo_ends


ideo_ends = get_ideogram_ends(ideogram_length, gap)


def make_ideogram_arc(R, phi, a=50):  # was 50
    # R is the circle radius
    # phi is the list of  angle coordinates of an arc ends
    # a is a parameter that controls the number of points to be evaluated on an arc
    if not test_2PI(phi[0]) or not test_2PI(phi[1]):
        phi = [moduloAB(t, 0, 2 * pi) for t in phi]
    length = (phi[1] - phi[0]) % 2 * pi
    nr = 5 if length <= pi / 4 else int(a * length / pi)

    if phi[0] < phi[1]:
        theta = np.linspace(phi[0], phi[1], nr)
    else:
        phi = [moduloAB(t, -pi, pi) for t in phi]
        theta = np.linspace(phi[0], phi[1], nr)
    return R * np.exp(1j * theta)


make_ideogram_arc(1.3, [11 * pi / 6, pi / 17])

labels = labels

# set colours to SciLifeLab visual identity
# to set colours randomly
# ideo_colors = [
#     "rgba(4, 92, 100, 0.75)",
#     "rgba(167, 201, 71, 0.75)",
#     "rgba(76, 151, 159, 0.75)",
#     "rgba(166, 166, 166, 0.75)",
#     "rgba(73, 31, 83, 0.75)",
#     "rgba(63, 63, 63, 0.75)",
# ] * 6

ideo_colors = [
    "rgba(166, 166, 166, 0.75)",  # Cellular and molecular imaging platform
    "rgba(166, 166, 166, 0.75)",  # Cellular and molecular imaging platform
    "rgba(166, 166, 166, 0.75)",  # Cellular and molecular imaging platform
    "rgba(167, 201, 71, 0.75)",  # genomics platform
    "rgba(63, 63, 63, 0.75)",  # clinical proteomics and immunology
    "rgba(63, 63, 63, 0.75)",  # clinical proteomics and immunology
    "rgba(63, 63, 63, 0.75)",  # clinical proteomics and immunology
    "rgba(166, 203, 207, 0.75)",  # Integrated structural biology
    "rgba(63, 63, 63, 0.75)",  # clinical proteomics and immunology
    "rgba(76, 151, 159, 0.75)",  # Bioinformatics platform
    "rgba(166, 166, 166, 0.75)",  # Cellular and molecular imaging platform
    "rgba(164, 143, 169, 0.75)",  # Chemical biology and genome engineering
    "rgba(63, 63, 63, 0.75)",  # clinical proteomics and immunology
    "rgba(0, 0, 0, 0.75)",  # drug discovery any development
    "rgba(210, 229, 231, 0.75)",  # spatial biology
    "rgba(210, 229, 231, 0.75)",  # spatial biology
    "rgba(167, 201, 71, 0.75)",  # genomics platform
    "rgba(4, 92, 100, 0.75)",  # metabolomics
    "rgba(167, 201, 71, 0.75)",  # genomics platform
    "rgba(76, 151, 159, 0.75)",  # Bioinformatics platform
    "rgba(166, 203, 207, 0.75)",  # Integrated structural biology
    "rgba(164, 143, 169, 0.75)",  # Chemical biology and genome engineering
    "rgba(63, 63, 63, 0.75)",  # clinical proteomics and immunology
    "rgba(4, 92, 100, 0.75)",  # metabolomics
    "rgba(73, 31, 83, 0.75)",  # clinical genomics
    "rgba(73, 31, 83, 0.75)",  # clinical genomics
    "rgba(73, 31, 83, 0.75)",  # clinical genomics
    "rgba(73, 31, 83, 0.75)",  # clinical genomics
    "rgba(73, 31, 83, 0.75)",  # clinical genomics
    "rgba(73, 31, 83, 0.75)",  # clinical genomics
]
# *n multiplies the list n times
# increase colours in list/n to add more colours


def map_data(data_matrix, row_value, ideogram_length):
    mapped = np.zeros(data_matrix.shape)
    for j in range(L):
        mapped[:, j] = ideogram_length * data_matrix[:, j] / row_value
    return mapped


mapped_data = map_data(matrix, row_sum, ideogram_length)

idx_sort = np.argsort(mapped_data, axis=1)


def make_ribbon_ends(mapped_data, ideo_ends, idx_sort):
    L = mapped_data.shape[0]
    ribbon_boundary = np.zeros((L, L + 1))
    for k in range(L):
        start = ideo_ends[k][0]
        ribbon_boundary[k][0] = start
        for j in range(1, L + 1):
            J = idx_sort[k][j - 1]
            ribbon_boundary[k][j] = start + mapped_data[k][J]
            start = ribbon_boundary[k][j]
    return [
        [(ribbon_boundary[k][j], ribbon_boundary[k][j + 1]) for j in range(L)]
        for k in range(L)
    ]


ribbon_ends = make_ribbon_ends(mapped_data, ideo_ends, idx_sort)


def control_pts(angle, radius):
    # angle is a  3-list containing angular coordinates of the control points b0, b1, b2
    # radius is the distance from b1 to the  origin O(0,0)

    if len(angle) != 3:
        raise InvalidInputError("angle must have len =3")
    b_cplx = np.array([np.exp(1j * angle[k]) for k in range(3)])
    b_cplx[1] = radius * b_cplx[1]
    return list(zip(b_cplx.real, b_cplx.imag))


def ctrl_rib_chords(l, r, radius):
    # this function returns a 2-list containing control poligons of the two quadratic Bezier
    # curves that are opposite sides in a ribbon
    # l (r) the list of angular variables of the ribbon arc ends defining
    # the ribbon starting (ending) arc
    # radius is a common parameter for both control polygons
    if len(l) != 2 or len(r) != 2:
        raise ValueError("the arc ends must be elements in a list of len 2")
    return [control_pts([l[j], (l[j] + r[j]) / 2, r[j]], radius) for j in range(2)]


ribbon_color = [L * [ideo_colors[k]] for k in range(L)]

# ribbon_color[0][4]=ideo_colors[4]
# ribbon_color[1][2]=ideo_colors[2]
# ribbon_color[2][3]=ideo_colors[3]
# ribbon_color[2][4]=ideo_colors[4]


def make_q_bezier(
    b,
):  # defines the Plotly SVG path for a quadratic Bezier curve defined by the
    # list of its control points
    if len(b) != 3:
        raise valueError("control poligon must have 3 points")
    A, B, C = b
    return f"M {A[0]}, {A[1]} Q {B[0]}, {B[1]} {C[0]}, {C[1]}"


b = [(1, 4), (-0.5, 2.35), (3.745, 1.47)]
make_q_bezier(b)


def make_ribbon_arc(theta0, theta1):
    if test_2PI(theta0) and test_2PI(theta1):
        if theta0 < theta1:
            theta0 = moduloAB(theta0, -pi, pi)
            theta1 = moduloAB(theta1, -pi, pi)
            if (
                theta0 * theta1 > 10
            ):  # was originally 0 changed to 10 to stop this error
                raise ValueError("incorrect angle coordinates for ribbon")

        nr = int(40 * (theta0 - theta1) / pi)
        if nr <= 2:
            nr = 3
        theta = np.linspace(theta0, theta1, nr)
        pts = np.exp(1j * theta)  # points in polar complex form, on the given arc

        string_arc = ""
        for k in range(len(theta)):
            string_arc += f"L {pts.real[k]}, {pts.imag[k]} "
        return string_arc
    else:
        raise ValueError(
            "the angle coordinates for an arc side of a ribbon must be in [0, 2*pi]"
        )


make_ribbon_arc(np.pi / 3, np.pi / 6)  # 3 and 6


def plot_layout(title, plot_size):
    return dict(
        title=title,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        showlegend=False,
        width=plot_size,
        height=plot_size,
        margin=dict(t=25, b=25, l=25, r=25),
        hovermode="closest",
    )


def make_ideo_shape(path, line_color, fill_color):
    # line_color is the color of the shape boundary
    # fill_collor is the color assigned to an ideogram

    return dict(
        line=dict(color=line_color, width=0.45),
        path=path,
        layer="below",
        type="path",
        fillcolor=fill_color,
    )


def make_ribbon(l, r, line_color, fill_color, radius=0.2):
    # l=[l[0], l[1]], r=[r[0], r[1]]  represent the opposite arcs in the ribbon
    # line_color is the color of the shape boundary
    # fill_color is the fill color for the ribbon shape

    poligon = ctrl_rib_chords(l, r, radius)
    b, c = poligon

    return dict(
        line=dict(color=line_color, width=0.5),
        path=make_q_bezier(b)
        + make_ribbon_arc(r[0], r[1])
        + make_q_bezier(c[::-1])
        + make_ribbon_arc(l[1], l[0]),
        type="path",
        layer="below",
        fillcolor=fill_color,
    )


def make_self_rel(l, line_color, fill_color, radius):
    # radius is the radius of Bezier control point b_1

    b = control_pts([l[0], (l[0] + l[1]) / 2, l[1]], radius)

    return dict(
        line=dict(color=line_color, width=0.5),
        path=make_q_bezier(b) + make_ribbon_arc(l[1], l[0]),
        type="path",
        layer="below",
        fillcolor=fill_color,
    )


def invPerm(perm):
    # function that returns the inverse of a permutation, perm
    inv = [0] * len(perm)
    for i, s in enumerate(perm):
        inv[s] = i
    return inv


# title and size (1500 good for print)
layout = plot_layout(" ", 2000)

radii_sribb = [0.4, 0.30, 0.35, 0.39, 0.12]  # these value are set after a few trials

ribbon_info = []
shapes = []

# A given label should only appear once per publication
# Can change if j != k: to if j == k: in below and uncomment function to error check

for k in range(L):
    sigma = idx_sort[k]
    sigma_inv = invPerm(sigma)
    for j in range(k, L):
        if matrix[k][j] == 0 and matrix[j][k] == 0:
            continue
        eta = idx_sort[j]
        eta_inv = invPerm(eta)
        l = ribbon_ends[k][sigma_inv[j]]

        if j != k:
            #     shapes.append(make_self_rel(l, 'rgb(175,175,175)' ,
            #                             ideo_colors[k], radius=radii_sribb[k]))
            #     z = 0.9*np.exp(1j*(l[0]+l[1])/2)

            #     #the text below will be displayed when hovering the mouse over the ribbon
            #     text = f'ERROR {labels[k]} occurs twice {int(matrix[k][k])} in labels'

            #     ribbon_info.append(go.Scatter(x=[z.real],
            #                                y=[z.imag],
            #                                mode='markers',
            #                                marker=dict(size=0.5, color=ideo_colors[k]),
            #                                text=text,
            #                                hoverinfo='text'
            #                                )
            #                       )
            # else:
            r = ribbon_ends[j][eta_inv[k]]
            zi = 0.9 * np.exp(1j * (l[0] + l[1]) / 2)
            zf = 0.9 * np.exp(1j * (r[0] + r[1]) / 2)
            # texti and textf are the strings that will be displayed when hovering the mouse
            # over the two ribbon ends
            texti = f"{labels[k]} worked with {labels[j]} on {int(matrix[k][j])} publications"
            textf = f"{labels[j]} worked with {labels[k]} on {int(matrix[j][k])} publications"

            ribbon_info.append(
                go.Scatter(
                    x=[zi.real],
                    y=[zi.imag],
                    mode="markers",
                    marker=dict(size=0.5, color=ribbon_color[k][j]),
                    text=texti,
                    hoverinfo="text",
                )
            ),
            ribbon_info.append(
                go.Scatter(
                    x=[zf.real],
                    y=[zf.imag],
                    mode="markers",
                    marker=dict(size=0.5, color=ribbon_color[k][j]),
                    text=textf,
                    hoverinfo="text",
                )
            )
            r = (r[1], r[0])  # Reverse these arc ends or you get a twisted ribbon
            # append the ribbon shape
            shapes.append(make_ribbon(l, r, "rgb(175,175,175)", ribbon_color[k][j]))

ideograms = []
for k in range(len(ideo_ends)):
    z = make_ideogram_arc(1.1, ideo_ends[k])
    zi = make_ideogram_arc(1.0, ideo_ends[k])
    m = len(z)
    n = len(zi)
    ideograms.append(
        go.Scatter(
            x=z.real,
            y=z.imag,
            mode="lines",
            line=dict(color=ideo_colors[k], shape="spline", width=0.25),
            text=f"{labels[k]} <br>{int(row_sum[k])} publications",
            hoverinfo="text",
        )
    )

    path = "M "
    for s in range(m):
        path += f"{z.real[s]}, {z.imag[s]} L "

    Zi = np.array(zi.tolist()[::-1])

    for s in range(m):
        path += f"{Zi.real[s]}, {Zi.imag[s]} L "
    path += f"{z.real[0]} ,{z.imag[0]}"

    shapes.append(make_ideo_shape(path, "rgb(150,150,150)", ideo_colors[k]))

data = ideograms + ribbon_info
layout["shapes"] = shapes
fig = go.Figure(data=data, layout=layout)
fig.update_layout(plot_bgcolor="white")
# will need to change this to ensure plot looks circular
fig.update_layout(autosize=False, width=1600, height=850)

# Add labels centrally on outer edge of respective ideogram 'slice'
# int portion set labels at centre point on outer circle edge
# if statements ensure labels do not overlap plot
for i, m in enumerate(labels):
    fig.add_annotation(
        dict(
            font=dict(color="black", size=16),
            x=ideograms[i].x[int((len(ideograms[i].x) / 2))],
            y=ideograms[i].y[int((len(ideograms[i].y) / 2))],
            showarrow=True,
            text=labels[i],
            xanchor="left"
            if ideograms[i].x[int((len(ideograms[i].x) / 2))] > 0
            else "right",
            yanchor="bottom"
            if ideograms[i].y[int((len(ideograms[i].y) / 2))] > 0
            else "top",
            ax=40 if ideograms[i].x[int((len(ideograms[i].x) / 2))] > 0 else -40,
            ay=-30 if ideograms[i].y[int((len(ideograms[i].y) / 2))] > 0 else 30,
        )
    )
# show is useful for checks
# fig.show()
if not os.path.isdir("Plots"):
    os.mkdir("Plots")
fig.write_image("Plots/collabcircosplots_platcol_v2.png", scale=3)
