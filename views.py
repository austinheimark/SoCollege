from flask import (
    Flask, 
    render_template,
    redirect,
    url_for,
    request
    )
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.debug = True
app.secret_key = 'something'
app.config.from_object(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

#user table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
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

    #flash('You successfully registered for this website!')
    return render_template('dashboard.html')

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