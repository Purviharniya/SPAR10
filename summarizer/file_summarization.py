import typing
from borb.pdf.document import Document
from borb.pdf.pdf import PDF
from borb.toolkit.text.simple_text_extraction import SimpleTextExtraction
import textract
import codecs

def file_summarizer(filename):
  extension = filename.split('.')[-1]
  string = ''' ''' #extracted string

  if extension == 'pdf':

    d: typing.Optional[Document] = None
    l: SimpleTextExtraction = SimpleTextExtraction()
    with open(filename, "rb") as pdf_in_handle:
      d = PDF.loads(pdf_in_handle, [l])

    assert d is not None
    
    for i in range(len(d)):
      string += l.get_text_for_page(i)
      
  else:
    string = textract.process(filename,method='tesseract')
    string = codecs.decode(string, "unicode_escape") 
    
  return string
 