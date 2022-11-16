from flask import Flask,render_template
app=Flask(__name__)

@app.route("/")
@app.route("/index.php")
def home():
    return render_template('index.php')

@app.route("/signup.php")
def signup():
    return render_template('signup.php')
if __name__=='__main__':
    app.run(debug=True)