from flask_login import login_required, current_user
from flask import Blueprint, render_template,redirect, url_for, request, flash,session
from system.models import User,Contact
import os
import re
from __init__ import create_app,db,postamail,UPLOAD_FOLDER,REDACTION_FOLDER
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage

system_review_summarization = Blueprint('system_review_summarization', __name__)

def allowed_files_for_revsum(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ['csv','xlsx']

@system_review_summarization.route("/review-summarization", methods=['GET', 'POST'])
@login_required
def reviewsummarization():
    if request.method == 'POST':
        reviewText = request.form.get('reviewtext')
        print(reviewText)
        print(request.files)

        if 'file1' not in request.files and reviewText == '':
            flash('No file part or review text is empty',"error")
            return redirect(url_for('system_review_summarization.reviewsummarization'))

        if request.files['file1'].filename !='' and reviewText != '':
            flash('Input either a file OR a text review, both wont do!',"error")
            return redirect(url_for('system_review_summarization.reviewsummarization'))

        file = request.files['file1']

        if file.filename == '' and  reviewText=='':
            flash('No selected file',"error")
            return redirect(url_for('system_review_summarization.reviewsummarization'))

        check = allowed_files_for_revsum(file.filename)
        print("CHECK:",check)

        if file and check == True:
            filename = secure_filename(file.filename)
            path_to_save= UPLOAD_FOLDER+ 'review_summarization' + filename
            file.save(os.path.join(UPLOAD_FOLDER+'review_summarization', filename))
            #load model and get summarized reviews 
            #save summarized file
            #redirect with summarized file path
            return render_template('system_views/reviewsummarization.html', file_name=path_to_save)

        if check == False:
            flash('Only excel files are allowed',"error")
            return redirect(url_for('system_review_summarization.reviewsummarization'))

        if reviewText != '':
            return render_template('system_views/reviewsummarization.html', review_text=reviewText)
    else:
        return render_template('system_views/reviewsummarization.html')