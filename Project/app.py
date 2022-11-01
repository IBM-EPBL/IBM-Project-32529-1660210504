from contextlib import redirect_stderr
from flask import render_template, url_for
from flask import Flask

app = Flask(__name__)            

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/support')
def support():
    return render_template('support.html')

@app.route('/about')
def about():
    return render_template('about.html')

#@app.errorhandler(404)
#def page_not_found(e):
#    return render_template('404.html'), 404   

if __name__=='__main__':
    app.run(debug=True) 