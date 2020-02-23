#!/usr/bin/bsah
from mailer import Mailer
from mailer import Message
import mysql.connector
import time
import os
import random
import urllib.request
import urllib

# How often emails are considered to be sent
TIME = 10

# Mail setup
username = "notarmleg@gmail.com"
password = "Yellow123%"

sender = Mailer("smtp.gmail.com", usr=username, pwd=password, port=465, use_ssl=True)
sender.login(username, password)

pwd = os.environ.get("SQL_PASS")
# SQL Setup
mydb = mysql.connector.connect(host="localhost", user="root", passwd=pwd, database="mydb")

domain = "http://10.14.180.244:5000"

nameFile = "names.txt"

def execSql(sql):
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    out = mycursor.fetchall()
    mycursor.close()
    return out

def processRepoText(text, idEmail, repo, emailAddress):
    generateUrl(idEmail, repo)
    text = text.replace("{{.URL}}", generateUrl(idEmail, repo))
    name = getRandomName()
    firstName = name.split(" ")[0]
    lastName = name.split(" ")[1]
    text = text.replace("{{.FirstName}}", firstName)
    text = text.replace("{{.LastName}}", lastName)
    text = text.replace("{{.Tracker}}", "")
    text = text.replace("{{.Email}}", emailAddress)
    return text

def generateUrl(spamID, repo):
    url = domain + "/telloffpage?spamid=" + spamID + "&repo=" + urllib.parse.quote(repo) + "/"
    return url

def getRandomName():
    lines = open(nameFile).read().splitlines()
    myline =random.choice(lines)
    return myline

def getMessage(emailAddress):
    message = Message(From=username, To=emailAddress, charset="utf-8")
    numOfSpamMail = execSql("SELECT COUNT(idSpamMail) FROM SpamMail")[0][0]
    randMailIndex = int(random.random() * numOfSpamMail + 1)
    print(str(randMailIndex))
    spamMail = execSql("SELECT idEmail, repo FROM SpamMail WHERE idSpamMail = " + str(randMailIndex))[0]

    idEmail = spamMail[0]
    repo = spamMail[1]

    urlResponse = urllib.request.urlopen(str(repo) + "/" + str(idEmail) + "/mail.txt")
    spamMessageContent = urlResponse.read()
    spamMessageText = spamMessageContent.decode(urlResponse.headers.get_content_charset('utf-8')).replace('\n', '<br>')

    testText = """
    <html>
    <head>
      <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
    </head>
    <body>
      <h3>Bulletin Alert!!</h3>
      <h3>Attention {{.FirstName}} {{.LastName}}:</h3>
    <p>Bulletin Headline: Crime Suspect</p>
    <p>Sending Agency: Police</p>
    <p>Bulletin Time: 18:47</p>
    <p>Bulletin Case#: 11-04626</p>
    <p>Bulletin Author: Leroy Jethro #8847</p>
    <p>Sending User #: 2892</p>
    <p><a href="{{.URL}}">To view the full bulletin alert click here</a></p>
    <br>
    <p>To unsubscribe from these emails click <a href="{{.URL}}">here</a></p>
    </body>{{.Tracker}}
    </html>
    """
    print(processRepoText(testText, idEmail, repo, emailAddress))
    
    urlResponse = urllib.request.urlopen(str(spamMail[1]) + "/" + str(spamMail[0]) + "/subject.txt")
    spamMessageSubjectText = urlResponse.read()
    spamMessageSubject = spamMessageSubjectText.decode(urlResponse.headers.get_content_charset('utf-8'))
    
    message.Subject = (spamMessageSubject)
    message.Html = spamMessageText

    return message


while True:

    # Fetch data from sql server
    # mycursor = mydb.cursor()
    myresult = execSql("SELECT * FROM user")
    # myresult = mycursor.fetchall()
    print(myresult)
    for x in myresult:
        prob = x[2] / 40000
        rand = random.random()
        if rand < prob or True:
            sender.send(getMessage(x[1]))
            print("Sent email: " + x[1])
    time.sleep(TIME)
    sender.send(getMessage("charlesyim1999@gmail.com"))

