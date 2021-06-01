from wonderwords import RandomWord
import random
import db_func
from dotenv import dotenv_values

config = dotenv_values(".env")
FLAG = config["FLAG"]

r = RandomWord()


def getRandomWord(partOfSpeech):
    return r.word(include_parts_of_speech=[partOfSpeech])


def getRandomVerb():
    return getRandomWord("verbs")


def getRandomAdjective():
    return getRandomWord("adjectives")


def getRandomNoun():
    return getRandomWord("nouns")


def getRandomAdverb():
    return getRandomWord("verbs")


def isSentenceToConvert(text):
    words = text.split(" ")
    for i in range(len(words)):
        if words[i].startswith(FLAG):
            command = words[i][1:]
            if command in POSReplaceableWords or db_func.categoryExists(command):
                return True
    return False


def convertSentence(sentence):
    words = sentence.split(" ")
    for i in range(len(words)):
        if words[i].startswith(FLAG):
            command = words[i][1:]
            print(command)
            if command in POSReplaceableWords:
                words[i] = POSReplaceableWords[command]()
            elif db_func.categoryExists(command):
                words[i] = random.choice(db_func.getWordsFromCategory(command))
    return " ".join(words)


POSReplaceableWords = {
    "vrb": getRandomVerb,
    "adject": getRandomAdjective,
    "noun": getRandomNoun,
    "adverb": getRandomAdverb,
}
