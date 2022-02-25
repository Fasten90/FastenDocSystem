import unittest


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


class TestFakeGeneration(unittest.TestCase):

    def test_generate_test(self):
        result = generate_test_content()
        assert result


if __name__ == '__main__':
    unittest.main()
