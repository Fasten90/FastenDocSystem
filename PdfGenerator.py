import os

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


###############################################################################


def debug_log(str):
    print(str)


def make_directory(directory):

    if not os.path.exists(directory):
        os.makedirs(directory)


def generate_pdf(filepath):

    canvas_obj = canvas.Canvas(filepath,
                               pagesize=A4)

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

