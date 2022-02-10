# Fasten90

Fasten90 is a project to create a prototype of a tool to use reportlab to export md and csv data to a PDF document. 

## Installation

Use the install.bat to install Fasten90.

```python
python -m venv venv

venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Usage

Arguments of PdfGenerator.py:
* `--input-path`
  * input directory path. Where the CSV files are existing
* `--open-after-generated`
  * Opening pdf after the generation
* `--export-pdf-file-path`
  * Export PDF file path where it shall be generated

e.g. 
`venv\Scripts\python.exe PdfGenerator.py --input-path=input --open-after-generated --export-pdf-file-path=out/FastenDoc.pdf`


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT] (Please refer to LICENCE.txt).(https://choosealicense.com/licenses/mit/)


> Written with [StackEdit](https://stackedit.io/).
