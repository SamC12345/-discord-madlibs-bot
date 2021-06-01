from dotenv import dotenv_values
import db_func
from sentenceConverter import POSReplaceableWords

config = dotenv_values(".env")
FLAG = config["FLAG"]


def createCategory(args):
    if len(args) == 0:
        return "please specify a category name"
    elif len(args) == 1:
        category = args[0]
        if isPartOfSpeechKeyword(category):
            return f'"{category}" is a part of speech!'
        db_func.createCategory(category)
        return f'created category "{category}"'
    elif len(args) > 1:
        category = args[0]
        wordsInCategory = args[1:]
        if isPartOfSpeechKeyword(category):
            return f'"{category}" is a part of speech!'
        db_func.createCategory(category, wordsInCategory)
        return f'created category "{category}" with the following words: {", ".join(wordsInCategory)}'
    return "couldn't process your request :/"


def getWordsFromCategory(args):
    if len(args) == 0:
        return "please specify a category name"
    elif len(args) == 1:
        category = args[0]
        if isPartOfSpeechKeyword(category):
            return f'"{category}" is a part of speech!'
        if not db_func.categoryExists(category):
            return "that category doesn't exist"
        else:
            words = db_func.getWordsFromCategory(category)
            if len(words) == 0:
                return f'there are no words in category "{category}"'
            else:
                return f'category "{category}" has the following words: {", ".join(sorted(words))}'
    return "couldn't process your request :/"


def addWordsToCategory(args):
    if len(args) == 0:
        return "please specify a category name"
    elif len(args) == 1:
        category = args[0]
        if isPartOfSpeechKeyword(category):
            return f'"{category}" is a part of speech!'
        return f'please specify some words to add to "{category}"'
    elif len(args) > 1:
        category = args[0]
        words = args[1:]
        if isPartOfSpeechKeyword(category):
            return f'"{category}" is a part of speech!'
        if not db_func.categoryExists(category):
            db_func.addToCategory(category, words)
            return f'created category "{category}" with the following words: {", ".join(sorted(words))}'
        else:
            db_func.addToCategory(category, words)
            return f'category "{category}" now has the following words: {", ".join(sorted(db_func.getWordsFromCategory(category)))}'
    return "couldn't process your request :/"


def isPartOfSpeechKeyword(word):
    return word in POSReplaceableWords


def isCommand(text):
    words = text.split(" ")
    if len(words) > 0 and words[0].startswith(FLAG):
        command = words[0][1:].lower()
        if command in commands:
            return True
    return False


def handleCommand(text):
    words = text.split(" ")
    if len(words) > 0 and words[0].startswith(FLAG):
        command = words[0][1:].lower()
        args = words[1:]
        if command in commands:
            return commands[command](args)
    return "handling command"


def listCategories(args):
    return f'the following categories exist: {", ".join(db_func.getCategories())}'


def help(args):
    return f'here\'s my commands: {", ". join(commands.keys())}'


commands = {
    "categorycreate": createCategory,
    "cc": createCategory,
    "categoryget": getWordsFromCategory,
    "cg": getWordsFromCategory,
    "categoryadd": addWordsToCategory,
    "ca": addWordsToCategory,
    "categorylist": listCategories,
    "cl": listCategories,
    "help": help,
    "h": help,
}
