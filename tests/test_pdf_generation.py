import unittest

import PdfGenerator


class TestPdfGenerator(unittest.TestCase):

    def test_generate_test(self):
        PdfGenerator.generate_pdf(file_path='testfile.pdf', content='')
        # Not return value


if __name__ == '__main__':
    unittest.main()
