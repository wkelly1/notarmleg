import MySQLdb
from MySQLdb import escape_string as thwart
"""
"""
class DatabaseConnection:

    def __init__(self, address, user, password, database):
        self.address = address
        self.user = user
        self.password = password
        self.database = database

    """
    
    """
    def connect(self):
        self.conn = MySQLdb.connect(host=self.address,
                               port=3306,
                               user=self.user,
                               passwd=self.password,
                               db=self.database)

        c = self.conn.cursor()
        return c, self.conn

    def disconnect(self):
        self.conn.close()


    def addEmail(self, email, number):
        try:
            c, conn = self.connect()
            c.execute("INSERT INTO User (email, maxEmailsPerMonth)  VALUES (%s, %s)", (thwart(email), thwart(number),))
            conn.commit()
            self.disconnect()
            return True
        except Exception:
            return False

    def removeEmail(self, email):
        try:
            c, conn = self.connect()
            c.execute("DELETE from User WHERE email = (%s)", (thwart(email),))
            conn.commit()
            self.disconnect()
            return True
        except Exception:
            return False


    def updateSpamTable(self, mailID, repo):
        try:
            c, conn = self.connect()
            no = c.execute("SELECT * FROM spammail WHERE idEmail = %s", (thwart(mailID),))
            print(no)
            if no == 0:
                c.execute("INSERT INTO spammail (numClicked, repo, idEmail) VALUES (%s, %s, %s)", (1, thwart(repo), thwart(mailID),))
            else:
                c.execute("SELECT numClicked FROM spammail WHERE idEmail = %s", (thwart(mailID),))
                no = c.fetchone()[0]
                print(no)
                c.execute("UPDATE spammail SET numClicked = %s WHERE idEmail = %s", (no+1, thwart(mailID),))

            conn.commit()
            self.disconnect()
            print("here")
            return True
        except:
            return False

    def getMostClicked(self):
        try:
            c, conn = self.connect()
            c.execute("SELECT idEmail, repo, numClicked FROM SpamMail ORDER BY numClicked DESC LIMIT 1")
            data = c.fetchone()
            print(data)
            self.disconnect()
            return [data[0], data[1], data[2]]
        except:
            return []

