import sys
import discord
from discord.ext import commands
import asyncio
import aiohttp
import ssl
import certifi

from config import BOT_TOKEN



# Define intents
intents = discord.Intents.default()
intents.message_content = True  # Enable intents for message content
intents.members = True  # Enable Server Members Intent if needed

# SSL context
ssl_context = ssl.create_default_context(cafile=certifi.where())

initial_extensions = ['cogs.tasks', 'cogs.helper', 'cogs.transaction', 'cogs.rewards']
#, 'cogs.rewards', 'cogs.transactions', 'cogs.users', cogs.rewards]

bot = commands.Bot(command_prefix='!', intents=intents)

async def load_extensions():
    for extension in initial_extensions:
        try:
            await bot.load_extension(extension)
        except Exception as e:
            print(f'Failed to load extension {extension}.', file=sys.stderr)
            print(e, file=sys.stderr)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

async def main():
    await load_extensions()
    await bot.start(BOT_TOKEN, reconnect=True)

if __name__ == '__main__':
    asyncio.run(main())


