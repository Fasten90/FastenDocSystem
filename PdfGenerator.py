import os
import time

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Paragraph
from functools import partial


###############################################################################


def debug_log(str):
    print(str)


def make_directory(directory):
    # Make a directory in the file system
    if not os.path.exists(directory):
        os.makedirs(directory)


def generate_pdf(filepath):

    styles = getSampleStyleSheet()
    styleN = styles['Normal']
    # TODO: self.styles.add(ParagraphStyle ...
    styleHeaderFooter = ParagraphStyle(name='StyleHeaderFooter', alignment=TA_CENTER)
    #styleFooter.alignment = TA_CENTER
    styleH = styles['Heading1']

    def header_footer(canvas, doc):
        canvas.saveState()

        # Header
        header_text = Paragraph("FastenPdf.  ", styleHeaderFooter)
        w, h = header_text.wrap(doc.width, doc.topMargin)
        # NOTE: Original recommended: header_text.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - h)
        offset_header = 0.5 * cm
        header_text.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin + offset_header)

        # Footer
        page_num = canvas.getPageNumber()
        footer_text = Paragraph("%s" % page_num, styleHeaderFooter)
        w, h = footer_text.wrap(doc.width, doc.bottomMargin)
        offset_footer = 1 * cm
        footer_text.drawOn(canvas, doc.leftMargin, offset_footer)

        canvas.restoreState()

    # Doc initialization
    doc = BaseDocTemplate(filepath, pagesize=A4, leftMargin=2*cm, rightMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height,
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0,
                  id='normal')
    template = PageTemplate(id='test', frames=frame, onPage=partial(header_footer))
    doc.addPageTemplates([template])

    text = []
    for i in range(111):
        text.append(Paragraph("This is line %d." % i, styleN))

    # Finish pdf
    try:
        doc.build(text)
    except PermissionError as ex:
        debug_log("Error: {}".format(ex))
        debug_log("Please close the pdf document!")

        # TODO: This solution is not works fine
        time_sec = 20
        for i in range(time_sec, 0, -1):
            # Wait 1 sec
            debug_log("Wait {} seconds...".format(i))
            time.sleep(1)

        # Retry generation
        doc.build(text)


    """
    canvas_obj = canvas.Canvas(filepath, pagesize=A4)

    # Create textobject
    textobject = canvas_obj.beginText()

    # Set text location (x, y)
    textobject.setTextOrigin(10, 730)

    spacing = 0
    for indent in range(8):
        textobject.setCharSpace(spacing)
        line = '{} - ReportLab spacing demo'.format(spacing)
        textobject.textLine(line)
        spacing += 0.7

    canvas_obj.drawText(textobject)
    canvas_obj.save()
    """


def open_pdf(filepath):
    os.system("start " + filepath)


def main():
    debug_log("Pdf generation started...")

    directory = "out"
    make_directory(directory)

    filename = "test.pdf"
    filepath = os.path.join(directory, filename)

    generate_pdf(filepath)

    open_pdf(filepath)

    debug_log("Pdf generation finished...")


if __name__ == "__main__":
    # execute only if run as a script
    main()

