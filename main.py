from __init__ import create_app,db

if __name__ == '__main__':
    db.create_all(app=create_app()) # create the SQLite database
    create_app().run(debug=True,port=10000) # run the flask app on debug mode