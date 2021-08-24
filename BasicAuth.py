
# r=requests.post(url="http://127.0.0.1:5000/login",data={"email":'foo@bar.tld',"password":'secret'},verify=False)

import os
from flask_httpauth import HTTPBasicAuth
from flask import render_template,Flask,request,redirect,url_for

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") #os.environ.get("SECRETKEY")  # random key used to encrypt your cookies and save send them to the browser
auth=HTTPBasicAuth()
users = {'test': "pass"}

@auth.verify_password
def validate(email,password):
    if email not in users or password != users[email]: return False
    return True


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':return render_template("index.html")
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if(validate(email,password)):
            return redirect(url_for('protected'))
    return 'Bad login'


@app.route('/protected')
@auth.login_required()
def protected():
    return 'Loggedin:'+auth.current_user()


@auth.error_handler
def auth_error(status):
    return "Access Denied", status


if __name__=="__main__":
    app.run(debug=True)
