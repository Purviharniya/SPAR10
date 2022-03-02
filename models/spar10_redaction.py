# NLP libraries
import spacy
nlp = spacy.load('en_core_web_sm')

# Time Pkg
import time
timestr = time.strftime("%Y%m%d-%H%M%S")

# for opening pdf
import fitz

# for dealing for docx
import aspose.words as aw

# fr ignoring warnings
import warnings
warnings.filterwarnings('ignore')

import re

"""# CODE"""

def get_sensitive_data(lines,tt):
	
  docx = nlp(lines)
  for ent in docx.ents:
    ent.merge()
  for token in docx:
    if token.ent_type_ == tt:
      yield token.string

def get_email_addresses(string):
  
  r = re.compile(r'[\w\.-]+@[\w\.-]+')
  return r.findall(string)

def get_path():

  # replace it with name of the pdf file
  path = "C:/Users/91720/Desktop/STUDY/NOTES/SEM 7/LY project/Code/SPAR10/uploads/review_summarization/testing.pdf"

  if path[-4:]=='docx':
    
    # Load word document
    doc = aw.Document("C:/Users/91720/Desktop/STUDY/NOTES/SEM 7/LY project/Code/SPAR10/uploads/review_summarization/testing.docx")
    # Save as PDF
    doc.save("C:/Users/91720/Desktop/STUDY/NOTES/SEM 7/LY project/Code/SPAR10/uploads/review_summarization/testing.pdf")
    path="C:/Users/91720/Desktop/STUDY/NOTES/SEM 7/LY project/Code/SPAR10/uploads/review_summarization/testing.pdf"

  return path

def redaction():
	
  """ main redactor code """

  redactables = ['EMAIL','PERSON','GPE','LOC','ORG','TIME','DATE','MONEY','FAC','QUANITY','CARDINAL','ORDINAL']
    
  # get the path of the pdf
  path = get_path()
    
  # opening the pdf
  doc = fitz.open(path)
    
  # iterating through pages
  for page in doc:
    
    # _wrapContents is needed for fixing
    # alignment issues with rect boxes in some
    # cases where there is alignment issue
    page._wrapContents()
    
    for i in redactables:

      # getting the react boxes which consists the matching email regex or the NER's
      
      if i=='EMAIL':
        sensitive = get_email_addresses(page.getText("text"))
      
      else:
        sensitive = get_sensitive_data(page.getText("text"),i)
    
      for data in sensitive:
        areas = page.searchFor(data)
          
        # drawing outline over sensitive datas
        [page.addRedactAnnot(area, fill = (0, 0, 0)) for area in areas]
          
        # applying the redaction
        page.apply_redactions()
      
  # saving it to a new pdf
  doc.save('redacted.pdf')
  print("Successfully redacted")

redaction()