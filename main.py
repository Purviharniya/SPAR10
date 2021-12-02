from flask import Blueprint, render_template
# from . import
from flask_login import login_required, current_user
from __init__ import create_app,db,postamail

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    return render_template('index.html')

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

@main.route("/profile")
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@main.route("/dashboard")
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.name)

if __name__ == '__main__':
    db.create_all(app=create_app()) # create the SQLite database
    create_app().run(debug=True) # run the flask app on debug mode