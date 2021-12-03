from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from __init__ import db,postamail
from flask_login import login_user, login_required, logout_user
import re
import random
import string

auth = Blueprint('auth', __name__)

@auth.route("/login")
def login():
    return render_template('login.html')

@auth.route("/signup")
def signup():
    return render_template('signup.html')

def validate_signup(name,email,password,cpassword,contact,remember):

    if name=='' or email =='' or password=='' or contact =='':
        return("Please fill all the fields!")

    if password != cpassword:
        return('Passwords don\'t match')
    
    if not re.fullmatch(re.compile(r'^[a-zA-Z ]+$'), name):
        return('Invalid name')

    if not re.fullmatch(re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'), email):
        return('Invalid email address')
         
    if not re.fullmatch(re.compile("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"), password):
        return('Password Should have at least one number, at least one uppercase and one lowercase character,at least one special symbol,be between 6 to 20 characters.')
         
    if password != cpassword:
        return('Your passwords dont match')
         
    if remember==False:
        return('Agree to the terms and conditions')
         
    return True

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    cpassword = request.form.get('confirm-password')
    contact =  request.form.get('contactno')
    remember = True if request.form.get('tnc') else False
    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    check_valid = validate_signup(name,email,password,cpassword,contact,remember)

    if check_valid != True:
        flash(check_valid,"error")
        return redirect(url_for('auth.signup'))

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash(u'Email address already exists',"error")
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'),contact=contact)

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    flash(u'Registered Successfully! Please login',"success")
    return redirect(url_for('auth.login'))

@auth.route('/login', methods=['POST'])
def login_post():
    # login code goes here
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    if email=='' or password =='':
        flash(u"Please fill all the fields","error")
        return redirect(url_for('auth.login'))
        
    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash(u'Please check your login details and try again.',"error")
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.dashboard'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@auth.route('/forgotpass',methods=["POST","GET"])
def forgotpass():
    if request.method=="POST":
        mail = request.form['mail']
        check = User.query.filter_by(mail=mail).first()
        if check:
            hashCode = ''.join(random.choices(string.ascii_letters + string.digits, k=24))
            check.hashCode = hashCode
            db.session.commit()
            msg = Message('Confirm Password Change', sender = 'purvi.h@somaiya.edu', recipients = [mail])
            msg.body = "Hello,\nWe've received a request to reset your password. If you want to reset your password, click the link below and enter your new password\n http://localhost:5000/" + check.hashCode
            postamail.send(msg)
            flash(u'Updation link has been sent to your mail',"success")
            return render_template('forgotpass.html')
    else:
        return render_template('forgotpass.html')

@auth.route("/<string:hashCode>",methods=["GET","POST"])
def hashcode(hashCode):
    check = User.query.filter_by(hashCode=hashCode).first()    
    if check:
        if request.method == 'POST':
            passw = request.form['passw']
            cpassw = request.form['cpassw']
            if passw == cpassw:
                check.password = passw
                check.hashCode= None
                db.session.commit()
                flash(u'Passwords updated successfully',"success")
                return redirect(url_for('auth.login'))
            else:
                flash(u'The passwords don\'t match',"error")
                return render_template('reenterpass.html')
        else:
            return render_template('reenterpass.html')
    else :
        return redirect(url_for('main.not_found'))