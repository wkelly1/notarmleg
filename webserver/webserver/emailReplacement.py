import random
import urllib
domain = "http://10.14.180.244:5000"
nameFile = "webserver/names.txt"

def processRepoText(text, idEmail, repo, emailAddress):
    generateUrl(idEmail, repo)
    text = text.replace("{{.URL}}", generateUrl(idEmail, repo))
    name = getRandomName()
    firstName = name.split(" ")[0]
    lastName = name.split(" ")[1]
    text = text.replace("{{.FirstName}}", firstName)
    text = text.replace("{{.LastName}}", lastName)
    text = text.replace("{{.Tracker}}", "")
    text = text.replace("{{.Email}}", emailAddress)
    return text

def generateUrl(spamID, repo):
    url = domain + "/telloffpage?spamid=" + spamID + "&repo=" + urllib.parse.quote(repo) + "/"
    return url

def getRandomName():
    lines = open(nameFile).read().splitlines()
    myline =random.choice(lines)
    return myline