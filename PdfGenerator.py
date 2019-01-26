import os


from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet
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
    styleFooter = styleN
    styleFooter.alignment = TA_CENTER
    styleH = styles['Heading1']

    def header_footer(canvas, doc, content):
        # TODO: content could be decided here
        canvas.saveState()

        # Header
        w, h = content.wrap(doc.width, doc.topMargin)
        content.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - h)

        # Footer
        page_num = canvas.getPageNumber()
        footer_text = Paragraph("%s" % page_num, styleFooter)
        w, h = footer_text.wrap(doc.width, doc.bottomMargin)
        footer_text.drawOn(canvas, doc.leftMargin, h)

        canvas.restoreState()

    doc = BaseDocTemplate(filepath, pagesize=A4)
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height - 2 * cm, id='normal')
    header_content = Paragraph("This is a multi-line header.  It goes on every page.  " * 8, styleN)
    template = PageTemplate(id='test', frames=frame, onPage=partial(header_footer, content=header_content))
    doc.addPageTemplates([template])

    text = []
    for i in range(111):
        text.append(Paragraph("This is line %d." % i, styleN))

    # Finish pdf
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

