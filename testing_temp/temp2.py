import PyPDF2
fhandle = open(r'temp2.pdf', 'rb')
pdfReader = PyPDF2.PdfFileReader(fhandle)
for i in range(7):
    pagehandle = pdfReader.getPage(i)
    print(pagehandle.extractText())