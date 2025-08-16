import os
from dotenv import load_dotenv 
import twitchio
from twitchio.ext import commands

load_dotenv()

BOT_NICK = os.getenv("BOT_NICK")
TOKEN = os.getenv("TOKEN")
CHANNEL = os.getenv("CHANNEL")