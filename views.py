from flask import (
    Flask, 
    render_template,
    redirect,
    url_for,
    request,
    session,
    flash,
    abort
    )
from constants import CONSUMER_KEY, CONSUMER_SECRET, APP_SECRET_KEY
from flask.ext.sqlalchemy import SQLAlchemy
import sqlalchemy.orm
import os, sys, hashlib
import sqlite3
import datetime
import requests

app = Flask(__name__)
app.debug = True
app.secret_key = APP_SECRET_KEY
#app.config.from_object(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

#user table
class User(db.Model):
    username = db.Column(db.String, primary_key=True)
    email = db.Column(db.String)
    password = db.Column(db.String)
    posts = db.relationship('Post', backref = 'author', lazy = 'dynamic')

    def __init__(self,username,email,password):
        self.username = username
        self.email = email
        self.password = password

#posts table
class Post(db.Model):
    title = db.Column(db.String, primary_key=True)
    description = db.Column(db.String)
    pay = db.Column(db.String)
    location = db.Column(db.String)
    date = db.Column(db.String)
    user = db.Column(db.Integer, db.ForeignKey('user.username'))

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/dashboard")
def dashboard(page="Dashboard"):
    #ensure that the user is logged in
    if not session.get('username'): 
        abort(401)

    return render_template('dashboard.html', page=page)

@app.route("/signup")
def signup(page="Sign up"):
    return render_template('signup.html', page=page)

@app.route("/signup/authenticate", methods=['POST'])
def signup_authenticate():
    #make sure all the form entry fields are there

    #check the databse to make sure that this user and email has not registered before
    check_username = User.query.filter_by(username=request.form['username']).first()
    check_email = User.query.filter_by(email=request.form['email']).first()
    password = request.form['password']
    password_verification = request.form['verification']

    # print check_username.username
    if check_username is not None:
        flash('That username has been used.')
        return redirect(url_for('signup'))

    if check_email is not None:
        flash('That email has been used.')
        return redirect(url_for('signup'))

    #verify that the email is .edu

    #make sure the password matches the password verification
    if password != password_verification:
        flash('Passwords do not match')
        return redirect(url_for('signup'))

    encrypted = hashlib.sha1(request.form['password'])


    #add the user to the database
    new_user = User(request.form['username'], request.form['email'], encrypted.hexdigest())    
    db.session.add(new_user)
    db.session.commit()

    #will need to set the session information so that the user is logged in here
    session['username'] = request.form['username']

    # redirect user to venmo login
    if session.get('venmo_token'):
        flash("You have successfully logged into your Venmo, %s" % session.get('venmo_token'))
        return redirect(url_for('dashboard'))
    else:
        return redirect('https://api.venmo.com/oauth/authorize?client_id=%s&scope=make_payments,access_profile&response_type=code' % CONSUMER_KEY)

@app.route('/oauth-authorized')
def oauth_authorized():
    AUTHORIZATION_CODE = request.args.get('code')
    data = {
        "client_id":CONSUMER_KEY,
        "client_secret":CONSUMER_SECRET,
        "code":AUTHORIZATION_CODE
        }
    url = "https://api.venmo.com/oauth/access_token"
    response = requests.post(url, data)
    response_dict = response.json()
    app.logger.debug(response_dict)
    access_token = response_dict.get('access_token')
    user = response_dict.get('user')

    session['venmo_token'] = access_token
    session['venmo_username'] = user['username']
    session['venmo_name'] = user['name']
    session['venmo_firstname'] = user['firstname']
    session['venmo_lastname'] = user['lastname']
    session['venmo_picture'] = user['picture']
    session['venmo_email'] = user['email']
    session['venmo_phone'] = user['phone']
    session['venmo_balance'] = user['balance']
    session['venmo_id'] = user['id']

    flash("You have successfully logged into your Venmo, %s" % session.get('venmo_token'))
    return redirect(url_for('dashboard'))

@app.route("/signin")
def signin(page="Sign in"):
    return render_template('signin.html', page=page)

@app.route("/signin/authenticate", methods=['POST'])
def signin_authenticate():
    #search the User table for the entered email
    entered_username = request.form['username']
    entered_pass = hashlib.sha1(request.form['password'])

    encrypted_pass = entered_pass.hexdigest()

    instance = User.query.get(entered_username)

    #make sure the password is correct
    if entered_username == instance.username and encrypted_pass == instance.password:       
        #set the session information
        session['username'] = instance.username

        flash('You successfully signed in!')
        return redirect(url_for('dashboard'))

    #password and username must be incorrect
    flash('Incorrect username password combination.')
    return redirect(url_for('signin'))

@app.route("/signout")
def signout(page="Sign out"):
    #pop the session
    session.pop('username', None)
    session.pop('venmo_token', None)
    return render_template('signout.html', page=page)

@app.route("/newpost", methods=['POST'])
def newpost(page="New Post"):
    #make sure the user is logged in
    if not session.get('username'):
        abort(401)

    return render_template('newpost.html')

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

