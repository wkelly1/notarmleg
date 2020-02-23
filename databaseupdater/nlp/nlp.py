import os

import mysql
from scrips4crips import correctness
from scrips4crips import difficulty
from scrips4crips import significance

pwd = os.environ.get("SQL_PASS")
mydb = mysql.connector.connect(host="localhost", user="root", passwd=pwd, database="mydb")


def execSql(sql):
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    out = mycursor.fetchall()
    mycursor.close()
    return out

def updateCor(idSpamMail):
    correctness.functionCor()