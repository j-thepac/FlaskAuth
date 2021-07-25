"""
 r=requests.post(url="http://127.0.0.1:5000/login",data={"email":'foo@bar.tld',"password":'secret'},verify=False)


"""
import os

import flask_login,flask
from flask import render_template

app = flask.Flask(__name__)
app.secret_key = os.environ.get("SECRETKEY")  # random key used to encrypt your cookies and save send them to the browser
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

users = {'foo@bar.tld': {'password':  os.environ.get("password") }}#

class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    if email not in users:return
    user = User()
    user.id = email
    return user

# @login_manager.request_loader
# def request_loader(request):
#     email = request.form.get('email')
#     if email not in users: return
#     user = User()
#     user.id = email
#     user.is_authenticated = request.form['password'] == users[email]['password']
#     return user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return render_template("index.html")
    if flask.request.method == 'POST':
        email = flask.request.form['email']
        if flask.request.form['password'] == users[email]['password']:
            user = User()
            user.id = email
            flask_login.login_user(user)
            return flask.redirect(flask.url_for('protected'))

    return 'Bad login'


@app.route('/protected')
@flask_login.login_required
def protected(): return 'Logged in as: ' + flask_login.current_user.id

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'

@login_manager.unauthorized_handler
def unauthorized_handler():return 'Unauthorized'

if __name__=="__main__":
    app.run(debug=True)
