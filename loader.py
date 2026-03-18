from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from data.config import TOKEN

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode="HTML")
)

dp = Dispatcher()