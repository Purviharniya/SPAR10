from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
import os
from system import filehandling

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()
# SQLALCHEMY_TRACK_MODIFICATIONS = False
postamail = Mail()


def get_SPAR10_dir_path():
    path = os.path.dirname(os.path.abspath(__file__))
    return path.replace("\\", "/")


SPAR10_directory = get_SPAR10_dir_path()

filehandling_object = filehandling.FileHandling(SPAR10_directory)

UPLOAD_FOLDER, DOWNLOAD_FOLDER, REDACTION_FOLDER, REVSUM_FOLDER, PARASUM_FOLDER, EXTRACTION_FOLDER, DOCCLASS_FOLDER = filehandling_object.get_all_paths()


def create_app():
    app = Flask(__name__)

    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'spar10.project@gmail.com'
    app.config['MAIL_PASSWORD'] = 'SPAR10PROJECT'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  # main directory of uploads
    # redaction folder for uploads
    app.config['REDACTION_FOLDER'] = REDACTION_FOLDER
    # para summarization folder for uploads
    app.config['PARASUM_FOLDER'] = PARASUM_FOLDER

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

    from system.models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from system.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from system.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from system.system import system as system_blueprint
    app.register_blueprint(system_blueprint)

    from system.system_redaction import system_redaction as system_redaction_blueprint
    app.register_blueprint(system_redaction_blueprint)

    from system.system_para_summarization import system_para_summarization as system_para_summarization_blueprint
    app.register_blueprint(system_para_summarization_blueprint)

    from system.system_extraction import system_extraction as system_extraction_blueprint
    app.register_blueprint(system_extraction_blueprint)

    from system.system_classification import system_classification as system_classification_blueprint
    app.register_blueprint(system_classification_blueprint)

    return app
