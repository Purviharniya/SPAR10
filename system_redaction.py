from flask_login import login_required, current_user
from flask import Blueprint, render_template,redirect, url_for, request, flash,session
from models import User,Contact
import os
import re
from __init__ import create_app,db,postamail,UPLOAD_FOLDER

system_redaction = Blueprint('system_redaction', __name__)

@system_redaction.route("/system-redaction", methods=['GET', 'POST'])
@login_required
def systemredaction():
    if request.method == 'POST':
        file = request.files['file1']

        check = allowed_file(file.filename)
        print("CHECK:",check)

        if file and check == True:
            filename = secure_filename(file.filename)
            path_to_save= UPLOAD_FOLDER+ 'review_summarization' + filename
            file.save(os.path.join(UPLOAD_FOLDER+'review_summarization', filename))
            import py_files.spar10_redaction
            #load model and get summarized reviews 

            #save summarized file
            #redirect with summarized file path
            return render_template('system_views/system_redaction.html', file_name=path_to_save)

        if check == False:
            flash('Only excel files are allowed',"error")
            return redirect(url_for('system_redaction.systemredaction'))
    
    else:
        return render_template('system_views/systemredaction.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ['pdf']