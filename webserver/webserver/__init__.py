from flask import Flask, render_template, request, flash, Markup, url_for, redirect
from MySQLdb import escape_string as thwart
from webserver.databaseConnection import DatabaseConnection
import os
import urllib.request
import json
from urllib import parse
import traceback
import webserver.emailReplacement

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
        flash("You have been unsubscribed!", "alert-success")
        return redirect(url_for("index"))
    return render_template("unsubscribe.html")



@app.route('/telloffpage')
def tellOffpage():
    arg = request.args.get("spamid")
    repo = request.args.get("repo")


    if arg == None or repo == None:
        return render_template("telloffpagewithoutmail.html")
    else:
        try:
            repo = parse.unquote(repo)

            data = urllib.request.urlopen(repo + arg + '/features.json').read()
            jsonData = json.loads(data)["features"]
            features = []
            for i in jsonData:
                print(i["repository"] + i["id"] + '/header.txt')
                header = urllib.request.urlopen(i["repository"] + i["id"] + '/header.txt').read().decode("utf-8")
                body = urllib.request.urlopen(i["repository"] + i["id"] + '/body.txt').read().decode("utf-8")
                print(i["repository"] + i["id"] + '/image.jpg')
                try:
                    img = repo + 'featurerepo/' + i["id"] + '/image.jpg'
                    print(img)
                except Exception:
                    print("Exception")
                    img = ""

                features.append([header, body, img])

            databaseConnection.updateSpamTable(arg, repo)
            return render_template("telloffpage.html", features=features)
        except Exception:
            traceback.print_exc()
            return render_template("telloffpagewithoutmail.html")



@app.route('/stats')
def stats():
    data = databaseConnection.getMostClicked()
    if len(data) > 0:
        try:
            print(data[1] + data[0] + '/mail.txt')
            text = urllib.request.urlopen(
                data[1] + data[0] + '/mail.txt').read().decode("utf-8")
            text = Markup(text)
            text = emailReplacement.processRepoText(text, data[0], data[1], "example@example.com")
        except:
            text = "Hmmm something has gone wrong!"
    return render_template("stats.html", text=text)