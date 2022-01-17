from flask_login import login_required, current_user
from flask import Blueprint, render_template,redirect, url_for, request, flash,session
from models import User,Contact
import os
import re
from __init__ import create_app,db,postamail,UPLOAD_FOLDER
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage

from summarizer import Summarizer, TransformerSummarizer

system_para_summarization = Blueprint('system_para_summarization', __name__)

def allowed_files_for_revsum(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ['csv','xlsx']

@system_para_summarization.route("/para-summarization", methods=['GET', 'POST'])
@login_required
def parasummarization():
    if request.method == 'POST':
        paraText = request.form.get('paratext')
        print(paraText)
        print(request.files)

        if 'file1' not in request.files and paraText == '':
            flash('No file part or para text is empty',"error")
            return redirect(url_for('system_para_summarization.parasummarization'))

        if request.files['file1'].filename !='' and paraText != '':
            flash('Input either a file OR a text para, both wont do!',"error")
            return redirect(url_for('system_para_summarization.parasummarization'))

        file = request.files['file1']

        if file.filename == '' and  paraText=='':
            flash('No selected file',"error")
            return redirect(url_for('system_para_summarization.parasummarization'))

        check = allowed_files_for_revsum(file.filename)
        print("CHECK:",check)

        if file and check == True:
            filename = secure_filename(file.filename)
            path_to_save= UPLOAD_FOLDER+ 'para_summarization' + filename
            file.save(os.path.join(UPLOAD_FOLDER+'para_summarization', filename))
            #load model and get summarized paras 
            #save summarized file
            #redirect with summarized file path
            return render_template('system_views/parasummarization.html', file_name=path_to_save)

        if check == False:
            flash('Only excel files are allowed',"error")
            return redirect(url_for('system_para_summarization.parasummarization'))

        if paraText != '':
            return render_template('system_views/parasummarization.html', para_text=paraText)
    else:
        return render_template('system_views/parasummarization.html')