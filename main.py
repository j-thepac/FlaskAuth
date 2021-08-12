"""
 r=requests.post(url="http://127.0.0.1:5000/login",data={"email":'foo@bar.tld',"password":'secret'},verify=False)


"""
import os
import flask_login
from flask import render_template,Flask,request,redirect,url_for

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") #os.environ.get("SECRETKEY")  # random key used to encrypt your cookies and save send them to the browser
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
users = {'test@gmail.com': "pass"}

class User(flask_login.UserMixin):
    def __init__(self,  email):self.id = email

# Each time the logged-in user navigates to a new page, Flask-Login retrieves the ID of the user from the session, and then loads that user into memory.
@login_manager.user_loader
def user_loader(email):
    if email not in users:return None
    user = User(email)
    return user

def validate(email,password):
    if email not in users or password != users[email]: return False
    return True

@login_manager.request_loader #used for api only
def request_loader(request):
    token = request.headers.get('Authorization')# if token is None:token = request.args.get('token')
    if token is not None:
        email,password = token.split(":") # naive token
        if (validate(email, password)):
            user = User(email)
            flask_login.login_user(user)
            return user
        return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':return render_template("index.html")
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if(validate(email,password)):
            user = User(email)
            flask_login.login_user(user)
            return redirect(url_for('protected'))
    return 'Bad login'

@app.route('/protected')
@flask_login.login_required
def protected(): return 'Loggedin:'+ flask_login.current_user.id

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'

@login_manager.unauthorized_handler
def unauthorized_handler():return 'Unauthorized'

if __name__=="__main__":
    app.run(debug=True)
