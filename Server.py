#!/usr/bin/bsah
from mailer import Mailer
from mailer import Message
import mysql.connector
import time
import os
import random

#How often emails are considered to be sent
TIME = 10

#Mail setup
username = "notarmleg@gmail.com"
password = "Yellow123%"

sender = Mailer("smtp.gmail.com",usr=username,pwd=password, port=465,use_ssl=True)
sender.login(username,password)

pwd = os.environ.get("SQL_PASS")
#SQL Setup
mydb = mysql.connector.connect(host="localhost",user="root",passwd=pwd, database="mydb")


def getMessage(emailAddress):
    message = Message(From=username,To=emailAddress,charset="utf-8")
    message.Subject = ("Important document")
    message.Html = ("Please find attached")
    return message


while True:
   
    #Fetch data from sql server
    mycursor = mydb.cursor()
    mycursor.execute("SELECT email, MaxEmailsPerMonth FROM user")
    myresult = mycursor.fetchall()
     
    for x in myresult:
        prob = x[1]/40000
        rand = random.random()
        if rand < prob or True:
            sender.send(getMessage(x[0]))
            print("Sent email: " + x[0])
    time.sleep(TIME)

sender.send(getMessage("lukebirchwood@hotmail.com"))

