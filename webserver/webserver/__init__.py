from flask import Flask, render_template, request, flash
from MySQLdb import escape_string as thwart
from webserver.databaseConnection import DatabaseConnection
import os

app = Flask(__name__)
app.config.from_object('configuration')


pwd = os.environ.get("SQL_PASS")
databaseConnection = DatabaseConnection("127.0.0.1", "root", pwd, "mydb")

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        email = request.form.get("email")
        maxEmails = request.form.get("maxNo")
        print(email, maxEmails)
        if databaseConnection.addEmail(email, maxEmails):
            flash("You will now receive some spam tests!", "alert-success")
        else:
            flash("Something has gone wrong!", "alert-danger")
    return render_template("index.html")

@app.route('/unsubscribe', methods=["GET", "POST"])
def unsubscribe():
    if request.method == "POST":
        email = request.form.get("email")

        databaseConnection.removeEmail(email)

    return render_template("unsubscribe.html")



