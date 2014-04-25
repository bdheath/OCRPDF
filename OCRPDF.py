
# Tool for OCR'ing multi-page PDFs
#
# Usage is OCRPDF(filename, [conversion resolution], [verbose])
# standard conversion resolution is 300; higher numbers produce better results, but are slower

# Dependencies
# --- EXTERNAL DEPENDENCIES
# - ImageMagick
# - GhostScript (PythonMagick dependency)
# - Tesseract OCR engine
# --- PYTHON DEPENDENCIES
# - PIL (or Pillow)
# - PythonMagick (implementation of ImageMagick)
# - Helpful setup guidance here: http://stackoverflow.com/questions/13984357/pythonmagick-cant-find-my-pdf-files
# - pyPdf
# - pytesser
#   (modify pytesser.py if needed to change "import Image" to "from PythonMagick import Image")
# - os
# - re

# Return object is
#	obj
#		t : full text (str)
#		t_clean : full text after cleanup algorithm (str)
#		pages : number of pages (int)
#		p : list of obj
#			pagenum : pagenum (int)
#			t : text from this page (str)
#			t_clean : text from this page after cleanup (str)

from pyPdf import PdfFileWriter, PdfFileReader
from pytesser import *
import PythonMagick
from PIL import Image
import os
import re


class OCRResult:
	t = ''
	t_clean = ''
	pages = 0
	p = []
	
	def __init__(self, t, t_clean, pages, p):
		self.t = t
		self.t_clean = t_clean
		self.pages = pages
		self.p = p
		return None
	
class OCRPage:
	pagenum = 0
	t = ''
	t_clean = ''
	
	def __init__(self, pagenum, t, t_clean):
		self.pagenum = pagenum
		self.t = t
		self.t_clean = t_clean
		return None

class OCRPDF:
	
	def __init__(self):
		return None

	def OCRCleanup(self,text):
		cleaned = []
		CONSONANTS = re.compile('[bcdfghjklmnpqrstvwxz]{5}', re.IGNORECASE)
		DIGITS = re.compile(r'\d{5}')
		REPEAT = re.compile('([^0-9])\1{2,}')
		MULTIJUNK = re.compile('[\*\.\#\@\^\&\$\!\,\[\]\\\,]{2,}')
		# break into a series of words
		words = re.split(r'(\W+)', text)
		for w in words:
			if not re.search(CONSONANTS, w) \
				and len(w) <= 30 \
				and not re.search(DIGITS, w) \
				and not re.search(MULTIJUNK, w) \
				and not re.search(REPEAT, w):
				cleaned.append(w)
		text = ''.join(cleaned)
		text = re.sub(r'\n', ' \n ', text)
		return text

	def OCR(self, fn, resolution=300, verbose=False, part=''):
		
		i = 1
		pdf = PdfFileReader(file(fn, 'rb'))
		if pdf.getIsEncrypted():
			if pdf.decrypt(''):
				jnk = 0
			else:
				return false
		pagedata = []
		text = ''
		
		for p in pdf.pages:
		
			if verbose:
				print ' --- ' + str(i)
		
			part = str(part)
		
			# Temporary filenames for ImageMagick conversion
			pgfile = 'c:/tmp-' + part + '-' + str(i) + '.pdf'
			pgfilejpg = 'c:/tmp-' + part + '-' + str(i) + '.jpg'
			
			# Parse this page
			output = PdfFileWriter()
			output.addPage(p)
			outputStream = file(pgfile,'wb')
			output.write(outputStream)
			outputStream.close()
		
			# Convert this page to a high-resolution JPEG
			img = PythonMagick.Image()
			img.density(str(resolution))
			img.read(pgfile)
			img.write(pgfilejpg)
			
			# OCR the converted JPG
			im = Image.open(pgfilejpg)
			if(len(im.split()) == 4):
				r, g, b, a = im.split()
				im = Image.merge('RGB', (r,g,b))

			t = image_to_string(im)
			
			# Cleanup
			os.remove(pgfile)
			os.remove(pgfilejpg)
			
			# Add to data object
			pagedata.append(OCRPage(i, t, self.OCRCleanup(t)))
			text += t

			i += 1
		
		# Produce the output data object
		result = OCRResult(text, self.OCRCleanup(text), (i-1), pagedata)

		return result