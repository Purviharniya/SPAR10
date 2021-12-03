from flask import Blueprint, render_template,redirect, url_for, request, flash,session
# from . import
from flask_login import login_required, current_user
from __init__ import create_app,db,postamail
import re

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    return render_template('index.html')

@main.route("/page404")
def not_found():
    return render_template("404.html")

@main.route("/overview")
def overview():
    return render_template('overview.html')

@main.route("/about-us")
def aboutus():
    return render_template('aboutus.html')

@main.route("/contact-us")
def contact():
    return render_template('contactus.html')

@main.route("/faqs")
def faqs():
    return render_template('faqs.html')

@main.route("/text-extraction")
def textextraction():
    return render_template('textextraction.html')

@main.route("/text-summarization")
def textsummarization():
    return render_template('textsummarization.html')

@main.route("/text-classification")
def textclassification():
    return render_template('textclassification.html')

@main.route("/text-redaction")
def textredaction():
    return render_template('textredaction.html')

def validate_profile_details(name,email,contact):

    if name=='' or email =='' or contact =='':
        return("Please fill all the fields!")
    
    if not re.fullmatch(re.compile(r'^[a-zA-Z ]+$'), name):
        return('Invalid name')

    if not re.fullmatch(re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'), email):
        return('Invalid email address')
       
    return True

@main.route("/profile",methods=["POST","GET"])
@login_required
def profile():
    if request.method=='POST':
        name = request.form['name']
        mail = request.form['email']
        contact = request.form['contact']
        id = current_user.id

        check_valid = validate_profile_details(name,mail,contact)
        if check_valid != True:
            flash(check_valid,"error")
            return redirect(url_for('main.profile'))

        try:
            db.session.commit()
            flash(u"Details updated successfully!","success")
            current_user.name = name
            current_user.email = mail
            current_user.contact = contact
            return render_template('profile.html', name=current_user.name , user = current_user)
        except:
            flash(u"Looks like there is some error with database!","error")
            return render_template('profile.html', name=current_user.name , user = current_user)

    else:    
        return render_template('profile.html', name=current_user.name , user = current_user)

# @main.route("/settings",methods=["POST","GET"])
# @login_required
# def settings():


@main.route("/dashboard")
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.name)

if __name__ == '__main__':
    db.create_all(app=create_app()) # create the SQLite database
    create_app().run(debug=True) # run the flask app on debug mode
