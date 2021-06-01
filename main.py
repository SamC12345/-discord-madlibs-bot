import discord
from dotenv import dotenv_values
from commands import isCommand, handleCommand
from sentenceConverter import isSentenceToConvert, convertSentence

config = dotenv_values(".env")

DISCORD_BOT_KEY = config["DISCORD_BOT_KEY"]
CHANNEL_NAME = config["CHANNEL_NAME"]


class MyClient(discord.Client):
    async def on_ready(self):
        print("Logged on as {0}!".format(self.user))

    async def on_message(self, message):
        print("Message from {0.author}: {0.content}".format(message))
        if message.channel.name == CHANNEL_NAME and not message.author.bot:
            text = message.clean_content
            if isSentenceToConvert(text):
                returnMessage = convertSentence(text)
                await message.channel.send(returnMessage)
                print("sent message!")
            elif isCommand(text):
                returnMessage = handleCommand(text)
                await message.channel.send(returnMessage)
                print("sent message!")


client = MyClient()
client.run(DISCORD_BOT_KEY)