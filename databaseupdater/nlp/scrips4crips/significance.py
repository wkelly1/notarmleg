from bs4 import BeautifulSoup
from nltk.corpus import stopwords
import sys, csv, nltk, math

class Signficance:
    def functionSig(csvFilePath, htmlText):
        
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
            positive = 0
            negative = 0
            for key,val in freq.items():
                for x in csv_reader:
                    if (x[2] == key):
                        positive += float(x[0])
                        negative += float(x[1])

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
