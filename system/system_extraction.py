from flask_login import login_required
from flask import Blueprint, render_template,redirect, url_for, request, flash
from __init__ import UPLOAD_FOLDER,DOWNLOAD_FOLDER
from werkzeug.utils import secure_filename
from extractor import extraction

system_extraction = Blueprint('system_extraction', __name__)

@system_extraction.route("/system-extraction", methods=['GET', 'POST'])
@login_required
def systemextraction():
    if request.method == 'POST':
        file = request.files['file1']
        check = allowed_files_for_extraction(file.filename)
        # print("CHECK:",check) to check if file extension is acceptable or not
        extraction_options = request.form.getlist('foptions')

        if file and extraction_options!=[] and check == True:
            filename = secure_filename(file.filename)
            path_to_save = UPLOAD_FOLDER + '/text_extraction/' + filename
            file.save(path_to_save)

            extracted_text = extraction.text_extractor()

            return render_template('system_views/extraction_result.html', data = extracted_text, options = extraction_options)

        if check == False:
            flash('Only pdf/png/jpg/jpeg files are allowed',"error")
            return redirect(url_for('system_extraction.systemextraction'))
    
    else:
        return render_template('system_views/systemextraction.html')

def allowed_files_for_extraction(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ['pdf','jpg','png','jpeg']
