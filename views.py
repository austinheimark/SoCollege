from flask import (
    Flask, 
    render_template,
    redirect,
    url_for,
    request,
    session
    )
from flask.ext.sqlalchemy import SQLAlchemy
import os, sys, hashlib

app = Flask(__name__)
app.debug = True
app.secret_key = b'Q\x8b\xb3\x0f\xc0`u\xf4\xb8R\x0b\xbe\xe5^\xf5\xea\xe6\xf5\xc0\x8f\x95\xbcR\xdc\x84\xcb\x1fD\x84\x83:\xb6f\xb7\xc0\x19=M\\{\x9a+-a\xa9\xb3\x82B*\x86\t\x91\x11@\x92\x1a\x8d\xd1\x1d\xa4\xff.{\x91\x82\xf6\x10\x9b\x87\xb6\xcb cm\xf7\x81\x91\\k\xe0\x85\x92\xef\xe2\tyi\x1a\x0e\xbc\xbe\x8fN\x93\x84\xf8\xa4\x93\xd0e\x7f\xe7>=RN\x8c\ng8\x9b8\xa3\x1c\xecT#}\x88\xe5\xd2\xb1\x89\x07\xb8\xf2\xb0\x16\xb0h\x91\xe8\x92\x9c\x8aom\x15\n$\x1b\xb09\xb0\x86),\xac58\xeeY\xa6\xc4\x9a\xef\xa41\xc6 '
#app.config.from_object(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

#user table
class User(db.Model):
    username = db.Column(db.String, primary_key=True)
    email = db.Column(db.String)
    password = db.Column(db.String)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/dashboard")
def dashboard(page="Dashboard"):
    #ensure that the user is logged in

    return render_template('dashboard.html', page=page)

@app.route("/signup")
def signup(page="Sign up"):
    return render_template('signup.html', page=page)

@app.route("/signup/authenticate", methods=['POST'])
def signup_authenticate():
    #make sure all the form entry fields are there

    #check the databse to make sure that this user and email has not registered before
    # check_username = User.query.get(request.form['username'])
    # if check_username:
    #     flash('That username has been used.')
    #     return red irect(url_for('signup'))

    # check_email = User.query.get(request.form['email'])
    # if check_email:
    #     flash('That email has been used.')
    #     return redirect(url_for('signup'))

    #verify that the email is .edu

    #make sure the password matches the password verification

    #add the user to the database
    new_user = User(request.form['username'], request.form['email'], request.form['password'])    
    db.session.add(new_user)
    db.session.commit()

    #will need to set the session information so that the user is logged in here

    #flash('You successfully registered for this website!')
    return redirect(url_for('dashboard'))

@app.route("/signin")
def signin(page="Sign in"):
    return render_template('signin.html', page=page)

@app.route("/signin/authenticate", methods=['POST'])
def signin_authenticate():
    #search the User table for the entered email
    instance = User.query.get(request.form['username'])
    
    if request.form['username'] is instance.username and request.form['password'] is instance.password:
        return redirect(url_for('dashboard'))

    flash('Incorrect username-password combination!')
    return redirect(url_for('signin'))
    #set the session information


#unauthorized
@app.errorhandler(401)
def unauthorized_page(error):
    return render_template('401.html'), 401

#not found
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run()
