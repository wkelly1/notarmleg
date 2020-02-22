from flask import Flask, render_template, request
import databaseConnection
import os

app = Flask(__name__)

pwd = os.environ.get("SQL_PASS")
databaseConnection = databaseConnection.DatabaseConnection("127.0.0.1", "root", pwd, "mydb")

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        email = request.form.get("email")
        maxEmails = request.form.get("maxNo")
        print(email, maxEmails)
        databaseConnection.addEmail(email, maxEmails)

    return render_template("index.html")




if __name__ == '__main__':
    app.run()
