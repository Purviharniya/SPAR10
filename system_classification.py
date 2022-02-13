from flask_login import login_required, current_user
from flask import Blueprint, render_template,redirect, url_for, request, flash,session
from models import User,Contact
import os
import re
from __init__ import create_app,db,postamail,UPLOAD_FOLDER,DOWNLOAD_FOLDER
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from redaction.spar10_redaction import redaction

system_classification = Blueprint('system_classification', __name__)

@system_classification.route("/system-classification", methods=['GET', 'POST'])
@login_required
def systemclassification():
    if request.method == 'POST':
        file = request.files['file1']
        check = allowed_files_for_classification(file.filename)
        # print("CHECK:",check) to check if file extension is acceptable or not
 
        if file and check == True:
            filename = secure_filename(file.filename)
            path_to_save= UPLOAD_FOLDER + '/document_classification/' + filename
    
            file.save(path_to_save)

            return render_template('system_views/systemclassification.html')

        if check == False:
            flash('Only pdf/doc/docx/jpg/png/jpeg files are allowed',"error")
            return redirect(url_for('system_classification.systemclassification'))
    
    else:
        return render_template('system_views/systemclassification.html')

def allowed_files_for_classification(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ['pdf','doc','docx','jpg','png','jpeg']
