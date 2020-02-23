#!/usr/bin/bsah
from mailer import Mailer
from mailer import Message
import mysql.connector
import time
import os
import random
import urllib.request

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


def execSql(sql):
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    out = mycursor.fetchall()
    mycursor.close()
    return out


def getMessage(emailAddress):
    message = Message(From=username, To=emailAddress, charset="utf-8")
    numOfSpamMail = execSql("SELECT COUNT(idSpamMail) FROM SpamMail")[0][0]
    randMailIndex = int(random.random() * numOfSpamMail + 1)
    print(str(randMailIndex))
    spamMail = execSql("SELECT idEmail FROM SpamMail WHERE idSpamMail = " + str(randMailIndex))[0][0]
    print(str(spamMail))
    urlResponse = urllib.request.urlopen("http://matrix.alexthomas.xyz/telloffsite/spamrepo/" + str(spamMail) + "/mail.txt")
    spamMessageContent = urlResponse.read()
    spamMessageText = spamMessageContent.decode(urlResponse.headers.get_content_charset('utf-8')).replace('\n', '<br>')
    message.Subject = ("Important document")
    message.Html = spamMessageText
    # message.Html = ("Please find attached")
    return message


while True:

    # Fetch data from sql server
    # mycursor = mydb.cursor()
    myresult = execSql("SELECT email, MaxEmailsPerMonth FROM user")
    # myresult = mycursor.fetchall()

    for x in myresult:
        prob = x[1] / 40000
        rand = random.random()
        if rand < prob or True:
            sender.send(getMessage(x[0]))
            print("Sent email: " + x[0])
    time.sleep(TIME)
    sender.send(getMessage("charlesyim1999@gmail.com"))

