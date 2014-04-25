OCRPDF
======

OCRPDF is a Python wrapper that helps you quiclkly OCR multi-page PDF documents

Requirements
============
You must have already installed:
* ImageMagik (http://www.imagemagick.org/script/binary-releases.php)
* GhostScript (http://www.ghostscript.com)
* The Tesseract OCR engine (https://code.google.com/p/tesseract-ocr/)

Dependencies
============

You must also have installed the following Python modules:
* PIL (or Pillow)
* Pytesser (you may have to modify pytesser.py if needed to change "import Image" to "from PythonMagick import Image")
* PythonMagik (helpful guidance can be found at http://stackoverflow.com/questions/13984357/pythonmagick-cant-find-my-pdf-files)

Basic Usage
===========
To create a new instance of OCRPDF and OCR a file:
```python
from OCRPDF import OCRPDF

ocrTool = OCRPDF()
result = ocrTool.OCRPDF('YourFileNameHere')
```

This returns an object of:
```
	t         : raw text
	t_clean   : cleaned text
	pages     : number of pages
	p         : list of page data objects
	            pagenum : page number
				t       : raw text from this page
				t_clean : cleaned text from this page
```

So to view the raw text from page 3 of your document:
```
print result.p[2].t
```