import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import Response
import logging
import discord
from vector_database import VectorDatabase
from embeddings import Embedding


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = Intents.default()
intents.message_content = True
client = Client(intents=intents)

vd = VectorDatabase()
emd = Embedding()


async def send_message(message):
    try:
        response = Response(vd, emd, message)
        response = response.get_response()
        if response == 'Succesfully saved your link':
            await message.add_reaction("✅")
        else:
            await message.author.send(response)
    except Exception as e:
        logging.error(e)
        await message.author.send('Something went wrong, use !help for more Information')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if isinstance(message.channel, discord.DMChannel):
        await send_message(message)


def main():
    client.run(TOKEN)


if __name__ == '__main__':
    main()
