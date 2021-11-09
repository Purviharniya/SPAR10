from flask import Flask, render_template, request, flash, redirect

# from PIL import Image

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('index.html')

@app.route("/about-us")
def aboutus():
    return render_template('aboutus.html')

@app.route("/contact")
def contact():
    return render_template('contactus.html')

@app.route("/faqs")
def faqs():
    return render_template('faqs.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/signup")
def singup():
    return render_template('signup.html')

@app.route("/text-extraction")
def textextraction():
    return render_template('textextraction.html')

@app.route("/text-summarization")
def textsummarization():
    return render_template('textsummarization.html')

@app.route("/text-classification")
def textclassification():
    return render_template('textclassification.html')

@app.route("/text-redaction")
def textredaction():
    return render_template('textredaction.html')

if __name__ == '__main__':
	app.run(debug = True)
