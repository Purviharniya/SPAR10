from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager    
from flask_mail import Mail, Message
from flask import render_template
import os

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()
# SQLALCHEMY_TRACK_MODIFICATIONS = False 
postamail = Mail()

def get_SPAR10_dir_path():
    path = os.path.dirname(os.path.abspath(__file__))
    return path

SPAR10_directory = get_SPAR10_dir_path().replace("\\","/")
# print(SPAR10_directory)  #to check for the correct directory 

def create_uploads_folder_and_get_path(dir):
    path_uploads = dir +'/uploads'  
    if not os.path.exists(path_uploads):
        os.makedirs(path_uploads)

    return path_uploads

def create_downloads_folder_and_get_path(dir):
    path_downloads = dir +'/downloads' 
    if not os.path.exists(path_downloads):
        os.makedirs(path_downloads)

    return path_downloads

UPLOAD_FOLDER = create_uploads_folder_and_get_path(SPAR10_directory)
DOWNLOAD_FOLDER = create_downloads_folder_and_get_path(SPAR10_directory)
# print(DOWNLOAD_FOLDER) #check for uploads folder path  #C:/Users/User/projects/SPAR10/downloads

def create_redaction_folder_and_get_path(dir):
    path_redaction = dir +'/redaction'
    if not os.path.exists(path_redaction):
        os.makedirs(path_redaction)
    return path_redaction

def create_docsum_folder_and_get_path(dir):
    path_docsum = dir +'/document_summarization'
    if not os.path.exists(path_docsum):
        os.makedirs(path_docsum)
    return path_docsum

def create_revsum_folder_and_get_path(dir):
    path_revsum = dir +'/review_summarization'
    if not os.path.exists(path_revsum):
        os.makedirs(path_revsum)
    return path_revsum

def create_parasum_folder_and_get_path(dir):
    path_parasum = dir +'/review_summarization'
    if not os.path.exists(path_parasum):
        os.makedirs(path_parasum)
    return path_parasum

def create_extraction_folder_and_get_path(dir):
    path_extraction = dir +'/text_extraction'
    if not os.path.exists(path_extraction):
        os.makedirs(path_extraction)
    return path_extraction

def create_docclass_folder_and_get_path(dir):
    path_docclass = dir +'/document_classification'
    if not os.path.exists(path_docclass):
        os.makedirs(path_docclass)
    return path_docclass

def create_textclass_folder_and_get_path(dir):
    path_textclass = dir +'/document_classification'
    if not os.path.exists(path_textclass):
        os.makedirs(path_textclass)
    return path_textclass

REDACTION_FOLDER = create_redaction_folder_and_get_path(UPLOAD_FOLDER) #redaction folder
DOCSUM_FOLDER = create_docsum_folder_and_get_path(UPLOAD_FOLDER) #document summarization folder
REVSUM_FOLDER = create_revsum_folder_and_get_path(UPLOAD_FOLDER) #review summarization folder
PARASUM_FOLDER = create_parasum_folder_and_get_path(UPLOAD_FOLDER) #review summarization folder
EXTRACTION_FOLDER = create_extraction_folder_and_get_path(UPLOAD_FOLDER) #text extraction folder
DOCCLASS_FOLDER = create_docclass_folder_and_get_path(UPLOAD_FOLDER) #document classification folder
TEXTCLASS_FOLDER = create_textclass_folder_and_get_path(UPLOAD_FOLDER) #text classification folder

def create_app():
    app = Flask(__name__)

    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'spar10.project@gmail.com'
    app.config['MAIL_PASSWORD'] = 'SPAR10PROJECT'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['REDACTION_FOLDER'] = REDACTION_FOLDER
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

    from system import system as system_blueprint
    app.register_blueprint(system_blueprint)

    # from system_redaction import system_redaction as system_redaction_blueprint
    # app.register_blueprint(system_redaction_blueprint)

    from system_review_summarization import system_review_summarization as system_review_summarization_blueprint
    app.register_blueprint(system_review_summarization_blueprint)

    from system_para_summarization import system_para_summarization as system_para_summarization_blueprint
    app.register_blueprint(system_para_summarization_blueprint)

    # from system_redaction import system_redaction as system_redaction_blueprint
    # app.register_blueprint(system_redaction_blueprint)

    # from system_redaction import system_redaction as system_redaction_blueprint
    # app.register_blueprint(system_redaction_blueprint)

    return app