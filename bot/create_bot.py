from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


storage = MemoryStorage()
bot = Bot(token="5616533417:AAHp9h_EGANgri0GQM6Ms2CKDgQ2VNZslUc")
dp = Dispatcher(bot, storage=storage)