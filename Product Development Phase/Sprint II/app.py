from flask import Flask, render_template, request, redirect, url_for, session
import ibm_db
import re
import smtplib;

app = Flask(__name__)
  
app.secret_key = 'a'

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=815fa4db-dc03-4c70-869a-a9cc13f33084.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=30367;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=xlw42871;PWD=wOwGVowCPcnr1kXc",'','')

@app.route('/')

def home():
    return render_template('home.html')


@app.route('/login',methods =['GET', 'POST'])
def login():
    global userid
    msg = ''
   
  
    if request.method == 'POST' :
        username = request.form['username']
        password = request.form['password']
        sql = "SELECT * FROM users WHERE username =? AND password=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.bind_param(stmt,2,password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print (account)
        if account:
            session['loggedin'] = True
            session['id'] = account['USERNAME']
            userid=  account['USERNAME']
            session['username'] = account['USERNAME']
            msg = 'Logged in successfully !'
            
            msg = 'Logged in successfully !'
            return render_template('dashboard.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)

        

   
@app.route('/register', methods =['GET', 'POST'])
def registet():
    msg = ''
    if request.method == 'POST' :
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        sql = "SELECT * FROM users WHERE username =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers !'
        else:
            insert_sql = "INSERT INTO  users VALUES (?, ?, ?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, username)
            ibm_db.bind_param(prep_stmt, 2, email)
            ibm_db.bind_param(prep_stmt, 3, password)
            ibm_db.execute(prep_stmt)
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)

@app.route('/dashboard')
def dash():
    
    return render_template('dashboard.html')

@app.route('/apply',methods =['GET', 'POST'])
def apply():
     msg = ''
     if request.method == 'POST' :
         username = request.form['username']
         email = request.form['email']
         
         u_query= request.form['u_query']
        #  jobs = request.form['s']
         sql = "SELECT * FROM users WHERE username =?"
         stmt = ibm_db.prepare(conn, sql)
         ibm_db.bind_param(stmt,1,username)
         ibm_db.execute(stmt)
         account = ibm_db.fetch_assoc(stmt)
         print(account)
         if account:
            insert_sql = "INSERT INTO queries(username, email, u_query) VALUES (?, ?, ?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, username)
            ibm_db.bind_param(prep_stmt, 2, email)
            ibm_db.bind_param(prep_stmt, 3, u_query)
        #  ibm_db.bind_param(prep_stmt, 4, skills)
        #  ibm_db.bind_param(prep_stmt, 5, jobs)
            ibm_db.execute(prep_stmt)
            msg = 'Your Query has been Registered Successfully'
            session['loggedin'] = True
            TEXT = "Hello"+username+", your query has been Registered Successfully"
            ser = smtplib.SMTP('smtp.gmail.com',587);
            ser.starttls();
            ser.login('customercareregistry2022@gmail.com','rxwgqzuguhicknur')
            ser.sendmail('customercareregistry2022@gmail.com',email,TEXT);
         elif request.method == 'POST':
            msg = 'Register FIRST'
            return render_template('register.html', msg = msg)
        #  print('mail sent');
         #sendmail(TEXT,"sandeep@thesmartbridge.com")
        #  sendgridmail("sandeep@thesmartbridge.com",TEXT)
        #  rxwgqzuguhicknur
         
     elif request.method == 'POST':
         msg = 'Please fill out the form !'
     return render_template('apply.html', msg = msg)

@app.route('/display')
def display():
    sql = "SELECT * FROM queries WHERE USERNAME = '"+session['id']+"'"
    stmt = ibm_db.exec_immediate(conn,sql)
    acnt = []
    # abc = ibm_db.fetch_row(stmt)
    # print(session['id'] + " abc : "+ abc)
        # print(abc)
    while ibm_db.fetch_row(stmt)!=False:
        account = dict()
        account["username"] = ibm_db.result(stmt,"username")
        account["email"] = ibm_db.result(stmt,"email")
        account["u_query"] = ibm_db.result(stmt,"u_query")
        print(account)
        acnt.append(account)
        # abc = ibm_db.fetch_row(stmt)

    return render_template('display.html',acnt = acnt)


@app.route('/logout')

def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   return render_template('home.html')


    
if __name__ == '__main__':
   app.run(host='0.0.0.0')
