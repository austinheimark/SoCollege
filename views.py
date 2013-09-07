from flask import (
    Flask, 
    render_template,
    redirect,
    url_for,
    request
    )
from flask.ext.sqlalchemy import SQLAlchemy
import sys

app = Flask(__name__)
app.debug = True
app.secret_key = 'something'
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
def dashboard():
    #ensure that the user is logged in

    return render_template('dashboard.html')

@app.route("/signup")
def signup():
    return render_template('signup.html')

@app.route("/signup/authenticate", methods=['POST'])
def signup_authenticate():

    new_user = User(request.form['username'], request.form['email'], request.form['password'])    
    db.session.add(new_user)
    db.session.commit()

    #flash('You successfully registered for this website!')
    return redirect(url_for('home'))

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