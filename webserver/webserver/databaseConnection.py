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


    #def updateSpamTable(self, mailID, repo):