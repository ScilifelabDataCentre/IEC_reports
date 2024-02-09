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
        name_fsize = 22,
        annotation_fsize = 30
    ),
    u_y2_spec = dict(
        name_fsize = 20,
        annotation_fsize = 29
    ),
    figsize = dict(
        u_y2 = dict(imw=88, imh=68)
    )
)

unit_pdf_data['Ancient DNA'] = dict(
    usr_plot_spec = dict(
        stacked = True
    ),
    u_y3_spec = dict(
        name_fsize = 25,
        annotation_fsize = 33,
        stacked = True
    ),
    figsize = dict(
        u_y1 = dict(imw=85, imh=68),
        u_y2 = dict(imw=92, imh=70),
        u_y3 = dict(imw=80, imh=68)
    )
)

unit_pdf_data['National Genomics Infrastructure'] = dict(
    style = ("inner_heading", "page_text_s"),
    u_y1_spec = dict(
        name_fsize = 23,
        annotation_fsize = 32
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
        u_y1 = dict(imw=80, imh=65),
        u_y2 = dict(imw=90, imh=70),
        u_y3 = dict(imw=90, imh=70)
    )
)

unit_pdf_data['Clinical Genomics'] = dict(
    usr_plot_spec = dict(
        name_fsize = 22,
        annotation_fsize = 35
    ),
    u_y2_spec = dict(
        name_fsize = 20,
        annotation_fsize = 35
    )
)

unit_pdf_data['Autoimmunity and Serology Profiling'] = dict(
    u_y1_spec = dict(
        name_fsize = 20,
        annotation_fsize = 33,
        stacked  = True
    ),
    u_y2_spec = dict(
        name_fsize = 25,
        annotation_fsize = 33
    ),
    u_y3_spec = dict(
        name_fsize = 25,
        annotation_fsize = 33
    ),
    figsize = dict(
        u_y1 = dict(imw=92, imh=70),
        u_y2 = dict(imw=80, imh=67),
        u_y3 = dict(imw=80, imh=67)
    )
)

unit_pdf_data['Cellular Immunomonitoring'] = dict(
    usr_plot_spec = dict(
        name_fsize = 25,
        annotation_fsize = 34,
        stacked = True
    )
)

unit_pdf_data['Chalmers Mass Spectrometry Infrastructure'] = dict(
    u_y1_spec = dict(
        name_fsize = 21,
        annotation_fsize = 32,
        stacked = True
    ),
    u_y2_spec = dict(
        name_fsize = 22,
        annotation_fsize = 32,
    ),
    u_y3_spec = dict(
        name_fsize = 21,
        annotation_fsize = 32,
        stacked = True
    ),
    figsize = dict(
        u_y1 = dict(imw=93, imh=72),
        u_y2 = dict(imw=86, imh=72),
        u_y3 = dict(imw=92, imh=72)
    )
)

unit_pdf_data['Exposomics'] = dict(
    usr_plot_spec = dict(
        name_fsize = 24,
        annotation_fsize = 34,
        stacked = True
    ),
    u_y2_spec = dict(
        name_fsize = 26,
        annotation_fsize = 35,
        stacked = True
    ),
    figsize = dict(
        u_y1 = dict(imw=83, imh=67),
        u_y2 = dict(imw=83, imh=67)
    )
)

unit_pdf_data['Cryo-EM'] = dict(
    u_y1_spec = dict(
        name_fsize = 21,
        annotation_fsize = 31
    ),
    figsize = dict(
        u_y1 = dict(imw=90, imh=70),
        u_y2 = dict(imw=90, imh=70)
    )
)

unit_pdf_data['Integrated Microscopy Technologies Gothenburg'] = dict(
    u_y3_spec = dict(
        name_fsize = 21,
        annotation_fsize = 30
    ),
    figsize = dict(
        u_y1 = dict(imw=86, imh=68),
        u_y2 = dict(imw=85, imh=68),
        u_y3 = dict(imw=90, imh=70)
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
        u_y1 = dict(imw=86, imh=70),
        u_y2 = dict(imw=92, imh=71),
        u_y3 = dict(imw=90, imh=70)
    )
)

unit_pdf_data['Structural Proteomics'] = dict(
    u_y1_spec = dict(
        name_fsize = 25,
        annotation_fsize = 32,
        stacked = True
    ),
    figsize = dict(
        u_y1 = dict(imw=82, imh=68)
    )
)

unit_pdf_data['Swedish NMR Centre'] = dict(
    u_y2_spec = dict(
        name_fsize = 24,
        annotation_fsize = 34
    ),
    figsize = dict(
        u_y2 = dict(imw=77, imh=63)
    )
)
