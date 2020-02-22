#!/usr/bin/bsah
from mailer import Mailer
from mailer import Message
import mysql.connector
import time

#How often emails are considered to be sent
TIME = 600

#Mail setup
username = "notarmleg@gmail.com"
password = "Yellow123%"

sender = Mailer("smtp.gmail.com",usr=username,pwd=password, port=465,use_ssl=True)
sender.login(username,password)

#SQL Setup
mydb = mysql.connector.connect(host="localhost",user="admin",passwd="Yellow123%")


def getMessage(emailAddress):
    message = Message(From=username,To=emailAddress,charset="utf-8")
    message.Subject("Click this link!")
    message.Html = ("Spam email dont click links on emails like this!")
    return message


while True:
   
    #Fetch data from sql server
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM customers")
    myresult = mycursor.fetchall()
     
    for x in myresult:
        print(x)

    time.sleep(TIME)

sender.send(getMessage("lukebirchwood@hotmail.com"))

