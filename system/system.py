from flask_login import login_required, current_user
from flask import Blueprint, render_template,redirect, url_for, request, flash
from werkzeug.security import generate_password_hash
from system.models import User
import re
from __init__ import db

system = Blueprint('system', __name__)

@system.route("/dashboard")
@login_required
def dashboard():
    return render_template('system_views/dashboard.html', name=current_user.name)

@system.route("/profile",methods=["POST","GET"])
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
            return redirect(url_for('system.profile'))
        
        if current_user.email != mail:
            user = User.query.filter_by(email=mail).first()

            if user: # if a user is found, we want to redirect back to signup page so user can try again
                flash(u'Email address already exists',"error")
                return redirect(url_for('system.profile'))

        try:
            db.session.commit()
            flash(u"Details updated successfully!","success")
            current_user.name = name
            current_user.email = mail
            current_user.contact = contact
            return render_template('system_views/profile.html', name=current_user.name , user = current_user)
        except:
            flash(u"Looks like there is some error with database!","error")
            return render_template('system_views/profile.html', name=current_user.name , user = current_user)

    else:    
        return render_template('system_views/profile.html', name=current_user.name , user = current_user)


def validate_profile_details(name,email,contact):

    if name=='' or email =='' or contact =='':
        return("Please fill all the fields!")
    
    if not re.fullmatch(re.compile(r'^[a-zA-Z ]+$'), name):
        return('Invalid name')

    if not re.fullmatch(re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'), email):
        return('Invalid email address')
       
    return True

@system.route("/settings",methods=["POST","GET"])
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