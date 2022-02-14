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


if __name__ == '__main__':
    db.create_all(app=create_app()) # create the SQLite database
    create_app().run(debug=True) # run the flask app on debug mode
