import sys
import os
import mysql.connector
import urllib.request

pwd = os.environ.get("SQL_PASS")
# SQL Setup
mydb = mysql.connector.connect(host="localhost", user="root", passwd=pwd, database="mydb")

try: 
    repo = sys.argv[1]
except:
    print("Missing argument: repo")
    sys.exit(0)
          
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


urlResponse = urllib.request.urlopen(str(repo) + "/mail.csv")
mail = urlResponse.read().decode("utf-8").replace('\r', '').replace('\n', '').split(",")

# Iterate over mail in spamrepo
for i in mail:
    sql = "SELECT * FROM spammail WHERE idEmail='" + i + "'"
    sql = execSelectSql(sql)
    if len(sql) == 0:
        sql = "INSERT INTO spammail (repo, idEmail) VALUES ('" + repo + "', '" + i + "')"
        execChangeSql(sql)
        print("Adding mail: " + i)
