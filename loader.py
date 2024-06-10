from aiogram import Bot,Dispatcher
from data.config import BOT_TOKEN
# Import Database Class
from utils.db_api.postgresql import Database
from aiogram.fsm.storage.memory import MemoryStorage
bot=Bot(token=BOT_TOKEN)
dp=Dispatcher(storage=MemoryStorage())
# Create database
db = Database()
