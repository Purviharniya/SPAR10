from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager    
from flask_mail import Mail, Message
from flask import render_template
# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()
# SQLALCHEMY_TRACK_MODIFICATIONS = False 
postamail = Mail()

UPLOAD_FOLDER = "C:/Users/User/projects/SPAR10/uploads/"

def create_app():
    app = Flask(__name__)

    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'spar10.project@gmail.com'
    app.config['MAIL_PASSWORD'] = 'SPAR10PROJECT'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    postamail = Mail(app)

    app.config['SECRET_KEY'] = 'SPAR10'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    db.init_app(app)

    # app.config['TRAP_HTTP_EXCEPTIONS']=True

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from system_redaction import system_redaction as system_redaction_blueprint
    app.register_blueprint(system_redaction_blueprint)

    # from review_summarization import system_redaction as system_redaction_blueprint
    # app.register_blueprint(system_redaction_blueprint)

    # from system_redaction import system_redaction as system_redaction_blueprint
    # app.register_blueprint(system_redaction_blueprint)

    # from system_redaction import system_redaction as system_redaction_blueprint
    # app.register_blueprint(system_redaction_blueprint)

    return app