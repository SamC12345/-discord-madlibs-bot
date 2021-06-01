from tinydb import TinyDB, Query

db = TinyDB("db.json")
categories = db.table("categories")
quotes = db.table("quotes")


def categoryExists(category):
    return 1 == categories.count(Query().name == category)


def createCategory(category, words=[]):
    if not categoryExists(category):
        categories.insert({"name": category, "words": words})


def getWordsFromCategory(category):
    createCategory(category)
    return categories.get(Query().name == category)["words"]


def addToCategory(category, words):
    createCategory(category, words)
    existingWords = getWordsFromCategory(category)
    updatedWords = list(set(existingWords + words))
    if len(updatedWords) != len(existingWords):
        categories.update({"words": updatedWords}, Query().name == category)


def getCategories():
    return [category["name"] for category in categories.all()]


def getQuotes():
    return quotes.all()


def addQuote(quote, url):
    currQuoteCount = quotes.__len__()
    quotes.insert({"number": currQuoteCount + 1, "quote": quote, "url": url})
    return currQuoteCount + 1


def getQuote(quoteNumber):
    return quotes.get(Query().number == quoteNumber)