import MySQLdb

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
        c, conn = self.connect()
        c.execute("INSERT INTO User (email, maxEmailsPerMonth)  VALUES (%s, %s)", (email, number,))
        self.disconnect()
