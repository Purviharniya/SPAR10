import typing
from borb.pdf.document import Document
from borb.pdf.pdf import PDF
from docx2pdf import convert #convert doc to pdf
from fpdf import FPDF #convert txt to pdf 
from borb.toolkit.text.simple_text_extraction import SimpleTextExtraction
import textract
import codecs

def main(filename):

    # check = allowed_files_for_redaction(filename) 
    # if check==True:
    #     extension = filename.split('.')[-1]
    # else:
    #     return "Invalid extension"
    extension = filename.split('.')[-1]

    string = ''' ''' #extracted string

    if extension == 'pdf':

        # filename = filename.split('.')[0] + '.pdf'

        d: typing.Optional[Document] = None
        l: SimpleTextExtraction = SimpleTextExtraction()
        with open(filename, "rb") as pdf_in_handle:
            d = PDF.loads(pdf_in_handle, [l])

        assert d is not None
        #print("length: ",len(d))
        
        for i in range(len(d)):
            string += l.get_text_for_page(i)

    else:
        string = textract.process(filename,method='tesseract')
        string = codecs.decode(string, "unicode_escape")    

    return string
    
st = main("temp2.docx")
print(st)