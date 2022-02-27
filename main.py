from __init__ import create_app,db,postamail,UPLOAD_FOLDER

if __name__ == '__main__':
    db.create_all(app=create_app()) # create the SQLite database
    create_app().run(debug=True) # run the flask app on debug mode