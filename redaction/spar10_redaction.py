import spacy
from spacy import displacy
nlp = spacy.load('en_core_web_sm')
import time
timestr = time.strftime("%Y%m%d-%H%M%S")
import fitz
import aspose.words as aw
import warnings
warnings.filterwarnings('ignore')

import re

def get_sensitive_data(lines,tt):
  docx = nlp(lines)
  redacted_sentences = []
  with docx.retokenize() as retokenizer:
    for ent in docx.ents:
      retokenizer.merge(ent)
  for token in docx:
    if token.ent_type_ == tt:
      yield token.text

def get_email_addresses(string):
  r = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')
  return r.findall(string)

def get_dates(string):
  r = re.compile(r'(?:\d{1,2}[-/th|st|nd|rd\s.])?(?:(?:Jan|January|Feb|February|Mar|March|Apr|April|May|Jun|June|Jul|July|August|Sep|September|Oct|October|Nov|November|Dec|December)[\s,.]*)?(?:(?:\d{1,2})[-/th|st|nd|rd\s,.]*)?(?:\d{2,4})')
  return r.findall(string)

def get_path(file_path):
  path = file_path

  if path.split('.')[-1] in ['docx','doc']:
    # Load word document
    doc = aw.Document(file_path)
    # Save as PDF
    path=file_path.split('.')[0]+'.pdf'
    doc.save(path)
  
  return path

def redaction(file_path,DOWNLOAD_FOLDER,filename,redaction_options):
	
  """ main redactor code """

  redactables = ['EMAIL','PERSON','GPE','LOC','ORG','TIME','DATE','MONEY','FAC','QUANITY','CARDINAL','ORDINAL'] #redaction options for reference
    
  # get the path of the pdf
  path = get_path(file_path)

  # opening the pdf
  doc = fitz.open(path)
  
  for page in doc:
    
    # _wrapContents is needed for fixing
    # alignment issues with rect boxes in some
    # cases where there is alignment issue
    page._wrapContents()
    
    # print('CONTENT:',page.getText("text"))

    for i in redaction_options:
      if i=='EMAIL':
        sensitive = get_email_addresses(page.getText("text"))

      elif i=='DATE':
        sensitive = get_dates(page.getText("text"))

      else:
        sensitive = get_sensitive_data(page.getText("text"),i)

      for data in sensitive:
        areas = page.searchFor(data)
          
        [page.addRedactAnnot(area, fill = (0, 0, 0)) for area in areas]
          
        page.apply_redactions()
          
  redactedfile = filename.split('.')[0]+'_redacted.pdf'
  redactedfilepath = DOWNLOAD_FOLDER + '/' + redactedfile

  doc.save(redactedfilepath)

  print("Successfully redacted")
  return redactedfile