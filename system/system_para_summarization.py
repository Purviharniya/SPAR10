import time
from flask import (Blueprint, flash, redirect, render_template, request,
                   url_for)
from flask_login import login_required
from summarizer import TransformerSummarizer
from summarizer.file_summarization import file_summarizer
from werkzeug.utils import secure_filename
from __init__ import PARASUM_FOLDER

# from summarizer.sbert import SBertSummarizer

system_para_summarization = Blueprint('system_para_summarization', __name__)

transformer_model_key_dict = {'Albert':'albert-base-v2','XLNet':'xlnet-large-cased','Roberta':'roberta-large',
'BigBird':'google/bigbird-roberta-base','XLM':'xlm-mlm-en-2048','GPT2':'gpt2-large','Bert':'bert-base-uncased'}

def allowed_files_for_parasum(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ['doc','docx','pdf','txt']

@system_para_summarization.route("/para-summarization", methods=['GET', 'POST'])
@login_required
def parasummarization():
    if request.method == 'POST':
        paraText = request.form.get('paratext')
        option = request.form.get('options')
        model_type = request.form.get('model_type')
        # print("option:",option)
        option_value=0  # ratio or num of sentence
        # print(paraText)
        # print(request.files)

        if 'file1' not in request.files and paraText == '':
            flash('No file part or paragraph text is empty',"error")
            return redirect(url_for('system_para_summarization.parasummarization'))

        if request.files['file1'].filename !='' and paraText != '':
            flash('Input either a file OR a text para, both won\'t do!',"error")
            return redirect(url_for('system_para_summarization.parasummarization'))

        if option=='0':
            flash('Select an option for summarizing the text!',"error")
            return redirect(url_for('system_para_summarization.parasummarization'))

        elif option=='1':
            ratio = request.form.get('ratio')
            # print("RATIO",type(ratio)) #str
            if not ratio.replace('.','',1).isdigit():
                ratio=0.0
            ratio = float(ratio)
            print("RATIO",ratio)
            if ratio<=0.0 or ratio>=1.0:
                flash('Enter a valid ratio!',"error")
                return redirect(url_for('system_para_summarization.parasummarization'))
            else:
                option_value=ratio

        elif option=='2':
            sentence = request.form.get('num_sent')
            if not sentence.isnumeric():
                sentence=0
            sentence = int(sentence)
            if sentence=='' or sentence<=0:
                flash('Enter a valid sentence count!',"error")
                return redirect(url_for('system_para_summarization.parasummarization'))
            else:
                option_value = sentence

        else:
            flash('Select an option for summarizing the text!',"error")
            return redirect(url_for('system_para_summarization.parasummarization'))

        file = request.files['file1']

        if file.filename == '' and  paraText=='':
            flash('No file selected',"error")
            return redirect(url_for('system_para_summarization.parasummarization'))

        check = allowed_files_for_parasum(file.filename)
        # print("CHECK:",check)
        # print(file)
        
        # global model
        model = TransformerSummarizer(transformer_type=model_type,transformer_model_key=transformer_model_key_dict[model_type]) 

        if file:
            if check == True:
                t = time.localtime()
                timestamp = time.strftime('%b-%d-%Y_%H_%M_%S', t)
                filename = file.filename.split('.')[0] + '_' + timestamp + '.' + file.filename.split('.')[1] 
                filename = secure_filename(filename)
                path_to_save= PARASUM_FOLDER + '/' + filename
                file.save(path_to_save)

                #extract text from file 
                extracted_text = file_summarizer(path_to_save)
                # print("EXTRACTED STRING",extracted_text)
                #load model and get summarized para  
                if type(option_value)==int:
                    result = model(extracted_text, num_sentences=option_value,min_length=30)  # Specified with ratio
                else:
                    result = model(extracted_text, ratio=option_value,min_length=30)
                # redirect to a new page with original and summarized text
                print(result)
                
                return render_template('system_views/parasummarizationresult.html', para_text=extracted_text,result=result)

            else:
                flash('Only pdf/doc/docx/txt files are allowed',"error")
                return redirect(url_for('system_para_summarization.parasummarization'))

        if paraText != '':
            # print('paraText is being passed')
            # print(paraText)
            # load model and get the summarized para 
            if type(option_value)==int:
                result = model(paraText, num_sentences=option_value)  # Specified with ratio
            else:
                result = model(paraText, ratio=option_value)
            # redirect to a new page with original and summarized text
            # print(result)
            
            return render_template('system_views/parasummarizationresult.html', para_text=paraText,result=result)
    else:
        return render_template('system_views/parasummarization.html')

