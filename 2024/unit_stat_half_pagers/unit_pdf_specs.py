#/usr/bin/env python
# -*- coding: utf-8 -*-

# This only contains the plot values for individual facility
# This is a dependancy for the fstat_pdf_gen.py script

from reportlab.lib.units import mm

base_dir = "Pdfs/"
doc_width = 250*mm
doc_height = 150*mm
doc_pads = 0*mm
show_bound = 0

def calc_frame_width(dw, dpd, ncol=3):
    return (dw - ((ncol-1)*dpd))/ncol

def calc_frame_height(dh, dpd, nrow=2):
    return (dh - ((nrow-1)*dpd))/nrow

unit_pdf_data = {}

# Facilites with huge user data  #

unit_pdf_data['Support, Infrastructure and Training'] = dict(
    usr_plot_spec = dict(
        name_fsize = 23,
        annotation_fsize = 30
    ),
    u_y2_spec = dict(
        name_fsize = 21,
        annotation_fsize = 29
    ),
    figsize = dict(
        u_y2 = dict(imw=88, imh=68)
    )
)

unit_pdf_data['Ancient DNA'] = dict(
    u_y3_spec = dict(
        name_fsize = 27,
        annotation_fsize = 35
    ),
    figsize = dict(
        u_y3 = dict(imw=80, imh=63)
    )
)

unit_pdf_data['National Genomics Infrastructure'] = dict(
    style = ("inner_heading", "page_text_s"),
    u_y1_spec = dict(
        name_fsize = 25,
        annotation_fsize = 34
    ),
    u_y2_spec = dict(
        name_fsize = 21,
        annotation_fsize = 30
    ),
    u_y3_spec = dict(
        name_fsize = 21,
        annotation_fsize = 30
    ),
    figsize = dict(
        u_y1 = dict(imw=80, imh=63),
        u_y2 = dict(imw=90, imh=70),
        u_y3 = dict(imw=90, imh=70)
    )
)

unit_pdf_data['Clinical Genomics Gothenburg'] = dict(
    usr_plot_spec = dict(
        name_fsize = 27,
        annotation_fsize = 35
    )
)

unit_pdf_data['Clinical Genomics Linköping'] = dict(
    usr_plot_spec = dict(
        name_fsize = 27,
        annotation_fsize = 35
    )
)

unit_pdf_data['Clinical Genomics Lund'] = dict(
    usr_plot_spec = dict(
        name_fsize = 27,
        annotation_fsize = 35
    )
)

unit_pdf_data['Clinical Genomics Stockholm'] = dict(
    usr_plot_spec = dict(
        name_fsize = 26,
        annotation_fsize = 34
    )
)

unit_pdf_data['Clinical Genomics Umeå'] = dict(
    usr_plot_spec = dict(
        name_fsize = 27,
        annotation_fsize = 35
    )
)

unit_pdf_data['Clinical Genomics Uppsala'] = dict(
    usr_plot_spec = dict(
        name_fsize = 26,
        annotation_fsize = 34
    )
)

unit_pdf_data['Clinical Genomics Örebro'] = dict(
    usr_plot_spec = dict(
        name_fsize = 27,
        annotation_fsize = 35
    )
)

unit_pdf_data['Autoimmunity and Serology Profiling'] = dict(
    u_y2_spec = dict(
        name_fsize = 27,
        annotation_fsize = 35
    ),
    u_y3_spec = dict(
        name_fsize = 27,
        annotation_fsize = 35
    ),
    figsize = dict(
        u_y2 = dict(imw=80, imh=63),
        u_y3 = dict(imw=80, imh=63)
    )
)

unit_pdf_data['Cellular Immunomonitoring'] = dict(
    u_y1_spec = dict(
        name_fsize = 27,
        annotation_fsize = 35
    ),
    figsize = dict(
        u_y1 = dict(imw=70, imh=62),
        u_y2 = dict(imw=80, imh=62),
        u_y3 = dict(imw=83, imh=62)
    )
)

unit_pdf_data['Chalmers Mass Spectrometry Infrastructure'] = dict(
    u_y1_spec = dict(
        name_fsize = 27,
        annotation_fsize = 35
    ),
    figsize = dict(
        u_y1 = dict(imw=80, imh=63)
    )
)

unit_pdf_data['Exposomics'] = dict(
    u_y2_spec = dict(
        name_fsize = 27,
        annotation_fsize = 35
    ),
    figsize = dict(
        u_y2 = dict(imw=80, imh=63)
    )
)

unit_pdf_data['Integrated Microscopy Technologies Umeå'] = dict(
    u_y2_spec = dict(
        name_fsize = 22,
        annotation_fsize = 30
    ),
    u_y3_spec = dict(
        name_fsize = 22,
        annotation_fsize = 30
    ),
    figsize = dict(
        u_y2 = dict(imw=90, imh=70),
        u_y3 = dict(imw=90, imh=70)
    )
)

unit_pdf_data['Swedish NMR Centre'] = dict(
    u_y2_spec = dict(
        name_fsize = 27,
        annotation_fsize = 34
    ),
    figsize = dict(
        u_y2 = dict(imw=75, imh=63)
    )
)
