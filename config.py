from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
#BOT_APPID = os.getenv('DISCORD_APP_ID')
#BOT_PUBKEY = os.getenv('DISCORD_PUBLIC_KEY')

if BOT_TOKEN is None:
    raise ValueError("No BOT_TOKEN found in environment variables")