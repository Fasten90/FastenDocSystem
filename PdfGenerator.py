import os
import time
import csv
import glob
import textwrap

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Paragraph,Table, TableStyle
from functools import partial


def debug_log(msg):
    print(msg)


def make_directory(directory):
    # Make a directory in the file system
    if not os.path.exists(directory):
        os.makedirs(directory)


def generate_pdf(file_path, content):

    styles = getSampleStyleSheet()
    styleN = styles['Normal']
    # TODO: self.styles.add(ParagraphStyle ...
    styleHeaderFooter = ParagraphStyle(name='StyleHeaderFooter', alignment=TA_CENTER)
    #styleFooter.alignment = TA_CENTER
    styleH = styles['Heading1']

    def header_footer(canvas, doc):
        canvas.saveState()

        # Header
        header_text = Paragraph("FastenPdf", styleHeaderFooter)
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
    doc = BaseDocTemplate(file_path, pagesize=A4,
                          leftMargin=2 * cm, rightMargin=2 * cm, topMargin=2 * cm, bottomMargin=2 * cm)
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height,
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0,
                  id='normal')
    template = PageTemplate(id='test', frames=frame, onPage=partial(header_footer))
    doc.addPageTemplates([template])
    doc.title = 'FastenDoc'

    # Content
    # Provided in input argument

    # Finish pdf
    try:
        doc.build(content)
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
        doc.build(content)


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


def generate_content():
    content = []
    styles = getSampleStyleSheet()
    styleN = styles['Normal']
    # Check input directory
    file_list = glob.glob("input/*.csv")
    print("Found files: {}".format(file_list))
    file_list.sort()
    for file in file_list:
        table_data = []
        with open(file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                # Check content
                new_row = []
                for cell in row:
                    if len(cell) > 60:
                        cell = "\n".join(textwrap.wrap(cell, 60))
                    new_row.append(cell)
                table_data.append(new_row)
        content.append(Paragraph("Compiler warning file: {}".format(file), styleN))
        t = Table(table_data)
        # Set header style of table
        t.setStyle(TableStyle([('BACKGROUND', (0, 0), (5, 0), colors.grey),
                               ('TEXTCOLOR', (0, 0), (5, 0), colors.white)]))
        content.append(t)
    return content


def generate_test_content():
    content = []
    styles = getSampleStyleSheet()
    styleN = styles['Normal']

    # Paragraph
    for i in range(111):
        content.append(Paragraph("This is line %d." % i, styleN))

    # Table
    data = [['00', '01', '02', '03', '04'],
            ['10', '11', '12', '13', '14'],
            ['20', '21', '22', '23', '24'],
            ['30', '31', '32', '33', '34']]
    t = Table(data)
    # Set header style of table
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (5, 0), colors.grey),
                           ('TEXTCOLOR', (0, 0), (5, 0), colors.white)]))
    content.append(t)

    return content


def open_pdf(file_path):
    os.system("start " + file_path)


def main():
    debug_log("Pdf generation started...")

    directory = "out"
    make_directory(directory)

    filename = "FastenDoc.pdf"
    file_path = os.path.join(directory, filename)

    content = generate_content()
    generate_pdf(file_path, content=content)

    open_pdf(file_path)

    debug_log("Pdf generation finished...")


if __name__ == "__main__":
    # execute only if run as a script
    main()

