from dotenv import dotenv_values
import db_func
import random
from sentenceConverter import POSReplaceableWords

config = dotenv_values(".env")
FLAG = config["FLAG"]


async def createCategory(args, message):
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


async def getWordsFromCategory(args, message):
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


async def addWordsToCategory(args, message):
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


async def handleCommand(text, message):
    words = text.split(" ")
    if len(words) > 0 and words[0].startswith(FLAG):
        command = words[0][1:].lower()
        args = words[1:]
        if command in commands:
            return await commands[command](args, message)
    return "handling command"


async def listCategories(args, message):
    return f'the following categories exist: {", ".join(db_func.getCategories())}'


async def help(args, message):
    return f'here\'s my commands: {", ". join(commands.keys())}'


async def quote(args, message):
    if message.reference == None:
        return "reply to a message to quote it"
    else:
        messageToQuote = await message.channel.fetch_message(
            message.reference.message_id
        )
        quoteNumber = db_func.addQuote(
            messageToQuote.clean_content, messageToQuote.jump_url
        )
        return f'quote #{quoteNumber}: "{messageToQuote.clean_content}"'


async def getQuote(args, message):
    if len(args) == 0:
        return "please specify a quote number"
    elif len(args) == 1:
        if not args[0].isnumeric():
            return "please specify a numeric quote number"
        else:
            quoteNumber = int(args[0])
            quote = db_func.getQuote(quoteNumber)
            if quote == None:
                return f"couldn't find quote #{quoteNumber}"
            else:
                return f'quote #{quoteNumber}: "{quote["quote"]}"'
    return "couldn't process your request :/"


async def getRandomQuote(args, message):
    quotes = db_func.getQuotes()
    if len(quotes) == 0:
        return "no quotes found :'("
    else:
        quote = random.choice(quotes)
        return f'quote #{quote["number"]}: "{quote["quote"]}"'


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
    "quote": quote,
    "q": quote,
    "quoteget": getQuote,
    "qg": getQuote,
    "quoterandom": getRandomQuote,
    "qr": getRandomQuote,
}
