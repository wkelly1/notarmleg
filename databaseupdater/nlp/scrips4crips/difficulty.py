from bs4 import BeautifulSoup
from nltk.corpus import stopwords
import sys, csv, nltk, math

#csvFilePath = sys.argv[1]
#inputFilePath = sys.argv[2]
class Difficulty:
    def functionDif(csvFilePath, htmlText):
        
        soup = BeautifulSoup(htmlText,'html5lib')

        inputTextStripped = soup.get_text(strip = True)

        tokens = [t for t in inputTextStripped.split()]

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
                    if (x[0] == key):
                        sum += float(x[4])
                        count = count + 1
        try:
            average = sum / count
            print (average)
        except:
            print(0)



