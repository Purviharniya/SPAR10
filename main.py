from flask import Blueprint, render_template,redirect, url_for, request, flash,session
# from . import
from flask_login import login_required, current_user
from __init__ import create_app,db,postamail,UPLOAD_FOLDER
import re
from models import User,Contact
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os



main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    return render_template('main_views/index.html')

@main.route("/page404")
def not_found():
    return render_template("partials/404.html")

@main.route("/overview")
def overview():
    return render_template('main_views/overview.html')

@main.route("/about-us")
def aboutus():
    return render_template('main_views/aboutus.html')

def validate_contactus(name,email,subject,message):

    if name=='' or email=="" or subject=="" or message=="":
        return("Please fill all the fields!")

    if len(message)<10:
        return("Message should have a minimum of 10 characters")

    if not re.fullmatch(re.compile(r'^[a-zA-Z ]+$'), name):
        return('Invalid name')

    if not re.fullmatch(re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'), email):
        return('Invalid email address')

    return True

@main.route("/contact-us",methods=['GET','POST'])
def contact():
    if request.method=='POST':
        email = request.form.get('email')
        name = request.form.get('name')
        subject = request.form.get('subject')
        message = request.form.get('message')

        check_valid = validate_contactus(name,email,subject,message)
        if check_valid != True:
            flash(check_valid,"error")
            return redirect(url_for('main.contact'))

        new_letter = Contact(email=email, name=name, subject=subject,message=message)
        db.session.add(new_letter)  # Adds new User record to database
        db.session.commit()  # Commits all changes

        flash("We have received your message! Stay tuned!","success")
        return redirect(url_for('main.contact'))

    else:
        return render_template('main_views/contactus.html')

@main.route("/faqs")
def faqs():
    return render_template('main_views/faqs.html')

@main.route("/text-extraction")
def textextraction():
    return render_template('main_views/textextraction.html')

@main.route("/text-summarization")
def textsummarization():
    return render_template('main_views/textsummarization.html')

@main.route("/text-classification")
def textclassification():
    return render_template('main_views/textclassification.html')

@main.route("/text-redaction")
def textredaction():
    return render_template('main_views/textredaction.html')

def validate_profile_details(name,email,contact):

    if name=='' or email =='' or contact =='':
        return("Please fill all the fields!")
    
    if not re.fullmatch(re.compile(r'^[a-zA-Z ]+$'), name):
        return('Invalid name')

    if not re.fullmatch(re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'), email):
        return('Invalid email address')
       
    return True

@main.route("/settings",methods=["POST","GET"])
@login_required
def settings():
    if request.method=="POST":
        passw = request.form['password']
        cpassw = request.form['confirm-password']

        if not re.fullmatch(re.compile("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"), passw):
            flash('Password should have at least one number, at least one uppercase and one lowercase character,at least one special symbol,be between 6 to 20 characters.','error')
            return render_template('system_views/settings.html', name=current_user.name)

        if cpassw != passw:
            flash('Passwords don\'t match!','error')
            return render_template('system_views/settings.html', name=current_user.name)
        
        check = User.query.filter_by(email=current_user.email).first()
        check.password = generate_password_hash(passw, method='sha256')
        db.session.commit()
        flash(u'Password updated successfully',"success")
        return render_template('system_views/settings.html', name=current_user.name)

    else:
        return render_template('system_views/settings.html', name=current_user.name)



@main.route("/review-summarization", methods=['GET', 'POST'])
@login_required
def reviewsummarization():
    if request.method == 'POST':
        reviewText = request.form.get('reviewtext')
        print(reviewText)
        print(request.files)

        if 'file1' not in request.files and reviewText == '':
            flash('No file part or review text is empty',"error")
            return redirect(url_for('main.reviewsummarization'))

        if request.files['file1'].filename !='' and reviewText != '':
            flash('Input either a file OR a text review, both wont do!',"error")
            return redirect(url_for('main.reviewsummarization'))
        
        file = request.files['file1']

        if file.filename == '' and  reviewText=='':
            flash('No selected file',"error")
            return redirect(url_for('main.reviewsummarization'))

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
            return render_template('system_views/reviewsummarization.html', file_name=path_to_save)

        if check == False:
            flash('Only excel files are allowed',"error")
            return redirect(url_for('main.reviewsummarization'))

        if reviewText != '':
            return render_template('system_views/reviewsummarization.html', review_text=reviewText)
        
    else:
        return render_template('system_views/reviewsummarization.html')

if __name__ == '__main__':
    db.create_all(app=create_app()) # create the SQLite database
    create_app().run(debug=True) # run the flask app on debug mode
