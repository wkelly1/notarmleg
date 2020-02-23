import sys
import os
import mysql.connector
import urllib.request

pwd = os.environ.get("SQL_PASS")
# SQL Setup
mydb = mysql.connector.connect(host="localhost", user="root", passwd=pwd, database="mydb")

def execSelectSql(sql):
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    out = mycursor.fetchall()
    mycursor.close()
    return out

def execChangeSql(sql):
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    mydb.commit()
    mycursor.close()


sql = "SELECT difficulty, correctness, significance FROM classification"

stringOut = "["

for i in execSelectSql(sql):
    stringOut = stringOut + str(i[0]) + " " + str(i[1]) + " " + str(i[2]) + ";\n"

stringOut = stringOut + "];"



sql2 = "SELECT * FROM spammail"

stringOut2 = "["

for i in execSelectSql(sql2):

    clicks = i[1]
    sent = i[0]
    if sent != 0:    
        stringOut2 = stringOut2 + str(i[1]/i[0]) + "\n"

stringOut2 = stringOut2 + "];"


my_file = open("input.txt","w+")
my_file.write(stringOut)
my_file.close()

my_file2 = open("output.txt","w+")
my_file2.write(stringOut2)
my_file2.close()

