"""This script creates pdf with unit stats"""

# Specific imports from reportlab
from reportlab.platypus import Paragraph, Spacer, FrameBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER

from svglib.svglib import svg2rlg
from pathlib import Path

from data_loader import unit_data, units_list  # funding_data
from unit_pdf_template import report_lab_obj
from unit_pdf_specs import unit_pdf_data
from plot_gen import publication_plot, users_plot


def get_image_story(impath, imw=83, imh=65, title=None, style=None, tech_pub_count=0):
    out_story = [FrameBreak()]
    if title and style:
        out_story.append(
            Paragraph(
                "<font color='#95C11E' name=Arial-bold>{}</font>".format(title), style
            )
        )
    img = svg2rlg(impath)
    scaling_factor = imw * mm / img.width
    img.width = imw * mm
    img.height = imh * mm
    img.scale(scaling_factor, scaling_factor)
    out_story.append(img)
    if title == "Publications by category":
        out_story.append(Spacer(1, 1 * mm))
        out_story.append(
            Paragraph(
                "<font color='#95C11E' name=Arial-bold>No. of Tech Dev Publications 2021 - 2023:</font> {}".format(
                    tech_pub_count
                ),
                styles[text_style],
            )
        )
    return out_story


years_to_work = [2020, 2021, 2022]

# Create output dir if doesn't exist
Path("Pdfs").mkdir(parents=True, exist_ok=True)

# register font to use
pdfmetrics.registerFont(TTFont("Arial", "Arial.ttf"))
pdfmetrics.registerFont(TTFont("Arial-bold", "Arial Bold.ttf"))

# define styles which are mandatory for paragraph elements
styles = getSampleStyleSheet()

styles.add(
    ParagraphStyle(
        name="inner_heading",
        parent=styles["Heading1"],
        fontName="Arial",
        fontSize=12,
        color="#FF00AA",
        leading=11,
        afterspace=0,
    )
)

styles.add(
    ParagraphStyle(
        name="page_text",
        parent=styles["Normal"],
        fontName="Arial",
        fontSize=10,
        bold=0,
        color="#000000",
        leading=13,
    )
)

styles.add(
    ParagraphStyle(
        name="page_text_s",
        parent=styles["Normal"],
        fontName="Arial",
        fontSize=9.5,
        bold=0,
        color="#000000",
        leading=13,
    )
)

styles.add(
    ParagraphStyle(
        name="bar_plot_title",
        parent=styles["Heading1"],
        fontName="Arial",
        fontSize=12,
        color="#FF00AA",
        leftIndent=18,
        leading=0,
        afterspace=0,
    )
)

styles.add(
    ParagraphStyle(
        name="pie_plot_title",
        parent=styles["Heading1"],
        fontName="Arial",
        fontSize=12,
        color="#FF00AA",
        leading=5,
        afterspace=0,
        alignment=TA_CENTER,
    )
)

styles.add(
    ParagraphStyle(
        name="no_data_info",
        parent=styles["Heading1"],
        fontName="Arial",
        fontSize=17,
        color="#FF00AA",
        spaceBefore=0,
        alignment=TA_CENTER,
    )
)

# units_list = [
#     "Swedish Metabolomics Centre"
# ]

