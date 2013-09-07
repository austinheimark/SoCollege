from flask import (
    Flask, 
    render_template,
    redirect,
    url_for
    )

app = Flask(__name__)



@app.route("/")
def home():
    return render_template('home.html')

@app.route("/dashboard")
def dashboard():
    #ensure that the user is logged in

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