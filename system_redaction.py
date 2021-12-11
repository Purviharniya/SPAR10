from flask_login import login_required, current_user
from flask import Blueprint, render_template,redirect, url_for, request, flash,session
from models import User,Contact
import os
import re
from __init__ import create_app,db,postamail,UPLOAD_FOLDER,REDACTION_FOLDER
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from py_files.spar10_redaction import redaction

system_redaction = Blueprint('system_redaction', __name__)

@system_redaction.route("/system-redaction", methods=['GET', 'POST'])
@login_required
def systemredaction():
    if request.method == 'POST':
        file = request.files['file1']

        check = allowed_file_for_redaction(file.filename)
        # print("CHECK:",check) to check if file extension is acceptable or not
 
        if file and check == True:
            # print("LINE 23: ",secure_filename())
            filename = secure_filename(file.filename)
            path_to_save= REDACTION_FOLDER + '/' + filename
            print(path_to_save)
            file.save(path_to_save)

            #load model and get summarized reviews 
            redaction()
            
            #save summarized file
            #redirect with summarized file path
            flash('The redacted file has been downloaded',"success")
            return redirect(url_for('system_redaction.systemredaction'))

        if check == False:
            flash('Only excel files are allowed',"error")
            return redirect(url_for('system_redaction.systemredaction'))
    
    else:
        return render_template('system_views/systemredaction.html')

def allowed_file_for_redaction(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ['pdf','doc','docx']