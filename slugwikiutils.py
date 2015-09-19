#This function gets a quote from slugwiki
import mwclient
import random

class SlugWikiUtils:
    url = "slugwiki.mit.edu"
    quotesPage='Slug_Quotes'
    username="button711"
    password=""
    page711="711_button"
    def __init__(self):
        useragent = 'YourBot, based on mwclient v0.7.2. Run by User: Ivan ivanaf@mit.edu'
        self.site = mwclient.Site(('http', self.url), clients_useragent=useragent, path ='/')
        if self.password!="":
            self.site.login(self.username, self.password)
    def getRandomQuote(self):
        page = self.site.Pages[self.quotesPage]
        pageText=page.text()
        sentences=page.text().split('\n')
        numberOfSentences=len(sentences)
        
        people= [k for k in sentences if "'''"in k] #Filter sentences that have ''' are the ones with names of people
        numberOfPeople=len(people)
        randomPersonIndex = random.randrange(numberOfPeople)
        randomPerson = people[randomPersonIndex]
        
        randomPersonSentenceIndex=sentences.index(randomPerson)
        if randomPersonIndex<(numberOfPeople-1):
            nextPerson=people[randomPersonIndex+1]
            nextRandomPersonSentenceIndex = sentences.index(nextPerson)

        else:
            nextRandomPersonSentenceIndex=numberOfSentences #removes last line
        if (randomPersonSentenceIndex+1<nextRandomPersonSentenceIndex):
            for i in range(5): #try 5 times to get a non empty index
                randomSentenceIndex = random.randrange(randomPersonSentenceIndex+1, nextRandomPersonSentenceIndex)
                randomSentence= sentences[randomSentenceIndex]
                if randomSentence != "":
                    break
        else:
            randomPerson=""
            for i in range(5): #try 5 times to get a non empty index
                randomSentenceIndex = random.randrange(len(sentences))
                randomSentence= sentences[randomSentenceIndex]
                if randomSentence != "":
                    break

        return [randomPerson,sentences[randomSentenceIndex]]
    def getQuotesText(self):
        page = self.site.Pages[self.quotesPage]
        return page.text()
    def addTo711(self, text):
        page = self.site.Pages[self.page711]
        pageText=page.text()
        page.save(pageText + u'<br>' + text, summary = '711')