# Generate facility stat plot for all facilities
for unit in units_list:

    print("Processing {}".format(unit))

    unit_fname = unit.replace(",", "")
    unit_grph = unit_pdf_data.get(unit, {})
    unit_stat = unit_data[unit_data.Unit == unit].fillna(0).to_dict("records")[0]

    head_style, text_style = unit_grph.get("style", ("inner_heading", "page_text"))
    caller_dict = {}
    all_frame_names = ["ustat", "ctbar", "jfbar", "usr_y1", "usr_y2", "usr_y3"]
    frames_to_work = unit_grph.get("frames", {}).get("flist", all_frame_names)[1:]

    # set base template
    unit_replab = report_lab_obj(fname="Pdfs/{}.pdf".format(unit))

    story = []

    # Publication bar plots
    cat_plot, jif_plot, tech_pub_count = publication_plot(unit, "svg")
    if cat_plot:
        caller_dict["ctbar"] = dict(
            impath=cat_plot,
            title="Publications by category",
            style=styles["bar_plot_title"],
            tech_pub_count=tech_pub_count,
            **unit_grph.get("figsize", {}).get("cat", {})
        )
    else:
        print("{} - missing category bar".format(unit))
    if jif_plot:
        caller_dict["jfbar"] = dict(
            impath=jif_plot,
            title="Publications by JIF",
            style=styles["bar_plot_title"],
            **unit_grph.get("figsize", {}).get("jif", {})
        )
    else:
        print("{} - missing JIF bar".format(unit))

    # Users affiliation plot
    usr_plot_spec = unit_grph.get("u_y1_spec", {}) or unit_grph.get("usr_plot_spec", {})
    usr_y1_plot = users_plot(unit, 2021, "svg", **usr_plot_spec)
    if usr_y1_plot:
        caller_dict["usr_y1"] = dict(
            impath=usr_y1_plot,
            title="Users 2021",
            style=styles["pie_plot_title"],
            **unit_grph.get("figsize", {}).get("u_y1", {})
        )
    else:
        print("{} - missing 2021 users".format(unit))

    usr_plot_spec = unit_grph.get("u_y2_spec", {}) or unit_grph.get("usr_plot_spec", {})
    usr_y2_plot = users_plot(unit, 2022, "svg", **usr_plot_spec)
    if usr_y2_plot:
        caller_dict["usr_y2"] = dict(
            impath=usr_y2_plot,
            title="Users 2022",
            style=styles["pie_plot_title"],
            **unit_grph.get("figsize", {}).get("u_y2", {})
        )
    else:
        print("{} - missing 2022 users".format(unit))

    usr_plot_spec = unit_grph.get("u_y3_spec", {}) or unit_grph.get("usr_plot_spec", {})
    usr_y3_plot = users_plot(unit, 2023, "svg", **usr_plot_spec)
    if usr_y3_plot:
        caller_dict["usr_y3"] = dict(
            impath=usr_y3_plot,
            title="Users 2023",
            style=styles["pie_plot_title"],
            **unit_grph.get("figsize", {}).get("u_y3", {})
        )
    else:
        print("{} - missing 2023 users".format(unit))

    story.append(
        Paragraph(
            "<font color='#95C11E' name=Arial-bold>Basic Information</font>",
            styles[head_style],
        )
    )
    story.append(
        Paragraph(
            "<font name=Arial-bold>{}:</font> {}".format(
                "PD" if unit in ["Clinical Genomics", "Drug Discovery and Development"] else "HU",
                unit_stat["HOU"]
                ),
            styles[text_style],
        )
    )
    if unit_stat["Co_HOU"]:
        story.append(
            Paragraph(
                "<font name=Arial-bold>Co-PD:</font> {}".format(unit_stat["Co_HOU"]),
                styles[text_style],
            )
        )
    story.append(
        Paragraph(
            "<font name=Arial-bold>Host University:</font> {}".format(
                unit_stat["H_uni"]
            ),
            styles[text_style],
        )
    )
    story.append(
        Paragraph(
            "<font name=Arial-bold>SciLifeLab unit since:</font> {}".format(
                unit_stat["SLL_since"]
            ),
            styles[text_style],
        )
    )
    story.append(
        Paragraph(
            "<font name=Arial-bold>FTEs:</font> {}".format(unit_stat["SLL_FTEs"]),
            styles[text_style],
        )
    )
    if unit_stat["PSD"]:
        story.append(
            Paragraph(
                "<font name=Arial-bold>PSD:</font> {}".format(unit_stat["PSD"]),
                styles[text_style],
            )
        )

    # story.append(Paragraph("<font name=Arial-bold>FTEs financed by SciLifeLab:</font> {}".format(unit_stat['SLL_FTEs']), styles[text_style]))
    story.append(Spacer(1, 3 * mm))
    story.append(
        Paragraph(
            "<font color='#95C11E' name=Arial-bold>Funding 2023 (kSEK)</font>",
            styles[head_style],
        )
    )
    story.append(
        Paragraph(
            "<font name=Arial-bold>SciLifeLab:</font> {}".format(
                str(unit_stat["Fund_SLL"])
            ),
            styles[text_style],
        )
    )
    story.append(
        Paragraph(
            "<font name=Arial-bold>Other:</font> {}".format(
                str(unit_stat["Fund_other"])
            ),
            styles[text_style],
        )
    )
    story.append(
        Paragraph(
            "<font name=Arial-bold>User Fees:</font> {}".format(
                str(unit_stat["Fee_total"])
            ),
            styles[text_style],
        )
    )

    # call for frames and add the images
    for frm in frames_to_work:
        if frm in caller_dict:
            story.extend(get_image_story(**caller_dict[frm]))
        else:
            story.append(FrameBreak())

    unit_replab.make_page_templates(**unit_grph.get("frames", {}))
    unit_replab.doc.build(story)
