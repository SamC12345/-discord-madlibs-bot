from tinydb import TinyDB, Query

db = TinyDB("db.json")


def categoryExists(category):
    return 1 == db.count(Query().name == category)


def createCategory(category, words=[]):
    if not categoryExists(category):
        db.insert({"name": category, "words": words})


def getWordsFromCategory(category):
    createCategory(category)
    return db.get(Query().name == category)["words"]


def addToCategory(category, words):
    createCategory(category, words)
    existingWords = getWordsFromCategory(category)
    updatedWords = list(set(existingWords + words))
    if len(updatedWords) != len(existingWords):
        db.update({"words": updatedWords}, Query().name == category)


def getCategories():
    return [category["name"] for category in db.all()]