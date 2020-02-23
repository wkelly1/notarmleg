import sys
import os
import re
import mysql.connector
import urllib.request
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
import sys, csv, nltk, math


#csvFilePath = sys.argv[1]
#inputFilePath = sys.argv[2]

punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''

def remove_attrs(soup, whitelist=tuple()):
    for tag in soup.findAll(True):
        for attr in [attr for attr in tag.attrs if attr not in whitelist]:
            del tag[attr]
    return soup

def functionCor(csvFilePath, htmlText):

    soup = BeautifulSoup(htmlText,'html5lib')
    
    [s.extract() for s in soup('style')]
        
    inputTextStripped2 = soup.get_text(strip=True)
    
    tokens = [t for t in inputTextStripped2.split()]
    
    clean_tokens = tokens[:]
    for token in tokens:

        if token in stopwords.words('english'):
            clean_tokens.remove(token)
    
    freq = nltk.FreqDist(clean_tokens)

    #Take input from CSV
    with open(csvFilePath) as csv_file:
        csv_reader = csv.reader(csv_file)
        positive = 0
        for key,val in freq.items():
            
            for x in csv_reader:
                xval = key
                no_punct = ""
                for char in xval:
                   if char not in punctuations:
                       no_punct = no_punct + char
                if (xval.strip().lower() == x[0] or xval.strip() == x[0]):
                    positive += float(x[1]) * val

    return positive

def functionSig(csvFilePath, htmlText):
        
        soup = BeautifulSoup(htmlText,'html5lib')

        [s.extract() for s in soup('style')]

        inputTextStripped2 = soup.get_text(strip=True)
        
        tokens = [t for t in inputTextStripped2.split()]

        clean_tokens = tokens[:]
        for token in tokens:
            if token in stopwords.words('english'):
                clean_tokens.remove(token)

        freq = nltk.FreqDist(clean_tokens)

        #Take input from CSV
        with open(csvFilePath) as csv_file:
            csv_reader = csv.reader(csv_file)
            positive = 0
            negative = 0
            for key,val in freq.items():
                for x in csv_reader:
                    xval = key
                    no_punct = ""
                    for char in xval:
                       if char not in punctuations:
                           no_punct = no_punct + char

                    if (x[2] == xval.lower()) or (x[2] == xval.upper()):
                        positive += float(x[1]) * val
                        negative += float(x[1]) * val
                        

        def sigmoid(x):
          return 1 / (1 + math.exp(-x))

        if negative == 0:
            return (sigmoid(positive))
        elif positive == 0:
            return (sigmoid(negative))
        elif negative > positive:
            return (sigmoid(positive/negative))
        else:
            return (sigmoid(negative/positive))

def functionDif(csvFilePath, htmlText):
        
        soup = BeautifulSoup(htmlText,'html5lib')

        [s.extract() for s in soup('style')]

        inputTextStripped2 = soup.get_text(strip=True)

        tokens = [t for t in inputTextStripped2.split()]

        clean_tokens = tokens[:]
        for token in tokens:
            if token in stopwords.words('english'):
                clean_tokens.remove(token)

        freq = nltk.FreqDist(clean_tokens)

        #Take input from CSV
        with open(csvFilePath) as csv_file:
            csv_reader = csv.reader(csv_file)
            sum = 0
            count = 0
            for key,val in freq.items():
             
                for x in csv_reader:
                    
                    xval = key
                    no_punct = ""
                    for char in xval:
                       if char not in punctuations:
                           no_punct = no_punct + char
                    if (x[0] == xval.lower() or x[0] == xval.upper()):
                        sum += float(x[4])
                        count = count + 1
        try:
            average = sum / count
            return average
        except:
            return 5
            
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

    email = urllib.request.urlopen(repo+ "/" + i + '/mail.txt').read().decode("utf-8")

    cor = functionCor("nlp/csv/correctness.csv", email)
    sig = functionSig("nlp/csv/significance.csv", email)
    dif = functionDif("nlp/csv/difficulty.csv", email)

    print(cor,sig,dif)
    addMLSQL = "INSERT INTO classification (idSpamMail, difficulty, correctness, significance) VALUES ((SELECT idSpamMail FROM spammail WHERE idEmail = '" + i + "'), '" + str(cor) + "', '" + str(sig) + "', '" + str(dif) + "')"
    execChangeSql(addMLSQL)
    
    if len(sql) == 0:
        sql2 = "INSERT INTO spammail (repo, idEmail) VALUES ('" + repo + "', '" + i + "')"
        execChangeSql(sql2)
        print("Adding mail: " + i)


        
        
        

    


