# This have class to create facility reportlab object to generate 
# facility maetrics pdf. This also have default values and the
# individual value for each facility is mention in facility_reportlab_data.py 
# This is a dependancy for the fstat_pdf_gen.py script

# 250, 175
# 200, 140
# 150, 105

from reportlab.lib.units import mm
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame

class report_lab_obj(object):
    
    def __init__(self, fname="report.pdf", dwidth=250*mm, dheight=175*mm, dpads=0*mm, show_bound=0):
        self.fname = fname
        self.dwidth = dwidth
        self.dheight = dheight
        self.dpads = dpads
        self.show_bound = show_bound
        self.doc = BaseDocTemplate(fname, pagesize=(dwidth, dheight), rightMargin=dpads , leftMargin=dpads, topMargin=dpads, bottomMargin=dpads)
        
        # default frame size
        self.default_fwidth = (self.doc.width - ((3-1)*self.dpads))/3
        self.default_fheight = (self.doc.height - ((2-1)*self.dpads))/2
        
    
    def make_page_templates(self, fdict=None, flist=None, use_default=True):
        """Makes template with frames if fdict not given goes with default 6 frames"""
        
        pad_space = 5*mm
        frames = []
        default_fdict = dict(
            ustat = dict(
                x1 = self.doc.leftMargin,
                y1 = self.doc.bottomMargin + self.default_fheight + self.dpads - pad_space,
                width = self.default_fwidth,
                height = self.default_fheight + pad_space,
                id = "ustat",
                showBoundary = self.show_bound,
                leftPadding = 10*mm,
                topPadding = 15*mm
                ),
            ctbar = dict(
                x1 = self.doc.leftMargin + self.default_fwidth + self.dpads,
                y1 = self.doc.bottomMargin + self.default_fheight + self.dpads - pad_space,
                width = self.default_fwidth,
                height = self.default_fheight + pad_space,
                id = "ctbar",
                showBoundary = self.show_bound,
                leftPadding = 0*mm,
                topPadding = 15*mm,
                rightPadding = 0*mm,
                bottomPadding = 0*mm
                ),
            jfbar = dict(
                x1 = (self.doc.leftMargin + self.default_fwidth + self.dpads)*2,
                y1 = self.doc.bottomMargin + self.default_fheight + self.dpads - pad_space,
                width = self.default_fwidth,
                height = self.default_fheight + pad_space,
                id = "jfbar",
                showBoundary = self.show_bound,
                leftPadding = 0*mm,
                topPadding = 15*mm,
                rightPadding = 0*mm,
                bottomPadding = 0*mm
                ),
            usr_y1 = dict(
                x1 = self.doc.leftMargin,
                y1 = self.doc.bottomMargin,
                width = self.default_fwidth,
                height = self.default_fheight - pad_space,
                id = "usr_y1",
                showBoundary = self.show_bound,
                leftPadding = 0*mm,
                topPadding = 0*mm,
                rightPadding = 0*mm,
                bottomPadding = 0*mm
                ),
            usr_y2 = dict(
                x1 = self.doc.leftMargin + self.default_fwidth + self.dpads,
                y1 = self.doc.bottomMargin,
                width = self.default_fwidth,
                height = self.default_fheight - pad_space,
                id = "usr_y2",
                showBoundary = self.show_bound,
                leftPadding = 0*mm,
                topPadding = 0*mm,
                rightPadding = 0*mm,
                bottomPadding = 0*mm
                ),
            usr_y3 = dict(
                x1 = (self.doc.leftMargin + self.default_fwidth + self.dpads)*2,
                y1 = self.doc.bottomMargin,
                width = self.default_fwidth,
                height = self.default_fheight - pad_space,
                id = "usr_y3",
                showBoundary = self.show_bound,
                leftPadding = 0*mm,
                topPadding = 0*mm,
                rightPadding = 0*mm,
                bottomPadding = 0*mm
                )
            )
        if fdict == None:
            fdict = {}
               
        if flist == None:
            flist = ['ustat', 'ctbar', 'jfbar', 'usr_y1', 'usr_y2', 'usr_y3']
        
        for frm in flist:
            kwargs = fdict.get(frm, default_fdict[frm])if use_default else fdict[frm]
            frames.append(Frame(**kwargs))
        
        self.doc.addPageTemplates([PageTemplate(id='unit_metrics', frames=frames)])
